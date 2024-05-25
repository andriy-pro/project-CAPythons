import sys
import os

# Додавання шляху до каталогу src для імпорту модулів
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..")))
#import scr 
from src.CAPythonsBook.presentation.cli import main

if __name__ == "__main__":
    main()
