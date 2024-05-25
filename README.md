
# CAPythonsBook : *Консольний додаток для зберігання контактів*

## Background

Цей проект має на меті створення консольного додатку для зберігання контактів, який буде розроблений мовою Python. Додаток дозволить користувачам зберігати інформацію про контакти, що можуть містити крім імен: номери телефонів, дні народження, email-адреси та теги. Основна ціль — створити простий у використанні інструмент з можливістю розширення функціоналу в майбутньому.

## Requirements

Основні функції, які має підтримувати додаток:
* `create`: Створення нових записів (контакти — з іменами, телефонами, днями народження тощо; нотатки — з назвами та тегами).
* `remove`: Видалення наявних записів.
* `update`: Оновлення інформації про наявні записи.
* `display`: Відображення деталей наявних записів.
* `search`: Пошук записів за різними критеріями.

Кожна з цих команд повинна приймати наступним аргументом визначення об'єкту, над яким буде виконана дія (наприклад, contact, note, phone, birthday).

Додаткові вимоги:
* Структура додатку має бути максимально простою для додавання нових команд та підтримування вже наявних.
* Архітектура додатку повинна дозволяти легке інтегрування з зовнішніми сервісами або API у майбутньому.
* Дані користувачів повинні зберігатися у файлах "addressbook.json" для контактів і "notes.json" для нотаток.
* Додаток має підтримувати багатомовність, а налаштування мають зберігатися у файлі "settings.json".
* Записи мають складатися з обов'язкового поля "Ім'я" та необов'язкових: телефон (може містити кілька значень), дата народження, email-адреса, теги тощо.
* Додаток має повідомляти користувача про дні народження у задану кількість наступних днів (установлене значення: 7).
* Нотатки обов'язково мають містити назву і текст, а також необов'язково теги.

## Method

Для реалізації даного додатку будуть використані такі основні компоненти:

### Структура проекту

Проект повинен мати чітку структуру, що розділяє різні компоненти:
- **app**: основні сервіси та інтерфейси.
- **infrastructure**: зберігання даних.
- **presentation**: командний інтерфейс та повідомлення.
- **resources**: мовні файли.
- **main.py**: головний файл для запуску програми.

```
    📂 CAPythonsBook
    ┣━━ 📂 app
    ┃   ┠── 📄 interfaces.py
    ┃   ┠── 📄 services.py
    ┃   ┖── 📄 settings.py
    ┣━━ 📂 infrastructure
    ┃   ┖── 📄 storage.py
    ┣━━ 📂 presentation
    ┃   ┠── 📄 cli.py
    ┃   ┖── 📄 messages.py
    ┣━━ 📂 resources
    ┃   ┠── 📄 messages_en.json
    ┃   ┖── 📄 messages_uk.json
    ┠── 📄 main.py
    ┠── 📄 addressbook.json
    ┖── 📄 notes.json
```

### Основні цілі підходів, застосованих до структури

1. **Чітка структура проекту**:
   - Розділення логіки, зберігання даних, інтерфейсу користувача та налаштувань.
   - Використання окремих модулів для різних функціональних частин додатку.

2. **Багатомовна підтримка**:
   - Використання JSON файлів для зберігання повідомлень різними мовами.
   - Можливість легко додавати нові мови шляхом додавання нових JSON файлів.

3. **Гнучкість та розширюваність**:
   - Використання інтерфейсів для визначення основних операцій з контактами та нотатками.
   - Простота додавання нових команд та функціоналу.

4. **Зберігання даних у JSON файлах**:
   - Простота та зручність реалізації.
   - Легкість читання та запису даних.

## Патерни, що необхідно використати

### Високий пріоритет

1. **Використання `command_registry` для організації команд**

`command_registry` дозволяє ефективно організувати команди у додатку та забезпечує додаткову гнучкість і розширюваність.

Короткий опис:
```python
# command_registry.py
command_registry = {}

def register_command(name):
    def decorator(func):
        command_registry[name] = func
        return func
    return decorator

def get_command(name):
    return command_registry.get(name)
```

Приклад використання:
```python
# services.py
@register_command('create_contact')
def create_contact(name, phone, birthday, email, tags):
    # Логіка створення контакту
    pass

@register_command('remove_contact')
def remove_contact(name):
    # Логіка видалення контакту
    pass

# cli.py
def handle_command(command_name, *args):
    command = get_command(command_name)
    if command:
        command(*args)
    else:
        print("Command not found.")
```

Переваги цього підходу:
- **Гнучкість**: Легко додавати нові команди без необхідності змінювати основний код додатку.
- **Розширюваність**: Додавання нових функцій стає простішим, оскільки нові команди можна реєструвати окремо від основного логічного коду.
- **Інкапсуляція**: Логіка команд ізольована від основного коду, що полегшує тестування та підтримку.
- **Організованість**: Забезпечує чітку структуру коду, де кожна команда реєструється окремо.
- **Читабельність**: Команди чітко організовані, і код залишається чистим і зрозумілим.
- **Зручність**: Полегшує додавання нових команд та модифікацію існуючих.
- **Модульність**: Кожна команда є незалежною функцією, що сприяє кращому модульному тестуванню.

Можливі недоліки:
- **Ускладненість**: Може бути складніше зрозуміти для нових розробників, які не знайомі з цим паттерном.

2. **Використання декораторів для обробки помилок**

Декоратор `input_error` обробляє помилки в функціях команд, забезпечуючи зручну обробку помилок та єдиний спосіб обробки виключень.

Приклад:
```python
def input_error(handler: Callable) -> Callable:
    """Decorator for handling errors in command functions."""
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except TypeError as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    return wrapper
```

3. **Документування коду**

Для полегшення розуміння коду іншими розробниками та для майбутньої підтримки варто використовувати докстрінги та створювати документацію до коду.

Приклад:
```python
def create_contact(name, phones=[], birthday=None, email=None, tags=[]):
    """
    Створює новий контакт.

    :param name: Ім'я контакту
    :param phones: Список телефонних номерів
    :param birthday: Дата народження
    :param email: Електронна пошта
    :param tags: Список тегів
    :return: None
    """
    pass
```
У додатку варто використовувати коментування та документування англійською мовою для ширшої підтримки розробників.

4. **Використання модульного тестування**

Для забезпечення якості коду і уникнення регресій варто впровадити модульне тестування. Модульні тести дозволяють перевіряти функціональність окремих частин коду автоматично.

Приклад:
```python
import unittest
from app.services import ContactManager

class TestContactManager(unittest.TestCase):
    def setUp(self

):
        self.contact_manager = ContactManager()

    def test_create_contact(self):
        self.contact_manager.create_contact("John Doe", ["123456789"], "01-01-1990", "john@example.com", ["friend"])
        contact = self.contact_manager.find_contact("John Doe")
        self.assertIsNotNone(contact)
        self.assertEqual(contact.name, "John Doe")

if __name__ == '__main__':
    unittest.main()
```

### Середній пріоритет

5. **Використання сторонніх бібліотек для покращення CLI**

Бібліотека `prompt_toolkit` забезпечує автозавершення команд та підказки з історії, що значно покращує користувацький досвід у консольному додатку.

Приклад:
```python
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion

class CommandCompleter(Completer):
    def get_completions(self, document: Document, complete_event):
        text = document.text_before_cursor
        matches = difflib.get_close_matches(text, command_registry.keys(), n=5, cutoff=0.1)
        for match in matches:
            yield Completion(match, start_position=-len(text))
```

6. **Використання логування**

Замість простого виведення повідомлень про помилки у консоль можна впровадити систему логування, яка допоможе відслідковувати помилки та діагностувати проблеми у додатку.

Приклад:
```python
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Використання логування у функціях
def some_function():
    try:
        # Ваш код
        pass
    except Exception as e:
        logger.error("An error occurred: %s", e)
```

7. **Використання парсингу аргументів командного рядка**

Для обробки аргументів командного рядка варто використовувати бібліотеки на кшталт `argparse`, які забезпечують зручний інтерфейс для роботи з параметрами командного рядка.

Приклад:
```python
import argparse

parser = argparse.ArgumentParser(description="Contact Manager")
parser.add_argument("command", help="Command to execute")
parser.add_argument("arguments", nargs="*", help="Arguments for the command")

args = parser.parse_args()
print(args.command, args.arguments)
```

8. **Використання `dataclass` для спрощення класів**

Бібліотека `dataclasses` спрощує створення класів для зберігання даних і автоматично генерує методи, такі як `__init__`, `__repr__`, та інші.

Приклад:
```python
from dataclasses import dataclass
from typing import List

@dataclass
class Contact:
    name: str
    phones: List[str]
    birthday: str
    email: str
    tags: List[str]
```

### Низький пріоритет

9. **Використання абстрактних класів та інтерфейсів**

Використання абстрактних класів для визначення інтерфейсів команд полегшує розширюваність функціоналу шляхом додавання нових класів, які наслідують ці інтерфейси.

Приклад:
```python
class Command(ABC):
    description = ""
    exit_command_flag = False

    @abstractmethod
    def execute(self, *args: str) -> None:
        pass

class FieldCommand(Command, ABC):
    @abstractmethod
    def execute_field(self, record: Record, field: Field) -> None:
        pass
```

10. **Використання Dependency Injection**

Для полегшення тестування та підвищення гнучкості коду можна впровадити паттерн "впровадження залежностей" (Dependency Injection).

Приклад:
```python
class ContactManager:
    def __init__(self, storage):
        self.storage = storage

class Storage:
    def save(self, data):
        pass

# Використання ContactManager з конкретною реалізацією Storage
storage = Storage()
contact_manager = ContactManager(storage)
```

### Відхилені патерни

#### Паттерн "Фабричний метод" (Factory Method)

Зайвий для невеликого додатку, де `command_registry` забезпечує достатню гнучкість.

Приклад:
```python
# command_factory.py
class CommandFactory:
    @staticmethod
    def create_command(command_type, *args):
        if command_type == 'create_contact':
            return CreateContactCommand(*args)
        elif command_type == 'remove_contact':
            return RemoveContactCommand(*args)
        # Додати інші команди
        else:
            raise ValueError(f"Unknown command type: {command_type}")

# services.py
class CreateContactCommand:
    def __init__(self, name, phone, birthday, email, tags):
        self.name = name
        self.phone = phone
        self.birthday = birthday
        self.email = email
        self.tags = tags

    def execute(self):
        # Логіка створення контакту
        pass

class RemoveContactCommand:
    def __init__(self, name):
        self.name = name

    def execute(self):
        # Логіка видалення контакту
        pass

# cli.py
def handle_command(command_type, *args):
    command = CommandFactory.create_command(command_type, *args)
    command.execute()
```

#### Паттерн "Команда" (Command Pattern)

Подібний за функціоналом до `command_registry`, але більш складний для реалізації.

Приклад:
```python
# command.py
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class CreateContactCommand(Command):
    def __init__(self, contact_manager, name, phone, birthday, email, tags):
        self.contact_manager = contact_manager
        self.name = name
        self.phone = phone
        self.birthday = birthday
        self.email = email
        self.tags = tags

    def execute(self):
        self.contact_manager.create_contact(self.name, self.phone, self.birthday, self.email, self.tags)

class RemoveContactCommand(Command):
    def __init__(self, contact_manager, name):
        self.contact_manager = contact_manager
        self.name = name

    def execute(self):
        self.contact_manager.remove_contact(self.name)

# cli.py
def handle_command(command):
    command.execute()
```

#### Паттерн "Стратегія" (Strategy Pattern)

Може бути корисним для складніших додатків, але надмірний для даного випадку.

Приклад:
```python
# strategy.py
class CommandStrategy(ABC):
    @abstractmethod
    def execute(self, *args):
        pass

class CreateContactStrategy(CommandStrategy):
    def execute(self, contact_manager, name, phone, birthday, email, tags):
        contact_manager.create_contact(name, phone, birthday, email, tags)

class RemoveContactStrategy(CommandStrategy):
    def execute(self, contact_manager, name):
        contact_manager.remove_contact(name)

# cli.py
def handle_command(strategy, *args):
    strategy.execute(*args)
```
