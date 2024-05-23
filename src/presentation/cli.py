import sys
import os
from typing import Tuple

# Додавання шляху до каталогу src для імпорту модулів
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from app.entities import AddressBook
from app.services import handle_command
from presentation.messages import Message
from infrastructure.storage import FileStorage
from colorama import init, Fore, Style
from app.interfaces import Command


def parse_input(user_input: str) -> Tuple[str, list[str]]:
    """Parse the user input into a command and arguments."""
    parts = user_input.lower().split()
    command = parts[0] if parts else ""
    args = parts[1:] if len(parts) > 1 else []
    return command, args


def main():
    storage = FileStorage()
    address_book = AddressBook(
        storage.load_contacts()
    )  # Load the address book from the file

    init(autoreset=True)  # Initialize colorama

    # Завантаження шаблонів для початкової мови
    Message.load_templates("en")

    banner_part_1 = """
     _               _       _                 _     ____          _                ____  
    / \\    ___  ___ (_) ___ | |_  __ _  _ __  | |_  | __ )   ___  | |_    __   __  |___ \\ 
   / _ \\  / __|/ __|| |/ __|| __|/ _` || '_ \\ | __| |  _ \\  / _ \\ | __|   \\ \\ / /    __) |
  / ___ \\ \\__ \\\\__ \\| |\\__ \\| |_| (_| || | | || |_  | |_) || (_) || |_     \\ V /_   / __/ 
 /_/   \\_\\|___/|___/|_||___/ \\__|\\__,_||_| |_| \\__| |____/  \\___/  \\__|     \\_/(_) |_____|
                                                                                         
"""
    print(f"{Fore.GREEN}{banner_part_1}{Style.RESET_ALL}")
    print()
    print(
        f"{Fore.CYAN}{Style.BRIGHT}Welcome to the Assistant Bot ver. 2.3 !{Style.RESET_ALL}"
    )
    print()

    # TODO: Переробити зміну мови боту
    # (на цей момент потрібно ввести команду "lang" + "uk" або "en")
    exit_command = False
    while not Command.exit_command_flag:
        user_input = input(f"{Fore.YELLOW}Enter a command: {Style.RESET_ALL}").strip()
        if user_input.startswith("lang "):
            _, lang = user_input.split(maxsplit=1)
            Message.load_templates(lang)
            print(f"Language set to {lang}.")
            continue

        command, args = parse_input(user_input)
        handle_command(command, address_book, *args)
        storage.save_contacts(
            address_book
        )  # Save the contacts after handling the command
