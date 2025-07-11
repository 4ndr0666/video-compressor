#!/usr/bin/env python3
"""
src/download.py

Robust FFmpeg downloader + installer thread.
"""

import os
import requests
import shutil
import zipfile

from PyQt6.QtCore import QThread, pyqtSignal

import globals as g

# URL for FFmpeg build
FFMPEG_DL = (
    "https://github.com/BtbN/FFmpeg-Builds"
    "/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
)

class DownloadThread(QThread):
    update_log      = pyqtSignal(str)
    update_progress = pyqtSignal(int)
    installed       = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # Ensure bin directory exists
        os.makedirs(g.bin_dir, exist_ok=True)

    def run(self) -> None:
        self.update_log.emit("Starting FFmpeg download…")
        zip_path = self._download_ffmpeg()
        if not zip_path:
            return

        self.update_log.emit("Installing FFmpeg…")
        if self._install_ffmpeg(zip_path):
            g.ffmpeg_installed = True
            self.installed.emit()
            self.update_log.emit("FFmpeg is ready.")
        else:
            g.ffmpeg_installed = False
            self.update_log.emit("FFmpeg installation failed.")

    def _download_ffmpeg(self) -> str | None:
        """Download the ZIP, emit progress, return path or None on failure."""
        local_zip = os.path.join(g.bin_dir, "ffmpeg.zip")
        try:
            with requests.get(FFMPEG_DL, stream=True, timeout=15) as r:
                r.raise_for_status()
                total = int(r.headers.get("Content-Length", 0))
                downloaded = 0
                with open(local_zip, "wb") as out:
                    for chunk in r.iter_content(chunk_size=8192):
                        if not chunk:
                            continue
                        out.write(chunk)
                        downloaded += len(chunk)
                        percent = int(downloaded * 100 / total) if total else 0
                        self.update_progress.emit(percent)
            self.update_log.emit("Download complete.")
            return local_zip
        except requests.RequestException as e:
            self.update_log.emit(f"Download error: {e}")
            return None

    def _install_ffmpeg(self, zip_path: str) -> bool:
        """Extract the ZIP into bin_dir, move executables, clean up, and return success."""
        try:
            with zipfile.ZipFile(zip_path, "r") as archive:
                archive.extractall(g.bin_dir)

            # Move or skip any pre-existing executables
            for exe in ("ffmpeg.exe", "ffprobe.exe"):
                src = os.path.join(g.bin_dir, exe)
                if os.path.isfile(src):
                    try:
                        # Overwrites only if missing
                        shutil.move(src, os.path.join(g.bin_dir, exe))
                    except shutil.Error:
                        self.update_log.emit(f"Skipped moving {exe}: already exists.")

            self.update_log.emit("Installation complete.")
            return True

        except (zipfile.BadZipFile, OSError) as e:
            self.update_log.emit(f"Installation error: {e}")
            return False

        finally:
            # Always clean up the zip file
            try:
                os.remove(zip_path)
            except OSError:
                pass
