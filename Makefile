.PHONY: all clean dist install uninstall run

PACKAGE = videocompressor

all: clean dist install

clean:
	@echo "🧼 Cleaning build artifacts..."
	rm -rf build dist *.egg-info src/*.egg-info __pycache__ src/__pycache__

dist:
	@echo "📦 Building wheel + sdist..."
	python -m build

install:
	@echo "📥 Installing package locally..."
	pip install --force-reinstall ./dist/$(PACKAGE)-*.whl

uninstall:
	@echo "🗑️  Uninstalling videocompressor..."
	pip uninstall -y $(PACKAGE)

run:
	@echo "🚀 Running videocompressor..."
	python main.py
