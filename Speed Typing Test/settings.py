import json
import os

class SettingsManager:
    FILE = "settings.json"

    def __init__(self):
        if not os.path.exists(self.FILE):
            with open(self.FILE, "w") as f:
                json.dump({"username": "Host"}, f)

    def get_username(self):
        with open(self.FILE, "r") as f:
            data = json.load(f)
            return data.get("username", "Host")

    def set_username(self, username):
        with open(self.FILE, "w") as f:
            json.dump({"username": username}, f)