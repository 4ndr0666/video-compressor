VERSION = "1.0.0"
TITLE = f"CVC v{VERSION}"
READY_TEXT = "Select your videos to get started."
DEFAULT_SETTINGS = {"target_size": 20.0, "use_gpu": False}

ffmpeg_path = "ffmpeg"
ffprobe_path = "ffprobe"
queue = []
completed = []
root_dir = ""
bin_dir = ""
output_dir = ""
res_dir = ""
ffmpeg_installed = False
compressing = False
