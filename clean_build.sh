#!/usr/bin/env bash
set -e

echo "🧼 Cleaning build artifacts..."
rm -rf build dist *.egg-info src/*.egg-info __pycache__ src/__pycache__
