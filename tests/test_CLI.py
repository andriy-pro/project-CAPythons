#import src.presentation.cli  # The module which contains the call to input
import unittest
import sys

import os

import src.presentation
import src.presentation.cli

#import src.presentation
#import src.presentation.cli

# Додавання кореневої теки проекту до sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import src

class Test(unittest.TestCase):
    def test_function(self):
        sys.stdin = open("./tests/preprogrammed_inputs.txt")  
        original_stdout = sys.stdout
        with open("./tests/otputs_ref.txt", 'w') as f:
        # Перенаправляем поток вывода stdout на файл
            sys.stdout = f
            output=sys.stdout
            src.presentation.cli.main()
            #output=1 #sys.stdout
        sys.stdout = original_stdout    
        #print(type(output))
        #print(dir(output))
        assert output=="Goodbay"