import json
import os


class Settings:
    DEFAULT_LANGUAGE = "en"
    SETTINGS_FILE = "settings.json"

    def __init__(self):
        self.language = self.DEFAULT_LANGUAGE
        self.load_settings()

    def load_settings(self):
        if os.path.exists(self.SETTINGS_FILE):
            with open(self.SETTINGS_FILE, "r") as file:
                settings = json.load(file)
                self.language = settings.get("language", self.DEFAULT_LANGUAGE)

    def save_settings(self):
        settings = {"language": self.language}
        with open(self.SETTINGS_FILE, "w") as file:
            json.dump(settings, file, indent=4)

    def set_language(self, language):
        self.language = language
        self.save_settings()
