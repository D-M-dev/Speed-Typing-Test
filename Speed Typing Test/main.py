import sys
from PyQt5.QtWidgets import QApplication
from ui_main import TypingSpeedApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TypingSpeedApp()
    window.show()
    sys.exit(app.exec_())