"""Minimal local MP4/audio to SRT/TXT transcription with faster-whisper on CPU."""

from __future__ import annotations

import argparse
from pathlib import Path

from faster_whisper import WhisperModel


def stamp(seconds: float, *, srt: bool) -> str:
    total_ms = round(max(0.0, seconds) * 1000)
    hours, remainder = divmod(total_ms, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}{',' if srt else '.'}{millis:03d}"


def main() -> None:
    parser = argparse.ArgumentParser(description="使用 CPU 把本地音视频转为 SRT/TXT")
    parser.add_argument("media", type=Path, help="本地 MP4 或音频文件")
    parser.add_argument("--model", default="small", help="Whisper 模型，例如 base、small、medium")
    parser.add_argument("--language", default="zh", help="语言代码，中文为 zh")
    parser.add_argument("--out-dir", type=Path, default=Path("output"))
    args = parser.parse_args()

    if not args.media.is_file():
        parser.error(f"找不到文件：{args.media}")
    args.out_dir.mkdir(parents=True, exist_ok=True)

    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        str(args.media), language=args.language, vad_filter=True, beam_size=5
    )

    srt_lines: list[str] = []
    txt_lines = [f"来源：{args.media.name}", f"识别语言：{info.language}", ""]
    count = 0
    for count, segment in enumerate(segments, start=1):
        text = segment.text.strip()
        srt_lines.extend(
            [
                str(count),
                f"{stamp(segment.start, srt=True)} --> {stamp(segment.end, srt=True)}",
                text,
                "",
            ]
        )
        txt_lines.append(
            f"[{stamp(segment.start, srt=False)}–{stamp(segment.end, srt=False)}] {text}"
        )

    srt_path = args.out_dir / f"{args.media.stem}.srt"
    txt_path = args.out_dir / f"{args.media.stem}.txt"
    srt_path.write_text("\n".join(srt_lines), encoding="utf-8-sig")
    txt_path.write_text("\n".join(txt_lines) + "\n", encoding="utf-8-sig")
    print(f"{count} 段；SRT: {srt_path}；TXT: {txt_path}")


if __name__ == "__main__":
    main()
