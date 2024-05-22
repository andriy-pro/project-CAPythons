from typing import Dict, Optional
from app.interfaces import Command

# Реєстр для зберігання команд
command_registry: Dict[str, Command] = {}


def register_command(name: str):
    """
    Декоратор для реєстрації команд.
    """

    def decorator(command: Command):
        command_registry[name] = command
        return command

    return decorator


def get_command(command_name: str) -> Optional[Command]:
    """
    Повертає команду за її назвою або None, якщо команда не знайдена.
    """
    return command_registry.get(command_name)
