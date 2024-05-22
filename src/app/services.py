import sys
from app.interfaces import Command, FieldCommand
from app.entities import Field, Name, Phone, Birthday, Record, AddressBook
from infrastructure.storage import FileStorage
from presentation.messages import Message
from app.command_registry import register_command, get_command
from typing import Callable
from colorama import Fore, Style


# Декоратор для обробки помилок у функціях команд
def input_error(handler: Callable) -> Callable:
    """Decorator for handling errors in command functions."""

    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except TypeError as e:
            print(
                f"{Fore.RED}Error: Incorrect command.\n{Fore.MAGENTA}{e}{Style.RESET_ALL}"
            )
        except ValueError as e:
            print(
                f"{Fore.RED}Error: Incorrect arguments.\n{Fore.MAGENTA}{e}{Style.RESET_ALL}"
            )
        except KeyError as e:
            print(
                f"{Fore.RED}Error: Contact not found.\n{Fore.MAGENTA}{e}{Style.RESET_ALL}"
            )
        except IndexError as e:
            print(
                f"{Fore.RED}Error: Index out of range.\n{Fore.MAGENTA}{e}{Style.RESET_ALL}"
            )
        except Exception as e:
            print(
                f"{Fore.RED}An unexpected error occurred:\n{Fore.MAGENTA}{e}{Style.RESET_ALL}"
            )

    return wrapper


@input_error
def handle_command(command: str, address_book: AddressBook, *args: str) -> None:
    """Обробляє команду користувача, викликаючи відповідний метод."""
    cmd = get_command(command)
    if cmd:
        cmd_instance = cmd(address_book)
        cmd_instance.execute(*args)
    else:
        Message.error("incorrect_command", command=command)


@register_command("hello")
class HelloCommand(Command):
    def execute(self, *args: str) -> None:
        """Виводить привітальне повідомлення."""
        Message.info("greeting")


@register_command("add")
class AddContactCommand(Command):
    def execute(self, *args: str) -> None:
        """Додає новий контакт у адресну книгу."""
        if len(args) != 2:
            Message.error("incorrect_arguments")
            return
        name, phone = args
        record = self.address_book.find_by_name(Name(name))
        if record:
            if any(p.value == phone for p in record.phones):
                Message.warning("contact_exists", name=name, phone=phone)
            else:
                current_phone = record.phones[0].value if record.phones else "No phone"
                Message.warning("contact_exists", name=name, phone=current_phone)
        else:
            new_record = Record(Name(name))
            new_record.add_phone(Phone(phone))
            self.address_book.add_record(new_record)
            Message.info("contact_added", name=name, phone=phone)


@register_command("change")
class ChangeContactCommand(Command):
    def execute(self, *args: str) -> None:
        """Змінює номер телефону існуючого контакту."""
        if len(args) != 2:
            Message.error("incorrect_arguments")
            return
        name, new_phone = args
        record = self.address_book.find_by_name(Name(name))
        if record:
            current_phone = record.phones[0].value if record.phones else None
            if new_phone == current_phone:
                Message.warning("contact_exists", name=name, phone=new_phone)
            else:
                record.edit_phone(record.phones[0], Phone(new_phone))
                Message.info(
                    "contact_updated",
                    name=name,
                    old_phone=current_phone,
                    new_phone=new_phone,
                )
        else:
            Message.error("contact_not_found", name=name)


@register_command("add-phone")
class AddPhoneCommand(FieldCommand):
    def create_field(self, *args: str) -> Field:
        return Phone(args[0])

    def execute_field(self, record: Record, field: Field) -> None:
        """Додає новий номер телефону до існуючого контакту."""
        if any(p.value == field.value for p in record.phones):
            Message.warning("contact_exists", name=record.name.value, phone=field.value)
        else:
            record.add_phone(field)
            Message.info("contact_added", name=record.name.value, phone=field.value)


@register_command("show-phone")
class ShowPhoneCommand(Command):
    def execute(self, *args: str) -> None:
        """Показує номер телефону контакту."""
        if len(args) != 1:
            Message.error("incorrect_arguments")
            return
        name = args[0]
        record = self.address_book.find_by_name(Name(name))
        if record:
            phones = "; ".join([phone.value for phone in record.phones])
            Message.info("phone_info", name=name, phone=phones)
        else:
            Message.error("contact_not_found", name=name)


@register_command("add-birthday")
class AddBirthdayCommand(FieldCommand):
    def create_field(self, *args: str) -> Field:
        return Birthday(args[0])

    def execute_field(self, record: Record, field: Field) -> None:
        """Додає день народження до існуючого контакту."""
        record.add_birthday(field)
        Message.info("birthday_set", name=record.name.value, birthday=field.value)


@register_command("all")
class ShowAllContactsCommand(Command):
    def execute(self) -> None:
        """Показує всі контакти."""
        if self.address_book.data:
            for record in self.address_book.data.values():
                print(str(record))
        else:
            raise IndexError("No contacts available.")

exit_command_flag=False

@register_command("exit")
@register_command("quit")
@register_command("close")
class ExitCommand(Command):
    def execute(self, *args: str) -> None:
        """Зберігає адресну книгу та виходить з програми."""
        storage = FileStorage()
        storage.save_contacts(self.address_book.data)
        Message.info("exit_message")
        Command.exit_command_flag=True #sys.exit()
