from PyQt5.QtWidgets import QApplication

class Themes:
    def __init__(self):
        self.dark = False

    def toggle_theme(self):
        self.dark = not self.dark

    def apply_theme(self, window):
        if self.dark:
            window.setStyleSheet("""
                QWidget { background: #23272f; color: #ececec; }
                QPushButton { background: #353b45; color: #ececec; }
                QLineEdit, QTextEdit { background: #2c313c; color: #ececec; }
                QProgressBar { background: #23272f; color: #3fd77a; }
            """)
        else:
            window.setStyleSheet("""
                QWidget { background: #f8fafd; color: #23272f; }
                QPushButton { background: #e6e8ea; color: #23272f; }
                QLineEdit, QTextEdit { background: #fff; color: #23272f; }
                QProgressBar { background: #f8fafd; color: #48b2f7; }
            """)