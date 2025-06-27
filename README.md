# 🎥 VideoCompressor

Compress videos to any target file size via a modern PyQt6 GUI — clean, native, and optimized for **Arch Linux**.

---

## ✨ Features

- Batch video queueing
- Target precise output file size (in MB)
- GPU acceleration support (NVIDIA NVENC, Intel QSV, AMD AMF)
- Two-pass encoding with automatic bitrate calculation
- Preserves audio quality and sync
- Native Linux notifications via `notify-send`
- Persistent user settings (target size + GPU toggle)
- Auto-opens output directory after encoding
- Clean PyQt6 interface with progress and status logging

---

## 🛠 Install (Arch Linux Only)

```bash
# Clone the project
git clone https://github.com/4ndr0666/video-compressor.git
cd video-compressor

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies and build the package
make install
```

---

## 🚀 Run

```bash
videocompressor
```

Or:

```bash
make run
```

---

## 🧹 Clean Build Artifacts

```bash
make clean
```

---

## 🗑 Uninstall

```bash
make uninstall
```

---

## 🧑‍💻 Maintainer

**4ndr0666**  
MIT Licensed  
Arch Linux Native
