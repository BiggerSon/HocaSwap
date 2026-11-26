import json
import os
import subprocess
import sys
from typing import Callable, List, Optional

from core.process_runner import ProcessRunner

FFMPEG_PATH = "ffmpeg"
FFPROBE_PATH = "ffprobe"

LogFn = Optional[Callable[[str], None]]


class VideoUtilsError(Exception):
    pass


def _creationflags():
    if sys.platform == "win32":
        return subprocess.CREATE_NO_WINDOW
    return 0


def get_video_duration(video_path: str) -> float:
    cmd = [
        FFPROBE_PATH, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json", video_path,
    ]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            creationflags=_creationflags(),
        )
    except FileNotFoundError:
        raise VideoUtilsError(
            "ffprobe bulunamadi. ffmpeg/ffprobe kurulu ve PATH'te oldugundan emin ol."
        )

    if result.returncode != 0:
        raise VideoUtilsError(f"ffprobe hata verdi: {result.stderr.strip()}")

    try:
        data = json.loads(result.stdout)
        return float(data["format"]["duration"])
    except (KeyError, ValueError, json.JSONDecodeError) as exc:
        raise VideoUtilsError(f"Video suresi okunamadi: {exc}")


def split_video_into_chunks(
    video_path: str,
    output_dir: str,
    chunk_seconds: int = 30,
    on_log: LogFn = None,
) -> List[str]:
    os.makedirs(output_dir, exist_ok=True)
    pattern = os.path.join(output_dir, "chunk_%04d.mp4")

    cmd = [
        FFMPEG_PATH, "-y",
        "-i", video_path,
        "-c", "copy",
        "-map", "0",
        "-f", "segment",
        "-segment_time", str(chunk_seconds),
        "-reset_timestamps", "1",
        pattern,
    ]

    runner = ProcessRunner()
    result = runner.run(cmd, on_stderr_line=on_log) 

    if not result.success:
        raise VideoUtilsError(f"Video parcalara bolunemedi (ffmpeg):\n{result.stderr_text}")

    chunk_files = sorted(
        f for f in os.listdir(output_dir)
        if f.startswith("chunk_") and f.endswith(".mp4")
    )
    if not chunk_files:
        raise VideoUtilsError("ffmpeg calisti ama hic parca dosyasi olusmadi.")

    return [os.path.join(output_dir, f) for f in chunk_files]


def concat_videos(
    chunk_paths: List[str],
    output_path: str,
    on_log: LogFn = None,
) -> str:
    if not chunk_paths:
        raise VideoUtilsError("Birlestirilecek parca listesi bos.")

    list_file_path = output_path + ".concat_list.txt"
    with open(list_file_path, "w", encoding="utf-8") as f:
        for path in chunk_paths:
            safe_path = os.path.abspath(path).replace("'", "'\\''")
            f.write(f"file '{safe_path}'\n")

    cmd = [
        FFMPEG_PATH, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file_path,
        "-c", "copy",
        output_path,
    ]

    runner = ProcessRunner()
    result = runner.run(cmd, on_stderr_line=on_log)

    try:
        os.remove(list_file_path)
    except OSError:
        pass

    if not result.success:
        raise VideoUtilsError(f"Parcalar birlestirilemedi (ffmpeg):\n{result.stderr_text}")

    return output_path


def mux_audio_from_source(
    processed_video_path: str,
    original_source_path: str,
    output_path: str,
    extra_vf: Optional[str] = None,
    on_log: LogFn = None,
) -> str:
    cmd = [
        FFMPEG_PATH, "-y",
        "-i", processed_video_path,
        "-i", original_source_path,
        "-map", "0:v:0",
        "-map", "1:a:0?",  
    ]

    if extra_vf:
        cmd.extend(["-vf", extra_vf, "-c:v", "libx264", "-preset", "fast", "-crf", "18"])
    else:
        cmd.extend(["-c:v", "copy"])

    cmd.extend(["-c:a", "aac", "-shortest", output_path])

    runner = ProcessRunner()
    result = runner.run(cmd, on_stderr_line=on_log)

    if not result.success:
        raise VideoUtilsError(f"Ses/filtre adimi basarisiz (ffmpeg):\n{result.stderr_text}")

    return output_path


def cleanup_temp_dir(temp_dir: str, on_log: LogFn = None) -> None:
    if not os.path.isdir(temp_dir):
        return
    for f in os.listdir(temp_dir):
        try:
            os.remove(os.path.join(temp_dir, f))
        except OSError as exc:
            if on_log:
                on_log(f"Uyari: gecici dosya silinemedi ({f}): {exc}")
    try:
        os.rmdir(temp_dir)
    except OSError:
        pass