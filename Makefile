.PHONY: all clean dist install run

PACKAGE = videocompressor

all: clean dist

clean:
	@./clean_build.sh

dist:
	@echo "📦 Building..."
	python -m build

install:
	@echo "📥 Installing..."
	pip install ./dist/$(PACKAGE)-*.whl

run:
	@echo "🚀 Launching..."
	python main.py
