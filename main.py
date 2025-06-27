import json
import sys
import os
import subprocess
import psutil
import src.globals as g
from src.download import DownloadThread
from src.thread import CompressionThread
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QFileDialog,
    QLabel,
    QLineEdit,
    QCheckBox,
    QProgressBar,
)
from PyQt6.QtGui import QIcon
from src.styles import *


def load_settings():
    try:
        with open(os.path.join(g.res_dir, "settings.json"), "r") as f:
            return json.load(f)
    except Exception:
        return g.DEFAULT_SETTINGS


def save_settings(settings):
    with open(os.path.join(g.res_dir, "settings.json"), "w") as f:
        json.dump(settings, f)


def kill_ffmpeg():
    for proc in psutil.process_iter():
        if "ffmpeg" in proc.name():
            proc.kill()


def delete_bin():
    for root, dirs, files in os.walk(g.bin_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def notify(title, message):
    subprocess.Popen(["notify-send", title, message])


class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.verify_directories()
        self.settings = load_settings()
        self.setFixedSize(WINDOW.w, WINDOW.h)
        self.setWindowTitle(g.TITLE)
        icon_path = os.path.join(g.res_dir, "icon.ico")
        self.setWindowIcon(QIcon(icon_path))

        # Buttons
        self.button_select = QPushButton("Select Videos", self)
        self.button_compress = QPushButton("Compress", self)
        self.button_abort = QPushButton("Abort", self)

        for btn in [self.button_select, self.button_compress, self.button_abort]:
            btn.setEnabled(False)

        # Button geometry
        self.button_select.resize(SELECT_BUTTON.w, SELECT_BUTTON.h)
        self.button_select.move(SELECT_BUTTON.x, SELECT_BUTTON.y)
        self.button_select.clicked.connect(self.select_videos)

        self.button_compress.resize(COMPRESS_BUTTON.w, COMPRESS_BUTTON.h)
        self.button_compress.move(COMPRESS_BUTTON.x, COMPRESS_BUTTON.y)
        self.button_compress.clicked.connect(self.compress_videos)

        self.button_abort.resize(ABORT_BUTTON.w, ABORT_BUTTON.h)
        self.button_abort.move(ABORT_BUTTON.x, ABORT_BUTTON.y)
        self.button_abort.clicked.connect(self.abort_compression)

        # Labels, inputs, checkbox
        self.label_size = QLabel("Size (MB)", self)
        self.label_size.resize(FILE_SIZE_LABEL.w, FILE_SIZE_LABEL.h)
        self.label_size.move(FILE_SIZE_LABEL.x, FILE_SIZE_LABEL.y)

        self.edit_size = QLineEdit(str(self.settings["target_size"]), self)
        self.edit_size.resize(FILE_SIZE_ENTRY.w, FILE_SIZE_ENTRY.h)
        self.edit_size.move(FILE_SIZE_ENTRY.x, FILE_SIZE_ENTRY.y)
        self.edit_size.setEnabled(True)

        self.label_gpu = QLabel("Use GPU", self)
        self.label_gpu.resize(GPU_LABEL.w, GPU_LABEL.h)
        self.label_gpu.move(GPU_LABEL.x, GPU_LABEL.y)

        self.checkbox_gpu = QCheckBox(self)
        self.checkbox_gpu.resize(GPU_CHECKBOX.w, GPU_CHECKBOX.h)
        self.checkbox_gpu.move(GPU_CHECKBOX.x, GPU_CHECKBOX.y)
        self.checkbox_gpu.setChecked(self.settings["use_gpu"])

        self.label_log = QLabel(g.READY_TEXT, self)
        self.label_log.resize(LOG_AREA.w, LOG_AREA.h)
        self.label_log.move(LOG_AREA.x, LOG_AREA.y)
        self.label_log.setWordWrap(True)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.resize(PROGRESS_BAR.w, PROGRESS_BAR.h)
        self.progress_bar.move(PROGRESS_BAR.x, PROGRESS_BAR.y)
        self.progress_bar.setRange(0, 100)

        # Apply styles
        self.button_select.setStyleSheet(BUTTON_DISABLED_STYLE)
        self.button_compress.setStyleSheet(BUTTON_DISABLED_STYLE)
        self.button_abort.setStyleSheet(BUTTON_DISABLED_STYLE)
        self.label_size.setStyleSheet(LABEL_STYLE)
        self.edit_size.setStyleSheet(LINEEDIT_STYLE)
        self.label_gpu.setStyleSheet(LABEL_STYLE)
        self.checkbox_gpu.setStyleSheet(CHECKBOX_STYLE)
        self.label_log.setStyleSheet(LABEL_LOG_STYLE)
        self.progress_bar.setStyleSheet(PROGRESS_BAR_STYLE)

        self.download_thread = None
        self.compress_thread = None

        self.verify_ffmpeg()

    def closeEvent(self, event):
        self.settings["target_size"] = float(self.edit_size.text())
        self.settings["use_gpu"] = self.checkbox_gpu.isChecked()
        save_settings(self.settings)
        kill_ffmpeg()
        tmp_path = os.path.join(g.root_dir, "TEMP")
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        event.accept()

    def reset(self):
        g.compressing = False
        g.queue = []
        self.button_select.setEnabled(True)
        self.button_select.setStyleSheet(BUTTON_SELECT_STYLE)
        self.button_compress.setEnabled(False)
        self.button_compress.setStyleSheet(BUTTON_DISABLED_STYLE)
        self.button_abort.setEnabled(False)
        self.button_abort.setStyleSheet(BUTTON_DISABLED_STYLE)
        self.edit_size.setEnabled(True)
        self.update_log(g.READY_TEXT)
        self.update_progress(0)

    def verify_directories(self):
        if getattr(sys, "frozen", False):
            g.root_dir = os.path.dirname(sys.executable)
        else:
            g.root_dir = os.path.dirname(os.path.abspath(__file__))

        g.bin_dir = os.path.join(g.root_dir, "bin")
        os.makedirs(g.bin_dir, exist_ok=True)

        g.output_dir = os.path.join(g.root_dir, "output")
        os.makedirs(g.output_dir, exist_ok=True)

        g.res_dir = os.path.join(g.root_dir, "res")

    def verify_ffmpeg(self):
        ffmpeg = os.path.join(g.bin_dir, "ffmpeg")
        ffprobe = os.path.join(g.bin_dir, "ffprobe")

        if os.path.exists(ffmpeg) and os.path.exists(ffprobe):
            g.ffmpeg_installed = True
            g.ffmpeg_path = ffmpeg
            g.ffprobe_path = ffprobe
            self.reset()
        else:
            self.download_thread = DownloadThread()
            self.download_thread.installed.connect(self.installed)
            self.download_thread.update_log.connect(self.update_log)
            self.download_thread.update_progress.connect(self.update_progress)
            self.download_thread.start()

    def select_videos(self):
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Video Files",
            "",
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm *.m4v);;All Files (*)",
        )

        if file_paths:
            for path in file_paths:
                if path not in g.queue:
                    g.queue.append(path)

            self.button_compress.setEnabled(True)
            self.button_compress.setStyleSheet(BUTTON_COMPRESS_STYLE)
            self.update_log(f"Selected {len(g.queue)} video(s).")

    def compress_videos(self):
        g.compressing = True
        self.button_select.setEnabled(False)
        self.button_compress.setEnabled(False)
        self.button_abort.setEnabled(True)
        self.button_select.setStyleSheet(BUTTON_DISABLED_STYLE)
        self.button_compress.setStyleSheet(BUTTON_DISABLED_STYLE)
        self.button_abort.setStyleSheet(BUTTON_ABORT_STYLE)
        self.edit_size.setEnabled(False)

        self.compress_thread = CompressionThread(
            float(self.edit_size.text()), self.checkbox_gpu.isChecked()
        )
        self.compress_thread.completed.connect(self.completed)
        self.compress_thread.update_log.connect(self.update_log)
        self.compress_thread.update_progress.connect(self.update_progress)
        self.compress_thread.start()

    def abort_compression(self):
        kill_ffmpeg()
        self.completed(True)

    def update_log(self, text):
        self.label_log.setText(text)

    def update_progress(self, percent):
        self.progress_bar.setValue(percent)

    def installed(self):
        g.ffmpeg_installed = True
        g.ffmpeg_path = os.path.join(g.bin_dir, "ffmpeg")
        g.ffprobe_path = os.path.join(g.bin_dir, "ffprobe")
        self.reset()
        notify("FFmpeg installed!", "You can now compress your videos.")

    def completed(self, aborted=False):
        g.compressing = False
        self.compress_thread.terminate()
        self.reset()
        title = "Aborted!" if aborted else "Done!"
        msg = "Your videos are cooked!" if aborted else "Your videos are ready."
        notify(title, msg)
        if not aborted:
            subprocess.Popen(["xdg-open", g.output_dir])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
