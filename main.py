import sys
from src.videocompressor.main import Window
from PyQt6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
