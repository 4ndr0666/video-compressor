# 🎬 Video Compressor

A native Arch Linux application to compress videos to a target file size using an intuitive PyQt6 GUI with GPU acceleration support.

---

## ✨ Features

- 🎯 Target file size (in MB)
- 🗃️ Batch processing (queue support)
- ⚙️ GPU acceleration (NVIDIA NVENC, Intel QSV, AMD AMF)
- 🎚️ Two-pass encoding for optimal quality
- 🔔 `notify-send` native Linux notifications
- 🧠 Persistent user settings (target size & GPU toggle)
- 🧼 Clean, PEP8-compliant, pre-commit-enabled codebase

---

## 📦 Installation (Arch Linux)

```bash
# 1. Clone the repository
git clone https://github.com/4ndr0666/video-compressor.git
cd video-compressor

# 2. Create and activate virtualenv (recommended)
python -m venv .venv
source .venv/bin/activate

# 3. Install the package
make install
```

To remove the package:

```bash
make uninstall
```

> This automatically builds the wheel, installs the package, and links the executable system-wide via setuptools entry_points.

---

## 🚀 Running the App

Launch from terminal after install:

```bash
videocompressor
```

Or during development:

```bash
make run
```

---

## 🔍 Development

### Format + Lint + Validate

```bash
pre-commit run --all-files
```

This runs:

- `black` (formatting)
- `ruff` (linting & import correctness)
- `ShellCheck` (Bash scripts)
- Shebang presence validation

> Ensure all hooks pass before committing. This is strictly enforced.

---

## 📁 Project Structure

```
video-compressor/
├── clean_build.sh     # Clean build artifacts only
├── Makefile           # Entrypoint for install/uninstall/run
├── main.py            # Application entrypoint
├── pyproject.toml     # PEP 621 metadata and requirements
├── setup.py           # Legacy support for setuptools
├── requirements.txt   # Runtime dependencies
├── res/
│   └── icon.ico       # Application icon
└── src/
    ├── globals.py     # Global constants & shared state
    ├── thread.py      # Compression thread logic
    ├── download.py    # FFmpeg downloader & extractor
    ├── styles.py      # PyQt6 stylesheet and layout constants
    └── ...
```

---

## 🧑‍💻 Maintainer

**4ndr0666**

- Arch Linux Native
- MIT Licensed
- GitHub: [@4ndr0666](https://github.com/4ndr0666)

🗓 Release: `v1.0.0`  
📦 Finalized: `2025-06-27`
