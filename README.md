# 会议转写与 AI Video Note 部署记录

本仓库保存 2026 年 11 月 13 日、20 日两场会议的文字成果，以及在无显卡 Linux 主机上复现本地转写的方法。原始 MP4、模型权重、账号与 API Key 不在仓库中。

## 这次是怎么转写的

使用开源项目 [AI Video Note](https://github.com/hehe1885/AI-Video-Note) 读取本地 MP4 音轨；录音没有可直接使用的字幕，因此采用本地 Whisper `medium` 模型进行中文语音识别。实际运行设备为 NVIDIA GeForce GTX 1660，后端为 Vulkan / float16。11 月 20 日录音约 10 分 19 秒，11 月 13 日录音约 10 分 43 秒；之后对明显同音字、重复识别及关键术语进行了人工语境核对，再整理会议纪要和录像截图。

11 月 20 日的 SRT 是**语境校订稿**，部分口语被压缩为易读句子；11 月 13 日的 SRT 是**自动识别初稿**，仅做极少量确定性订正，不能当作逐字人工听校稿。两份材料均应以原录音为最终依据。

## 文件

- `meeting/2026-11-20/meeting-minutes.pdf`：以 11 月 20 日会议为主，结合 11 月 13 日会议及墨刀原型补充“小手机”议题，含关键画面与行动项。
- `meeting/2026-11-20/subtitles.srt`、`subtitles.txt`：11 月 20 日时间轴字幕校订稿。
- `meeting/2026-11-13/transcript-asr.srt`、`transcript-asr.txt`：11 月 13 日时间轴自动识别初稿。
- `meeting/small-phone-cross-meeting.md`：两次会议中“小手机”议题的证据与结论。
- `tools/transcribe_cpu.py`：在没有显卡的主机上直接生成 SRT 与 TXT 的最小转写脚本。
- `deploy/linux-cpu.md`：部署 AI Video Note 到 Linux 主机并通过 SSH 隧道访问的步骤。

## 无显卡转写

AI Video Note 支持 CPU 识别，因此无显卡机器可以运行；速度由 CPU、内存和所选模型决定。先用 `base` 或 `small` 模型验证，`medium` 的 CPU 耗时会明显增加。下面的独立脚本采用 `faster-whisper` 的 CPU 实现；它与本次 Vulkan 转写不是同一运行后端，输出可能略有差异：

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install 'faster-whisper>=1.2,<2'
python tools/transcribe_cpu.py /path/to/meeting.mp4 --model small --out-dir output
```

网页服务的安装与访问方式见 [`deploy/linux-cpu.md`](deploy/linux-cpu.md)。
