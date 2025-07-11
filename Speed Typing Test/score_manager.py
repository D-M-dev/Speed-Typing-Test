import os, json
from datetime import datetime

class ScoreManager:
    FILE = "score_history.json"

    def __init__(self):
        if not os.path.exists(self.FILE):
            with open(self.FILE, "w") as f:
                json.dump([], f)

    def save_score(self, username, wpm, accuracy, mode):
        record = {
            "username": username,
            "wpm": wpm,
            "accuracy": accuracy,
            "mode": mode,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        history = self.get_history()
        history.append(record)
        with open(self.FILE, "w") as f:
            json.dump(history, f)

    def get_history(self):
        with open(self.FILE, "r") as f:
            return json.load(f)

    def reset_history(self):
        with open(self.FILE, "w") as f:
            json.dump([], f)