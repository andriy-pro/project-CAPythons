import sys
import os



# Додавання шляху до каталогу src для імпорту модулів
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

 
import CAPyBook
import CAPyBook.app.entities
import CAPyBook.presentation.cli


from CAPyBook.presentation.cli import main

if __name__ == "__main__":
    main()
