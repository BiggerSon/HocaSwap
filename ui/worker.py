import os
import re
import tempfile
import time
from typing import List, Optional

from PySide6.QtCore import QThread, Signal

from core.process_runner import ProcessRunner
from core.video_utils import (
    VideoUtilsError, cleanup_temp_dir, concat_videos, get_video_duration,
    mux_audio_from_source, split_video_into_chunks,
)

QUALITY_MAP = {"Hizli": "fast", "Dengeli": "balanced", "Yuksek": "high"}

from config import FACEFUSION_PYTHON, FACEFUSION_SCRIPT, FACEFUSION_CWD

def build_cli_command(
    image_paths: List[str], chunk_in: str, chunk_out: str,
    quality_value: str, prompt_text: str, face_mode: str,
) -> List[str]:
    
    cmd = [
        FACEFUSION_PYTHON, FACEFUSION_SCRIPT, "headless-run",
        "-s", *image_paths,
        "-t", chunk_in,
        "-o", chunk_out,
        "--execution-providers", "directml",
        "--execution-thread-count", "1", 
        "--video-memory-strategy", "tolerant",
        "--face-selector-mode", face_mode,
        "--face-swapper-model", "inswapper_128",
        "--output-video-quality", "100",
    ]

    processors = ["face_swapper"]
    if quality_value in ("balanced", "high"):
        processors.append("face_enhancer")

    p_low = prompt_text.lower() if prompt_text else ""
    age_direction = None
    if "yaşlandır" in p_low or "yaslandir" in p_low:
        age_direction = "50"
    elif "gençleştir" in p_low or "genclestir" in p_low:
        age_direction = "-50"
    
    if age_direction:
        processors.append("age_modifier")

    cmd.extend(["--processors", *processors])

    if quality_value == "balanced":
        cmd.extend([
            "--face-enhancer-model", "gfpgan_1.4", 
            "--face-swapper-pixel-boost", "256x256"
        ])
    elif quality_value == "high":
        cmd.extend([
            "--face-enhancer-model", "codeformer",
            "--face-enhancer-blend", "100",
            "--face-enhancer-weight", "0.5",
            "--face-swapper-pixel-boost", "512x512" 
        ])
        
    cmd.extend(["--face-detector-margin", "20", "0", "0", "0"])

    if age_direction:
        cmd.extend(["--age-modifier-model", "styleganex_age", "--age-modifier-direction", age_direction])

    return cmd

def build_extra_vf(prompt_text: str) -> Optional[str]:
    p_low = prompt_text.lower() if prompt_text else ""
    filters = []

    if "esmer" in p_low or "bronz" in p_low:
        filters.append("eq=brightness=-0.05:saturation=1.2:contrast=1.1")
    if "siyah beyaz" in p_low or "siyahbeyaz" in p_low:
        filters.append("hue=s=0")
    if "ayna" in p_low:
        filters.append("hflip")
    if "sakal" in p_low or "saç" in p_low or "sac" in p_low:
        if "siyah" in p_low or "koyu" in p_low:
            filters.append("curves=all='0/0 0.5/0.35 1/1',eq=contrast=1.2:saturation=0.8")
        elif "gri" in p_low or "beyaz" in p_low:
            filters.append("eq=saturation=0:brightness=0.1:contrast=1.1")

    return ",".join(filters) if filters else None

class VideoProcessingWorker(QThread):
    log_signal = Signal(str)
    progress_signal = Signal(int)
    status_signal = Signal(str)
    finished_signal = Signal(bool, str)

    def __init__(self, image_paths, video_path, audio_path, quality_label, output_path, prompt_text="", face_mode="many", chunk_seconds=30, parent=None):
        super().__init__(parent)
        self.image_paths = image_paths
        self.video_path = video_path
        self.audio_path = audio_path
        self.quality_label = quality_label
        self.output_path = output_path
        self.prompt_text = prompt_text
        self.face_mode = face_mode
        self.chunk_seconds = chunk_seconds

        self._cancel_requested = False
        self._current_runner: Optional[ProcessRunner] = None
        self._temp_dir: Optional[str] = None
        self._start_time = 0.0

    def request_cancel(self):
        self._cancel_requested = True
        if self._current_runner: self._current_runner.cancel()

    def _should_cancel(self) -> bool: return self._cancel_requested

    def run(self):
        try: self._run_pipeline()
        except VideoUtilsError as exc: self.finished_signal.emit(False, str(exc))
        except Exception as exc: self.finished_signal.emit(False, f"Beklenmeyen hata: {exc}")
        finally:
            if self._temp_dir: cleanup_temp_dir(self._temp_dir, on_log=self.log_signal.emit)

    def _run_pipeline(self):
        self._start_time = time.time()
        self.status_signal.emit("Video analiz ediliyor...")
        get_video_duration(self.video_path)

        self._temp_dir = tempfile.mkdtemp(prefix="facefusion_wrapper_")
        chunks_dir = os.path.join(self._temp_dir, "chunks")
        processed_dir = os.path.join(self._temp_dir, "processed")
        os.makedirs(processed_dir, exist_ok=True)

        if self._check_cancel(): return

        self.status_signal.emit("Parçalara bölünüyor...")
        chunk_paths = split_video_into_chunks(self.video_path, chunks_dir, self.chunk_seconds, on_log=self.log_signal.emit)
        self.progress_signal.emit(5)

        quality_value = QUALITY_MAP.get(self.quality_label, "balanced")
        processed_chunk_paths: List[str] = []
        total_chunks = len(chunk_paths)

        for index, chunk_path in enumerate(chunk_paths, start=1):
            if self._check_cancel(): return

            chunk_name = os.path.basename(chunk_path)
            processed_chunk_path = os.path.join(processed_dir, f"processed_{chunk_name}")

            cmd = build_cli_command(self.image_paths, chunk_path, processed_chunk_path, quality_value, self.prompt_text, self.face_mode)

            def handle_stdout(line: str, idx=index):
                self.log_signal.emit(f"[{idx}/{total_chunks}] {line}")
                match = re.search(r"processing:\s+(\d+)%", line)
                if not match: return
                chunk_fraction = int(match.group(1)) / 100.0
                overall_progress = 5 + int(((idx - 1 + chunk_fraction) / total_chunks) * 85)
                overall_progress = max(0, min(100, overall_progress))
                self.progress_signal.emit(overall_progress)

                elapsed = time.time() - self._start_time
                work_done = max(overall_progress - 5, 1) / 85.0 
                if work_done > 0:
                    eta_seconds = max(0, (elapsed / work_done) - elapsed)
                    minutes, seconds = divmod(int(eta_seconds), 60)
                    self.status_signal.emit(f"İşleniyor | Kalan: {minutes:02d}:{seconds:02d} | %{overall_progress}")

            self._current_runner = ProcessRunner()
            result = self._current_runner.run(
                cmd, cwd=FACEFUSION_CWD, env=dict(os.environ, PYTHONUNBUFFERED="1"),
                on_line=handle_stdout, on_stderr_line=lambda line, i=index: self.log_signal.emit(f"[{i}/{total_chunks}] {line}"),
                should_cancel=self._should_cancel,
            )
            self._current_runner = None

            if self._cancel_requested: return

            if not os.path.exists(processed_chunk_path):
                self.finished_signal.emit(False, f"FaceFusion çıktı üretmedi:\n{result.stderr_text}")
                return

            processed_chunk_paths.append(processed_chunk_path)
            self.progress_signal.emit(5 + int((index / total_chunks) * 85))

        if self._check_cancel(): return

        self.status_signal.emit("Birleştiriliyor | %95")
        merged_path = os.path.join(self._temp_dir, "merged.mp4")
        concat_videos(processed_chunk_paths, merged_path, on_log=self.log_signal.emit)

        self.status_signal.emit("Ses ve filtreler uygulanıyor | %98")
        extra_vf = build_extra_vf(self.prompt_text)
        audio_source = self.audio_path if self.audio_path and os.path.isfile(self.audio_path) else self.video_path

        mux_audio_from_source(
            processed_video_path=merged_path, original_source_path=audio_source,
            output_path=self.output_path, extra_vf=extra_vf, on_log=self.log_signal.emit,
        )

        self.progress_signal.emit(100)
        self.status_signal.emit("Tamamlandı | %100")
        self.finished_signal.emit(True, self.output_path)

    def _check_cancel(self) -> bool:
        if self._cancel_requested:
            self.finished_signal.emit(False, "İptal edildi.")
            return True
        return False