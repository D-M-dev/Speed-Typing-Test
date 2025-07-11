from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QProgressBar, QHBoxLayout
)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from word_provider import WordProvider
import time

class TypingTestWidget(QWidget):
    back_to_menu = pyqtSignal()

    def __init__(self, score_manager, settings, mode, difficulty, themes):
        super().__init__()
        self.score_manager = score_manager
        self.settings = settings
        self.themes = themes
        self.mode = mode
        self.difficulty = difficulty
        self.username = self.settings.get_username()
        self.init_ui()
        self.words = []
        self.current_index = 0
        self.correct_words = 0
        self.typed_words = []
        self.start_time = None
        self.timer = QTimer()
        self.time_limit = 30 if "čas" in mode.lower() else None
        self.countdown = QTimer()
        self.progress = 0

        self.prepare_test()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.info_label = QLabel("Připravte se...")
        self.info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info_label)

        self.words_label = QLabel("")
        self.words_label.setWordWrap(True)
        layout.addWidget(self.words_label)

        self.text_edit = QTextEdit()
        self.text_edit.setDisabled(True)
        self.text_edit.textChanged.connect(self.on_text_changed)
        layout.addWidget(self.text_edit)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.finish_btn = QPushButton("Konec / Odeslat")
        self.finish_btn.clicked.connect(self.finish_test)
        self.finish_btn.setDisabled(True)
        layout.addWidget(self.finish_btn)

        self.back_btn = QPushButton("Zpět do menu")
        self.back_btn.clicked.connect(self.back_to_menu)
        layout.addWidget(self.back_btn)

    def prepare_test(self):
        self.info_label.setText("3...")
        self.words = WordProvider.get_words(self.difficulty, 100 if "nekonečno" in self.mode.lower() else 20)
        self.display_words()
        self.text_edit.clear()
        self.text_edit.setDisabled(True)
        self.current_index = 0
        self.correct_words = 0
        self.typed_words = []
        self.progress = 0
        self.progress_bar.setValue(0)
        self.counter = 3
        self.countdown.timeout.connect(self.countdown_tick)
        self.countdown.start(1000)

    def countdown_tick(self):
        if self.counter > 1:
            self.counter -= 1
            self.info_label.setText(f"{self.counter}...")
        else:
            self.countdown.stop()
            self.info_label.setText("Start!")
            QTimer.singleShot(500, self.start_test)

    def start_test(self):
        self.text_edit.setDisabled(False)
        self.text_edit.setFocus()
        self.start_time = time.time()
        self.finish_btn.setDisabled(False)
        if self.time_limit:
            self.timer.timeout.connect(self.update_timer)
            self.timer.start(1000)
            self.time_left = self.time_limit
            self.progress_bar.setMaximum(self.time_limit)
            self.progress_bar.setValue(self.time_limit)
        else:
            self.progress_bar.setMaximum(len(self.words))
            self.progress_bar.setValue(0)

    def display_words(self):
        to_show = " ".join(self.words[:20]) if not self.time_limit else " ".join(self.words)
        self.words_label.setText(to_show)

    def on_text_changed(self):
        text = self.text_edit.toPlainText().strip()
        input_words = text.split()
        self.typed_words = input_words
        # Zvýraznění správných/špatných slov
        html = []
        for i, target in enumerate(self.words[:len(input_words)]):
            if i < len(input_words):
                user = input_words[i]
                if user == target:
                    html.append(f'<span style="color: #3fd77a; font-weight: bold;">{user}</span>')
                else:
                    html.append(f'<span style="color: #f25d5d; text-decoration:underline;">{user}</span>')
        # Zbytek slov
        if len(input_words) < len(self.words):
            html.append(" ".join(self.words[len(input_words):20]))
        self.words_label.setText(" ".join(html))
        # Progress
        if self.time_limit:
            if hasattr(self, "time_left"):
                self.progress_bar.setValue(self.time_left)
        else:
            self.progress_bar.setValue(len(input_words))

    def update_timer(self):
        self.time_left -= 1
        self.progress_bar.setValue(self.time_left)
        if self.time_left <= 0:
            self.timer.stop()
            self.finish_test()

    def finish_test(self):
        self.text_edit.setDisabled(True)
        self.finish_btn.setDisabled(True)
        total_words = len(self.typed_words)
        correct = sum([1 for i, word in enumerate(self.typed_words) if i < len(self.words) and word == self.words[i]])
        accuracy = int(100 * correct / total_words) if total_words else 0
        elapsed = time.time() - self.start_time if self.start_time else 1
        wpm = int((total_words / elapsed) * 60)
        self.info_label.setText(f"Výsledek: {wpm} WPM | Přesnost: {accuracy}%")
        self.score_manager.save_score(self.username, wpm, accuracy, self.mode)