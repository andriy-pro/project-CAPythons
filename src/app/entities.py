import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from collections import UserDict
from colorama import Fore, Style


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value: str):
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value: str):
        if not value.isdigit() or len(value.strip()) != 10:
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value: str):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)


class Record:
    def __init__(self, name: Name):
        self.id = uuid.uuid4()
        self.name = name
        self.phones: List[Phone] = []
        self.birthday: Optional[Birthday] = None

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def remove_phone(self, phone: Phone):
        self.phones = [p for p in self.phones if p.value != phone.value]

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday

    def __str__(self):
        phones = "; ".join([str(phone) for phone in self.phones])
        birthday = (
            f"{Fore.GREEN}, birthday: {Fore.CYAN}{self.birthday}{Style.RESET_ALL}"
            if self.birthday
            else ""
        )
        return f"{Fore.GREEN}Contact name: {Fore.CYAN}{self.name}{Fore.GREEN}, phones: {Fore.CYAN}{phones}{birthday}{Style.RESET_ALL}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.id] = record

    def delete(self, record_id: uuid.UUID):
        if record_id in self.data:
            del self.data[record_id]
        else:
            raise KeyError(f"Record with ID '{record_id}' not found")

    def find_by_name(self, name: Name) -> Optional[Record]:
        for record in self.data.values():
            if record.name.value == name.value:
                return record
        return None

    def get_upcoming_birthdays(self) -> List[Dict[str, str]]:
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                day_difference = (birthday_this_year - today).days
                if 0 <= day_difference <= 7:
                    congratulation_date = birthday_this_year
                    if birthday_this_year.weekday() > 4:
                        congratulation_date += timedelta(
                            days=7 - birthday_this_year.weekday()
                        )

                    upcoming_birthdays.append(
                        {
                            "name": record.name.value,
                            "congratulation_date": congratulation_date.strftime(
                                "%d.%m.%Y"
                            ),
                        }
                    )

        return upcoming_birthdays

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
