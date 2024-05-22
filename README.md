# project-CAPythons

Поточна структура проекту:
```plaintext
src/
├── application/
│   ├── services.py  # Логіка для роботи з контактами
│   ├── entities.py  # Класи Field, Name, Phone, Birthday, Record
│   └── interfaces.py  # Інтерфейси для взаємодії зі storage (у майбутньому — бази даних, хмарні сервіси тощо)
├── infrastructure
│   └── storage.py  # Реалізація збереження/відновлення контактів, серіалізація
├── presentation
│   ├── cli.py  # Обробка команд та взаємодія з користувачем 
│   └── messages.py # Оформлення повідомлень, до яких (в майбутньому) можна буде застосовувати різні кольорові теми
├── resources
│   ├── messages_en.json  # Шаблони повідомлень (англійські + українські)
│   └── messages_en.json
└── main.py  # Точка входу: для запуску у VS Code всього додатку, потрібно відкрити саме цей файл, і (наприклад) натиснути F5.

tests/ # Імена файлів з тестами могли б виглядати приблизно так
├── test_cli.py
├── test_entities.py
├── test_interfaces.py
├── test_services.py
└── test_storage.py
```
