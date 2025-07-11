from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget,
    QHBoxLayout, QLineEdit, QProgressBar, QComboBox, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QRect
from typing_test import TypingTestWidget
from score_manager import ScoreManager
from settings import SettingsManager
from themes import Themes

class TypingSpeedApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Typing Speed Test")
        self.setGeometry(200, 100, 800, 450)
        self.themes = Themes()
        self.settings = SettingsManager()
        self.score_manager = ScoreManager()
        self.central = QStackedWidget()
        self.setCentralWidget(self.central)
        self.init_menu()

    def init_menu(self):
        menu_widget = QWidget()
        layout = QVBoxLayout(menu_widget)

        title = QLabel("TYPING SPEED TEST")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold;")
        layout.addWidget(title)

        self.username_input = QLineEdit(self.settings.get_username())
        self.username_input.setPlaceholderText("Zadejte uživatelské jméno")
        layout.addWidget(self.username_input)

        start_btn = QPushButton("Start")
        start_btn.clicked.connect(self.start_test)
        layout.addWidget(start_btn)

        mode_box = QComboBox()
        mode_box.addItems(["20 slov (classic)", "Na čas (30s)", "Nekonečno"])
        self.mode_box = mode_box
        layout.addWidget(mode_box)

        diff_box = QComboBox()
        diff_box.addItems(["Krátká slova", "Dlouhá slova", "Mix"])
        self.diff_box = diff_box
        layout.addWidget(diff_box)

        theme_btn = QPushButton("Přepnout režim (tmavý/světlý)")
        theme_btn.clicked.connect(self.toggle_theme)
        layout.addWidget(theme_btn)

        leaderboard_btn = QPushButton("Historie skóre & Export")
        leaderboard_btn.clicked.connect(self.show_leaderboard)
        layout.addWidget(leaderboard_btn)

        reset_btn = QPushButton("Reset statistik")
        reset_btn.clicked.connect(self.reset_stats)
        layout.addWidget(reset_btn)

        layout.addStretch()
        self.central.addWidget(menu_widget)
        self.central.setCurrentWidget(menu_widget)
        self.themes.apply_theme(self)

    def start_test(self):
        username = self.username_input.text().strip()
        if not username:
            QMessageBox.warning(self, "Chyba", "Zadejte uživatelské jméno!")
            return

        self.settings.set_username(username)
        mode = self.mode_box.currentText()
        difficulty = self.diff_box.currentText()
        test_widget = TypingTestWidget(self.score_manager, self.settings, mode, difficulty, self.themes)
        test_widget.back_to_menu.connect(self.return_to_menu)
        self.central.addWidget(test_widget)
        self.central.setCurrentWidget(test_widget)
        self.animate_transition()

    def return_to_menu(self):
        self.central.setCurrentIndex(0)
        self.animate_transition()

    def animate_transition(self):
        # Jednoduchý fade-in
        self.central.setWindowOpacity(0)
        self.anim = QPropertyAnimation(self.central, b"windowOpacity")
        self.anim.setDuration(500)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()

    def show_leaderboard(self):
        history = self.score_manager.get_history()
        leaderboard = "\n".join(
            [f"{i+1}. {r['username']} | {r['wpm']} WPM | {r['accuracy']}% | {r['mode']} | {r['date']}"
             for i, r in enumerate(history)]
        )
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Historie skóre")
        dlg.setText("Leaderboard:\n\n" + leaderboard)
        dlg.setDetailedText("Můžete exportovat historii v nastavení.")
        dlg.exec_()

    def reset_stats(self):
        res = QMessageBox.question(self, "Reset", "Opravdu smazat všechna skóre?", QMessageBox.Yes | QMessageBox.No)
        if res == QMessageBox.Yes:
            self.score_manager.reset_history()
            QMessageBox.information(self, "Resetováno", "Statistiky byly vymazány.")

    def toggle_theme(self):
        self.themes.toggle_theme()
        self.themes.apply_theme(self)