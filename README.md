# VoxPet 🐱🎤

**桌面宠物 + AI 语音助手** — 基于 [DyberPet](https://github.com/ChaozhongLiu/DyberPet) 二次开发，融合语音交互管线。

右键点宠物 → 说话 → Whisper 转文字 → DeepSeek 回复 → TTS 播报，宠物全程冒泡反馈状态。

## 特性

- **桌面宠物** — 精灵动画、行为树、HP/好感度系统、番茄钟、物品背包
- **AI 语音助手** — 点击录音，松开即走完语音识别 → 大模型 → 语音合成全链路
- **可视化反馈** — 录音/识别/思考/播放各阶段宠物都有状态提示
- **低侵入** — 语音模块作为独立 QObject，不破坏原有宠物系统
- **纯本地录音** — Faster-Whisper tiny 本地运行，音频不经过第三方

## 快速开始

### 环境要求

- Windows 10/11（语音播放依赖 `winsound`）
- Python 3.12
- 麦克风

### 安装

```bash
git clone https://github.com/YOUR_USERNAME/voxpet.git
cd voxpet

python -m venv venv
venv\Scripts\activate

pip install PySide6 PySide6-Fluent-Widgets apscheduler tendo pynput
pip install sounddevice numpy httpx faster-whisper
```

### 运行

```bash
python run_DyberPet.py
```

右键点宠物 → **🎤 Voice Assistant** → 开始录音，再点一次停止。

### 语音管线配置

编辑 `DyberPet/voice_assistant.py` 头部：

```python
API_CHAT = "http://127.0.0.1:8765/anthropic/messages"  # LLM API 代理地址
API_KEY = "sk-xxx"                                       # API Key
API_TTS = "http://117.50.248.152:6006/"                  # TTS 服务地址
TTS_VOICE = "shaonv-isolated.wav"                        # 音色文件
```

Whisper 模型路径：`~/.cache/faster-whisper/tiny-copy/`

## 项目结构

```
voxpet/
├── run_DyberPet.py          # 入口
├── DyberPet/
│   ├── DyberPet.py          # 宠物主窗口
│   ├── voice_assistant.py   # 语音模块 ← 新增
│   ├── modules.py           # 动画/交互模块
│   ├── Notification.py      # 通知/气泡系统
│   ├── Accessory.py         # 饰品/子宠物系统
│   ├── settings.py          # 全局配置
│   └── ...
├── res/                     # 资源文件（角色动作帧、图标）
└── docs/                    # 开发文档
```

## 语音管线架构

```
麦克风 → sounddevice 录音
              ↓
      Faster-Whisper (tiny, 本地 CPU)
              ↓
      DeepSeek API (deepseek-v4-flash)
              ↓
      IndexTTS (云端声音克隆)
              ↓
      winsound 播放 WAV
```

## 鸣谢

- [DyberPet](https://github.com/ChaozhongLiu/DyberPet) — 原版桌面宠物框架
- [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper) — 本地语音识别
- [PySide6-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets) — Fluent Design 组件库

## 许可

GPL-3.0（继承自 DyberPet）
