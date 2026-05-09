"""
语音助手模块 — 录音 → Whisper → DeepSeek API → IndexTTS 播放

集成进 DyberPet：
  右键菜单点击 "🎤 语音助手" → 录音 → 宠物冒泡显示状态 → TTS 播报

配置：编辑项目根目录下的 config_voice.json（勿提交到 git）。
"""
import os
import sys
import json
import time
import tempfile
import threading
from pathlib import Path

import numpy as np
import httpx

from PySide6.QtCore import QObject, Signal

import DyberPet.settings as settings

SAMPLE_RATE = 16000

# ── 从外部配置文件加载（不提交 git） ────────────
_config = {}
_cfg_path = Path(__file__).parent.parent / "config_voice.json"
if _cfg_path.exists():
    try:
        _config = json.loads(_cfg_path.read_text(encoding="utf-8"))
    except Exception:
        pass

API_CHAT = _config.get("api_chat", "http://127.0.0.1:8765/anthropic/messages")
API_KEY = _config.get("api_key", "")
API_TTS = _config.get("api_tts", "")
TTS_VOICE = _config.get("tts_voice", "")
WHISPER_PATH = _config.get("whisper_model_path", "")
SYSTEM_PROMPT = _config.get("system_prompt", "用简短的中文回答，不超过50字。")


class VoiceAssistant(QObject):
    """语音助手，跑在独立线程里，通过信号反馈状态。"""

    show_bubble = Signal(dict, int, int)
    show_notification = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._recording = False
        self._audio_chunks = []
        self._whisper_model = None
        self._model_lock = threading.Lock()

    # ── 公开 API ────────────────────────────────

    def start_recording(self):
        if self._recording:
            return
        self._recording = True
        self._audio_chunks = []
        self.show_notification.emit("system", "🎤 录音中...")
        threading.Thread(target=self._record_thread, daemon=True).start()

    def stop_recording(self):
        if not self._recording:
            return
        self._recording = False
        self.show_notification.emit("system", "📝 识别中...")
        threading.Thread(target=self._process_pipeline, daemon=True).start()

    def toggle_recording(self):
        if self._recording:
            self.stop_recording()
        else:
            self.start_recording()

    # ── 录音 ────────────────────────────────────

    def _record_thread(self):
        import sounddevice as sd
        try:
            with sd.InputStream(
                samplerate=SAMPLE_RATE, channels=1,
                dtype="float32", callback=self._on_audio,
                blocksize=int(SAMPLE_RATE * 0.1),
            ):
                while self._recording:
                    sd.sleep(50)
        except Exception as e:
            self._recording = False
            self.show_notification.emit("system", f"🎤 录音出错: {e}")

    def _on_audio(self, indata, frames, time_info, status):
        if self._recording:
            self._audio_chunks.append(indata.copy())

    # ── 管线 ────────────────────────────────────

    def _process_pipeline(self):
        time.sleep(0.2)

        n = len(self._audio_chunks)
        if n < 5:
            self.show_notification.emit("system", "🎤 录音太短")
            return

        audio = np.concatenate(self._audio_chunks, axis=0).flatten()
        text = self._transcribe(audio)
        if not text:
            self.show_notification.emit("system", "😕 没听清")
            return

        self.show_bubble.emit({"message": f"📝 {text}"}, 0, -60)

        self.show_notification.emit("system", "🤖 思考中...")
        reply = self._ask_ai(text)
        if not reply:
            self.show_notification.emit("system", "😕 AI 没响应")
            return

        self.show_notification.emit("system", "♫ 播放中...")
        self.show_bubble.emit({"message": reply}, 0, -60)
        self._play_tts(reply)

        self.show_notification.emit("system", "✅ 完成")

    # ── 组件 ────────────────────────────────────

    def _load_whisper(self):
        if self._whisper_model is not None:
            return
        with self._model_lock:
            if self._whisper_model is not None:
                return
            from faster_whisper import WhisperModel
            mp = WHISPER_PATH or str(Path.home() / ".cache" / "faster-whisper" / "tiny-copy")
            self._whisper_model = WhisperModel(mp, device="cpu", compute_type="int8")

    def _transcribe(self, audio):
        try:
            self._load_whisper()
            segments, _ = self._whisper_model.transcribe(audio, beam_size=5, language="zh")
            return " ".join(s.text for s in segments).strip()
        except Exception as e:
            sys.stderr.write(f"[voice] Transcribe error: {e}\n")
            return ""

    def _ask_ai(self, text):
        try:
            r = httpx.post(
                API_CHAT,
                json={
                    "model": "deepseek-v4-flash",
                    "system": SYSTEM_PROMPT,
                    "messages": [{"role": "user", "content": text}],
                    "max_tokens": 200,
                },
                headers={"x-api-key": API_KEY, "anthropic-version": "2023-06-01"},
                timeout=30,
            )
            if r.status_code == 200:
                blocks = r.json().get("content", [])
                return "".join(b["text"] for b in blocks if b.get("type") == "text")
        except Exception as e:
            sys.stderr.write(f"[voice] API error: {e}\n")
        return ""

    def _play_tts(self, text):
        import winsound
        try:
            r = httpx.get(API_TTS, params={"text": text, "voice": TTS_VOICE}, timeout=60)
            if r.status_code == 200:
                p = os.path.join(tempfile.gettempdir(), f"vox_{time.time_ns()}.wav")
                with open(p, "wb") as f:
                    f.write(r.content)
                winsound.PlaySound(p, winsound.SND_FILENAME)
                try:
                    os.unlink(p)
                except Exception:
                    pass
        except Exception as e:
            sys.stderr.write(f"[voice] TTS error: {e}\n")
