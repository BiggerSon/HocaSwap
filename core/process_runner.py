import subprocess
import sys
import threading
from typing import Callable, List, Optional


class ProcessResult:
    def __init__(self, return_code: int, stdout_lines: List[str], stderr_lines: List[str]):
        self.return_code = return_code
        self.stdout_lines = stdout_lines
        self.stderr_lines = stderr_lines

    @property
    def success(self) -> bool:
        return self.return_code == 0

    @property
    def stderr_text(self) -> str:
        return "\n".join(self.stderr_lines)


class ProcessRunner:
    def __init__(self):
        self._process: Optional[subprocess.Popen] = None
        self._lock = threading.Lock()
        self._cancelled = False

    def run(
        self,
        cmd: List[str],
        on_line: Optional[Callable[[str], None]] = None,
        on_stderr_line: Optional[Callable[[str], None]] = None,
        should_cancel: Optional[Callable[[], bool]] = None,
        cwd: Optional[str] = None,
        env: Optional[dict] = None,
    ) -> ProcessResult:
        creationflags = 0
        if sys.platform == "win32":
            creationflags = subprocess.CREATE_NO_WINDOW

        with self._lock:
            self._cancelled = False
            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
                cwd=cwd,
                env=env,
                creationflags=creationflags,
            )

        process = self._process
        stdout_lines: List[str] = []
        stderr_lines: List[str] = []

        def _read_stdout():
            assert process.stdout is not None
            for line in iter(process.stdout.readline, ""):
                if not line:
                    break
                clean = line.rstrip("\n")
                stdout_lines.append(clean)
                if on_line:
                    on_line(clean)
            try:
                process.stdout.close()
            except Exception:
                pass

        def _read_stderr():
            assert process.stderr is not None
            for line in iter(process.stderr.readline, ""):
                if not line:
                    break
                clean = line.rstrip("\n")
                stderr_lines.append(clean)
                if on_stderr_line:
                    on_stderr_line(clean)
            try:
                process.stderr.close()
            except Exception:
                pass

        stdout_thread = threading.Thread(target=_read_stdout, daemon=True)
        stderr_thread = threading.Thread(target=_read_stderr, daemon=True)
        stdout_thread.start()
        stderr_thread.start()

        while True:
            if should_cancel and should_cancel():
                self.cancel()
                break
            try:
                process.wait(timeout=0.2)
                break
            except subprocess.TimeoutExpired:
                continue

        stdout_thread.join(timeout=5)
        stderr_thread.join(timeout=5)

        return_code = process.returncode if process.returncode is not None else -1

        with self._lock:
            self._process = None

        return ProcessResult(return_code, stdout_lines, stderr_lines)

    def cancel(self):
        with self._lock:
            self._cancelled = True
            if self._process and self._process.poll() is None:
                try:
                    self._process.kill()
                except Exception:
                    pass