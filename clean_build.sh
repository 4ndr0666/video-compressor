#!/usr/bin/env bash
set -euo pipefail

# Resolve script directory and cd into project root
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$script_dir"

echo "🧼 Cleaning build artifacts..."

# Remove top-level build outputs
rm -rf build/ dist/ *.egg-info

# Remove egg-info under src and any __pycache__ anywhere
rm -rf src/*.egg-info
find src -type d -name "__pycache__" -prune -exec rm -rf {} +

echo "✅ Clean complete."
