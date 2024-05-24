import sys

def test_function():
    # Сохраняем текущий поток вывода stdout
    original_stdout = sys.stdout
    
    # Открываем файл для записи вывода
    with open('output.txt', 'w') as f:
        # Перенаправляем поток вывода stdout на файл
        sys.stdout = f
        
        # Выполняем тесты или код, который содержит операторы print
        print("Привет, мир!")
        print("Это вывод, который будет направлен в файл.")
        
    # Возвращаем поток вывода stdout в исходное состояние
    sys.stdout = original_stdout

# Вызываем тестовую функцию
test_function()
