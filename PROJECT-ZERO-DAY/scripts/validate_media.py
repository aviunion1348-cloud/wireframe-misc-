#!/usr/bin/env python3
"""Reproducible FFprobe/FFmpeg checks for a rendered MP4.

This measures a media file; it does not approve acting, cinematography, emotion,
photorealism, dialogue performance, or a complete human playback pass.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], *, capture: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=False, text=True,
                          stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
                          stderr=subprocess.PIPE if capture else subprocess.DEVNULL)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("media", type=Path)
    ap.add_argument("--ffprobe", default="ffprobe")
    ap.add_argument("--ffmpeg", default="ffmpeg")
    ap.add_argument("--expect-seconds", type=float, default=60.0)
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--active-height", type=int, default=536,
                    help="Letterbox-excluded picture height for active-picture black detection")
    ap.add_argument("--matte-top", type=int, default=92)
    ap.add_argument("--black-duration", type=float, default=.25)
    ap.add_argument("--report", type=Path, help="Optional JSON report output")
    args = ap.parse_args()

    path = args.media.resolve()
    errors: list[str] = []
    if not path.is_file():
        print(f"FAIL: media file does not exist: {path}", file=sys.stderr)
        return 2
    size = path.stat().st_size
    if size <= 0:
        print("FAIL: media file is empty", file=sys.stderr)
        return 2

    probe = run([args.ffprobe, "-v", "error", "-show_entries",
                 "format=duration,size,format_name,bit_rate:stream=index,codec_type,codec_name,profile,width,height,pix_fmt,r_frame_rate,avg_frame_rate,start_time,duration,nb_frames,sample_rate,channels,channel_layout,bit_rate",
                 "-of", "json", str(path)])
    if probe.returncode:
        print(probe.stderr, file=sys.stderr)
        return 2
    meta = json.loads(probe.stdout)
    fmt = meta.get("format", {})
    streams = meta.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    if video is None:
        errors.append("missing video stream")
    if audio is None:
        errors.append("missing audio stream")

    duration = float(fmt.get("duration", 0.0))
    if abs(duration - args.expect_seconds) > 0.05:
        errors.append(f"container duration {duration:.6f}s != expected {args.expect_seconds:.3f}s")
    if video:
        if (video.get("width"), video.get("height")) != (args.width, args.height):
            errors.append(f"video raster {video.get('width')}x{video.get('height')} != {args.width}x{args.height}")
        expected_rate = f"{args.fps}/1"
        if video.get("r_frame_rate") != expected_rate or video.get("avg_frame_rate") != expected_rate:
            errors.append(f"frame rate nominal/average is {video.get('r_frame_rate')}/{video.get('avg_frame_rate')}, expected {expected_rate}")
        if video.get("codec_name") != "h264":
            errors.append(f"expected H.264 video, found {video.get('codec_name')}")
        if video.get("start_time") not in (None, "0.000000", "0.000000"):
            errors.append(f"video stream starts at {video.get('start_time')}s, not zero")
    if audio:
        if audio.get("codec_name") != "aac":
            errors.append(f"expected AAC audio, found {audio.get('codec_name')}")
        if int(audio.get("sample_rate", 0)) != 48000 or int(audio.get("channels", 0)) != 2:
            errors.append(f"expected 48 kHz stereo audio, found {audio.get('sample_rate')} Hz / {audio.get('channels')} channels")
        astart, adur = float(audio.get("start_time", 0.0)), float(audio.get("duration", 0.0))
        if abs(astart) > .02 or abs(adur - args.expect_seconds) > .05:
            errors.append(f"audio timing start={astart:.3f}s duration={adur:.3f}s does not match video target")

    decode = run([args.ffmpeg, "-v", "error", "-i", str(path), "-f", "null", "-"])
    decode_ok = decode.returncode == 0
    if not decode_ok:
        errors.append(f"full decode failed: {decode.stderr[-1500:]}")

    hashes = run([args.ffmpeg, "-v", "error", "-i", str(path), "-map", "0:v:0", "-f", "framemd5", "-"])
    if hashes.returncode:
        errors.append(f"framemd5 failed: {hashes.stderr[-1000:]}")
        frame_count, duplicate_pairs = 0, None
    else:
        digests = [line.split(",")[-1].strip() for line in hashes.stdout.splitlines()
                   if line.strip() and not line.startswith("#")]
        frame_count = len(digests)
        duplicate_pairs = sum(a == b for a, b in zip(digests, digests[1:]))
        expected_frames = int(round(args.expect_seconds * args.fps))
        if frame_count != expected_frames:
            errors.append(f"decoded frame count {frame_count} != {expected_frames}")
        if duplicate_pairs:
            errors.append(f"found {duplicate_pairs} consecutive identical frame pairs")

    black = run([args.ffmpeg, "-hide_banner", "-loglevel", "info", "-i", str(path),
                 "-vf", f"crop={args.width}:{args.active_height}:0:{args.matte_top},blackdetect=d={args.black_duration}:pix_th=0.10",
                 "-an", "-f", "null", "-"])
    black_intervals = re.findall(r"black_start:([0-9.]+) black_end:([0-9.]+)", black.stderr)
    if black.returncode:
        errors.append(f"active-picture black-gap analysis failed: {black.stderr[-1000:]}")
    if black_intervals:
        errors.append(f"detected active-picture black interval(s): {black_intervals}")

    volume = run([args.ffmpeg, "-hide_banner", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"])
    mean_match = re.search(r"mean_volume:\s*(-?[0-9.]+)\s*dB", volume.stderr)
    peak_match = re.search(r"max_volume:\s*(-?[0-9.]+)\s*dB", volume.stderr)
    mean_db = float(mean_match.group(1)) if mean_match else None
    peak_db = float(peak_match.group(1)) if peak_match else None
    if volume.returncode or mean_db is None or peak_db is None:
        errors.append("could not measure audio mean/peak level")
    elif peak_db >= 0.0:
        errors.append(f"audio peak is clipping/non-negative ({peak_db} dBFS)")

    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    report = {
        "status": "TECHNICAL PASS" if not errors else "FAIL",
        "file": str(path),
        "size_bytes": size,
        "sha256": digest,
        "container": fmt.get("format_name"),
        "container_duration_seconds": duration,
        "video": video,
        "audio": audio,
        "full_decode_passed": decode_ok,
        "decoded_video_frames": frame_count,
        "consecutive_identical_frame_pairs": duplicate_pairs,
        "active_picture_black_intervals": black_intervals,
        "audio_mean_volume_db": mean_db,
        "audio_peak_dbfs": peak_db,
        "limitations": ["Technical inspection only; no human full playback or artistic approval is implied."],
        "errors": errors,
    }
    result = json.dumps(report, indent=2, ensure_ascii=False)
    print(result)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(result + "\n", encoding="utf-8")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
