# Linux 无显卡部署：AI Video Note

目标主机：`192.168.1.50`（局域网地址）。在准备材料时，这台主机可响应 ping，TCP 22 可连接；TCP 8765 尚未开放或未运行该服务。端口连通只证明网络可达，尚未核实主机 CPU、内存、磁盘、系统发行版和 Python 版本。

上游项目的 [README](https://github.com/hehe1885/AI-Video-Note#readme) 说明 CPU 转写受支持，并给出其他系统源码运行入口。其默认服务监听 `127.0.0.1`，不直接开放给局域网。

## 在 Linux 主机安装

以下命令在 `192.168.1.50` 的终端执行。需要 Python 3.11–3.14、`git`、可用的网络与足够磁盘空间；首次依赖与模型下载需要联网。

```bash
git clone https://github.com/hehe1885/AI-Video-Note.git
cd AI-Video-Note
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt
python launcher.py --console
```

程序界面内下载语音识别模型，设备选 CPU。先用 `base` 或 `small` 跑一段短视频，确认转写、字幕和导出正常，再决定是否使用 `medium`。生成笔记还需另行配置 AI 通道或使用可用的 Agent 客户端；本地语音识别本身不要求笔记大模型 API Key。

## 从自己的电脑访问

保留服务仅监听 Linux 主机的 `127.0.0.1`。在你的电脑另开终端，通过 SSH 转发端口：

```bash
ssh -L 8765:127.0.0.1:8765 <Linux用户名>@192.168.1.50
```

隧道保持连接时，在本机浏览器打开 `http://127.0.0.1:8765`。若本机 8765 已被占用，改用 `ssh -L 18765:127.0.0.1:8765 ...`，浏览器访问 `http://127.0.0.1:18765`。服务实际端口如有变化，以 Linux 终端输出为准，并同步替换转发命令的右侧端口。

这份步骤还没有在目标 Linux 主机上执行；只有该主机的登录方式和资源信息确认后，才能判断实际转写速度与长期运行稳定性。
