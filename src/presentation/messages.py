import json
from colorama import Fore, Style
import os


class Message:
    templates = {}
    colors = {
        "info": Fore.GREEN,
        "highlight": Fore.CYAN,
        "warning": Fore.YELLOW,
        "error": Fore.RED,
        "param": Fore.MAGENTA,  # Колір для параметрів
        "reset": Style.RESET_ALL,
    }

    @classmethod
    def load_templates(cls, language: str) -> None:
        """Load message templates based on the selected language."""
        try:
            with open(
                os.path.join(
                    os.path.dirname(__file__), f"../resources/messages_{language}.json"
                ),
                "r",
                encoding="utf-8",
            ) as file:
                cls.templates = json.load(file)
        except FileNotFoundError:
            print(
                f"Language file for '{language}' not found. Loading default (English) templates."
            )
            with open(
                os.path.join(
                    os.path.dirname(__file__), "../resources/messages_en.json"
                ),
                "r",
                encoding="utf-8",
            ) as file:
                cls.templates = json.load(file)

    @staticmethod
    def apply_theme(message: str) -> str:
        """Apply color themes to the message."""
        for key, color in Message.colors.items():
            message = message.replace(f"{{{key}}}", color)
        return message

    @classmethod
    def format_message(cls, template_name: str, **kwargs) -> str:
        """Format the message with provided parameters."""
        template = cls.templates.get(template_name, "Message template not found")
        formatted_message = template.format(
            **{k: f"{{param}}{v}{{reset}}" for k, v in kwargs.items()}
        )
        return cls.apply_theme(formatted_message)

    @classmethod
    def info(cls, template_name: str, **kwargs) -> None:
        message = cls.format_message(template_name, **kwargs)
        print(f"{cls.colors['info']}{message}{cls.colors['reset']}")

    @classmethod
    def warning(cls, template_name: str, **kwargs) -> None:
        message = cls.format_message(template_name, **kwargs)
        print(f"{cls.colors['warning']}{message}{cls.colors['reset']}")

    @classmethod
    def error(cls, template_name: str, **kwargs) -> None:
        message = cls.format_message(template_name, **kwargs)
        print(f"{cls.colors['error']}{message}{cls.colors['reset']}")

    @classmethod
    def highlight(cls, template_name: str, **kwargs) -> None:
        message = cls.format_message(template_name, **kwargs)
        print(f"{cls.colors['highlight']}{message}{cls.colors['reset']}")
