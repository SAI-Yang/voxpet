<p align="center">
  <img src="res/role/ChrisKitty/action/stand_0.png" width="64" alt="VoxPet">
</p>

<h1 align="center">VoxPet 🐱🎤</h1>

<p align="center">
  <strong>桌面宠物 + AI 语音助手</strong>
</p>

<p align="center">
  <a href="https://github.com/SAI-Yang/voxpet/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-GPLv3-blue.svg" alt="License">
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.12%2B-blue" alt="Python">
  </a>
  <a href="https://github.com/SAI-Yang/voxpet">
    <img src="https://img.shields.io/github/stars/SAI-Yang/voxpet?style=social" alt="Stars">
  </a>
</p>

<p align="center">
  基于 <a href="https://github.com/ChaozhongLiu/DyberPet">DyberPet</a> 二次开发，融合语音交互管线。<br>
  <b>右键点宠物 → 说话 → AI 回复 → 语音播报</b>，宠物全程冒泡反馈状态。
</p>

---

## 📸 预览

<!-- 待补充：gif 或截图 -->
<details>
<summary>点击展开截图</summary>

| 宠物待机 | 录音中 | AI 回复 |
|---------|--------|---------|
| ![](docs/preview_img/lnl.png) | <!-- 待补充 --> | <!-- 待补充 --> |

</details>

---

## ✨ 特性

### 🎮 桌面宠物

| 功能 | 说明 |
|------|------|
| 🐈 **精灵动画** | 多角色切换（Kitty / ChrisKitty / 派蒙等），每角色有独立的动作帧（站立、行走、睡觉、拖拽、掉落、自定义） |
| 🧠 **行为树** | HP 饱食度 + 好感度双系统，宠物根据状态自动切换动画（饥饿时无精打采，饱食时活泼） |
| 🍅 **番茄钟** | 内置番茄工作法 + 专注计时器，宠物到点提醒 |
| 🎒 **背包系统** | 物品道具（食物/收藏品/装饰品），可喂食、装备、出售 |
| 💬 **气泡互动** | 宠物冒泡提示状态变化，支持自定义对话树 |
| 📊 **仪表盘** | 可视化面板：状态监控、物品管理、任务列表、动画编辑 |

### 🎤 AI 语音助手

| 功能 | 说明 |
|------|------|
| 🎙️ **一键录音** | 右键菜单触发，点一次录音，再点停止 |
| 🧠 **语音识别** | Faster-Whisper tiny 本地运行，纯 CPU 推理，不联网 |
| 🤖 **大模型对话** | 接入 DeepSeek API（兼容 OpenAI/Anthropic 格式），回复简洁 |
| 🔊 **语音合成** | IndexTTS 云端声音克隆，音色自然 |
| 💭 **可视化反馈** | 录音 → 识别 → 思考 → 播报，每步宠物冒泡提示 |

---

## 🚀 快速开始

### 环境要求

| 项目 | 要求 |
|------|------|
| OS | Windows 10/11（语音播放依赖 `winsound`） |
| Python | 3.12（推荐）/ 3.11 / 3.13 |
| 麦克风 | 可用录音设备 |
| 显存 | 无要求（Whisper tiny 纯 CPU 运行） |

> **注意**：Python 3.14 目前不兼容 PySide6，请使用 Python 3.12。

### 安装步骤

```bash
# 1. 克隆
git clone https://github.com/SAI-Yang/voxpet.git
cd voxpet

# 2. 创建虚拟环境（必须用 Python 3.12）
python -m venv venv

# 3. 激活
venv\Scripts\activate

# 4. 安装依赖
pip install PySide6 PySide6-Fluent-Widgets apscheduler tendo pynput
pip install sounddevice numpy httpx faster-whisper
```

### 运行

```bash
python run_DyberPet.py
```

桌面出现宠物后，**右键点击宠物** → 菜单选择 **🎤 Voice Assistant** → 开始录音，再点一次停止。

---

## 🎯 使用指南

### 宠物基础操作

| 操作 | 效果 |
|------|------|
| 🖱️ 左键拖拽 | 移动宠物位置 |
| 🖱️ 右键 | 打开功能菜单 |
| 🔄 双击 | 抚摸宠物（触发互动） |
| ❌ 右键 → Exit | 退出程序 |

### 右键菜单

```
┌─ 宠物名 ─────────────┐
│  Level N              │
│  Satiety [████░░]     │
│  Favor    [██████]    │
├───────────────────────┤
│  📊 Dashboard         │ ← 打开控制面板
│  ⚙️ System            │ ← 系统设置
├───────────────────────┤
│  🎤 Voice Assistant   │ ← 语音助手开关
├───────────────────────┤
│  ▶️ Select Action     │ ← 让宠物表演动作
│  📞 Call Partner      │ ← 召唤副宠
│  🔄 Change Character  │ ← 切换角色
├───────────────────────┤
│  ⏻ Exit               │ ← 退出
└───────────────────────┘
```

### 语音助手使用流程

```
1. 右键宠物 → 点击 "🎤 Voice Assistant"
2. 宠物冒泡 "🎤 录音中..." → 开始说话
3. 再次点击菜单项停止录音
4. 宠物依次显示：
   📝 识别中... → 显示文字
   🤖 思考中... → AI 回复
   ♫ 播放中... → TTS 语音播报
5. 回到待机状态
```

### 语音管线配置

复制配置模板（**不要**直接编辑原文件，它含敏感 API Key）：

```bash
cp config_voice.example.json config_voice.json
```

编辑 `config_voice.json`：

```json
{
  "api_chat": "http://127.0.0.1:8765/anthropic/messages",
  "api_key": "sk-your-key-here",
  "api_tts": "http://your-tts-server:6006/",
  "tts_voice": "your-voice.wav",
  "whisper_model_path": "~/.cache/faster-whisper/tiny-copy/",
  "system_prompt": "用简短的中文回答，不超过50字。"
}
```

该文件已加入 `.gitignore`，不会提交到仓库。

---

## 🏗️ 项目结构

```
voxpet/
├── run_DyberPet.py              # 🚀 入口：QApplication + 组件编排
├── DyberPet/
│   ├── DyberPet.py              # 🐱 宠物主窗口（QWidget + 右键菜单）
│   ├── voice_assistant.py       # 🎤 语音模块 ← 新增
│   ├── modules.py               # 🔄 动画/交互线程
│   ├── Notification.py          # 💬 通知/气泡系统
│   ├── Accessory.py             # 💍 饰品/子宠物系统
│   ├── bubbleManager.py         # 🫧 气泡行为管理
│   ├── conf.py                  # ⚙️ 数据模型（PetData/ActData/ItemData）
│   ├── settings.py              # 🔧 全局配置
│   ├── utils.py                 # 🛠️ 工具函数
│   ├── custom_widgets.py        # 🎨 自定义 UI 组件
│   ├── custom_roundmenu.py      # 🌀 圆形菜单
│   ├── extra_windows.py         # 🪟 辅助窗口
│   ├── Dashboard/               # 📊 仪表盘面板
│   │   ├── DashboardUI.py
│   │   ├── statusUI.py          # 状态面板
│   │   ├── inventoryUI.py       # 背包
│   │   ├── shopUI.py            # 商店
│   │   ├── taskUI.py            # 任务/番茄钟
│   │   ├── animationUI.py       # 动画编辑
│   │   └── ...
│   ├── DyberSettings/           # ⚙️ 系统设置
│   │   ├── DyberControlPanel.py
│   │   ├── PetCardUI.py
│   │   └── ...
│   └── HideDock/                # 🪄 Dock 隐藏工具
├── res/
│   ├── role/                    # 角色资源
│   │   ├── Kitty/               # 经典猫
│   │   ├── ChrisKitty/          # Chris 猫（默认）
│   │   └── sys/                 # 系统动画
│   ├── pet/                     # 副宠资源（派蒙等）
│   ├── items/                   # 物品道具
│   ├── icons/                   # UI 图标
│   ├── sounds/                  # 音效
│   └── language/                # 多语言
├── docs/                        # 📖 文档
└── .gitignore
```

---

## 🧠 语音管线架构

```
┌─────────────────────────────────────────────────┐
│                 用户说话                         │
└──────────────────┬──────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────┐
│  sounddevice.InputStream  (16kHz, float32)       │
│  录音 → 音频分片暂存                             │
└──────────────────┬──────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────┐
│  Faster-Whisper tiny (本地 CPU, int8)            │
│  beam_size=5, language=zh                        │
│  → 中文文本                                      │
└──────────────────┬──────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────┐
│  DeepSeek API (deepseek-v4-flash)                │
│  System: "用简短的中文回答，不超过50字"           │
│  → AI 回复文本                                   │
└──────────────────┬──────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────┐
│  IndexTTS (云端声音克隆)                          │
│  音色: shaonv-isolated.wav                       │
│  → WAV 音频数据                                  │
└──────────────────┬──────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────┐
│  winsound.PlaySound  (Windows)                   │
│  播放 WAV → 用户听到回复                         │
└─────────────────────────────────────────────────┘

全程线程安全：录音线程 → 管线线程 → 主线程信号（Qt Signal）
```

### 模块设计

语音助手 `VoiceAssistant` 是一个独立 `QObject`：

```
VoiceAssistant
├── show_bubble Signal(dict, int, int)      → 通知气泡系统
├── show_notification Signal(str, str)      → 宠物通知系统
├── toggle_recording()                      → 菜单触发入口
├── _record_thread()                        → sounddevice 录音线程
├── _transcribe()                           → Whisper 转文字
├── _ask_ai()                               → DeepSeek API
└── _play_tts()                             → IndexTTS + winsound
```

通过 Qt Signal/Slot 机制与宠物系统解耦，不修改原有代码结构。

---

## 🐱 更换宠物角色

VoxPet 内置三个角色：**Kitty**（经典猫）、**ChrisKitty**（默认）、**派蒙**。

右键菜单 → **Change Character** 切换。

### 添加新角色

1. 在 `res/role/` 下创建 `<角色名>/` 目录
2. 准备动作帧 PNG（透明背景）
3. 编写 `pet_conf.json`（配置尺寸、动作帧索引、默认动画）
4. 编写 `act_conf.json`（定义动画名称、类型、概率、好感度解锁条件）
5. 重启即可在菜单中看到

参考现有角色的配置格式。

---

## 🔧 常见问题

### Q: 启动后 `Shiboken::Conversions` 警告

无害的 Qt 内部类型转换警告，不影响任何功能。

### Q: Python 3.14 安装 PySide6 失败

PySide6 暂不支持 Python 3.14。请安装 Python 3.12：

```bash
# 下载 Python 3.12
https://www.python.org/downloads/release/python-3129/

# 创建虚拟环境
C:\Users\...\Python312\python.exe -m venv voxpet\venv
```

### Q: `tendo.singleton.SingleInstance` 阻止启动

如果之前异常退出，删掉 `data/lock` 文件：

```bash
rm voxpet/data/lock
```

### Q: 麦克风没声音

检查系统麦克风权限，确保 `sounddevice` 能检测到设备：

```python
python -c "import sounddevice; print(sounddevice.query_devices())"
```

### Q: 语音回复太慢

- Whisper tiny 首次加载模型需几秒，后续复用缓存
- DeepSeek API 响应时间取决于网络
- IndexTTS 部署在 Compshare 服务器，首次请求有冷启动延迟

---

## 📦 依赖清单

| 包 | 用途 | 安装大小 |
|----|------|---------|
| PySide6 | Qt 图形界面框架 | ~50 MB |
| PySide6-Fluent-Widgets | Fluent Design 组件库 | ~2 MB |
| apscheduler | 定时任务调度 | <1 MB |
| tendo | 单实例进程锁 | <1 MB |
| pynput | 全局热键/鼠标监听 | <1 MB |
| sounddevice | 音频录制 | ~1 MB |
| numpy | 音频数据处理 | ~20 MB |
| httpx | HTTP 请求（API/TTS） | ~2 MB |
| faster-whisper | 本地语音识别 | ~140 MB（模型） |

---

## 📜 许可

GPL-3.0 — 继承自 [DyberPet](https://github.com/ChaozhongLiu/DyberPet)。

DyberPet 原作者：[@ChaozhongLiu](https://github.com/ChaozhongLiu)

---

## 🙏 鸣谢

- [DyberPet](https://github.com/ChaozhongLiu/DyberPet) — 原版桌面宠物框架
- [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper) — 本地语音识别
- [PySide6-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets) — Fluent Design 组件库
- [qfluentwidgets](https://qfluentwidgets.com/) — Qt Fluent Design 开源组件
- [IndexTTS](https://github.com/IndexTeam/IndexTTS) — 声音克隆 TTS
