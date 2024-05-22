import sys
import os

# Додавання шляху до каталогу src для імпорту модулів
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from presentation.cli import main

if __name__ == "__main__":
    main()
