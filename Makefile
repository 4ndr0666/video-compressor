SHELL := /usr/bin/env bash
.SHELLFLAGS := -euo pipefail -c
.PHONY: all clean dist install uninstall run

PACKAGE := videocompressor
PYTHON  := $(shell command -v python3 >/dev/null && echo python3 || echo python)

all: clean dist install

clean:
	@echo "🧼 Cleaning build artifacts..."
	@bash clean_build.sh

dist:
	@echo "📦 Building wheel + sdist..."
	@$(PYTHON) -m build

install:
	@echo "📥 Installing package locally..."
	@$(PYTHON) -m pip install --force-reinstall ./dist/$(PACKAGE)-*.whl

uninstall:
	@echo "🗑️  Uninstalling $(PACKAGE)..."
	@$(PYTHON) -m pip uninstall -y $(PACKAGE)

run:
	@echo "🚀 Running videocompressor..."
	@$(PYTHON) main.py
