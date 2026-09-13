# FL Studio Clone - 数字音频工作站 (DAW)

一个功能完整的 FL Studio 风格数字音频工作站，使用 Python (主)、C/C++、C# 构建。

## 功能特性

- **Channel Rack** - 音序器和通道管理
- **Piano Roll** - MIDI 音符编辑
- **Playlist** - 编排和模式管理
- **Mixer** - 混音和效果控制
- **Browser** - 文件浏览和预览
- **Transport Controls** - 播放、停止、录音控制

## 技术栈

- **Python (主)** - PyQt5 GUI 框架
- **C/C++** - 高性能音频引擎
- **C#** - MIDI 控制器和音序器

## 安装

```bash
pip install -r requirements.txt
```

## 运行

```bash
python main.py
```

## 快捷键

- `F5` - Channel Rack
- `F6` - Playlist
- `F7` - Piano Roll
- `F9` - Mixer
- `Ctrl+N` - 新建项目
- `Ctrl+S` - 保存
- `Ctrl+O` - 打开

## 编译 C++ 音频引擎

```bash
g++ -std=c++17 -O2 -shared -fPIC audio_engine.cpp -o audio_engine.so
```

## 编译 C# MIDI 控制器

```bash
csc /target:library MidiController.cs
```