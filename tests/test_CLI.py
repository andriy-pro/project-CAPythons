#import src.presentation.cli  # The module which contains the call to input
import unittest
import sys

import os

# Додавання кореневої теки проекту до sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import src
import src.CAPythonsBook
import src.CAPythonsBook.presentation
import src.CAPythonsBook.presentation.cli

class Test(unittest.TestCase):

    file_names=["test1"]
    directory="./tests/"

    #@unittest.skip("make refs")
    def tests_CLI_make_ref(self):
        for name in Test.file_names:
            self.CLI_make_ref(name)

    def CLI_make_ref(self,name):
        sys.stdin = open(Test.directory+name+".txt")  
        original_stdout = sys.stdout
        with open(Test.directory+name+"_ref.txt", 'w') as f:
        # Перенаправляем поток вывода stdout на файл
            sys.stdout = f
            #output=sys.stdout
            src.CAPythonsBook.presentation.cli.main()
            #output=1 #sys.stdout
        sys.stdout = original_stdout    
        #print(type(output))
        #print(dir(output))
        assert True

    #@unittest.skip("make test")
    def tests_CLI_make_test(self):
        for name in Test.file_names:
            self.CLI_make_test(name)

    def CLI_make_test(self,name):
        sys.stdin = open(Test.directory+name+".txt")  
        original_stdout = sys.stdout
        with open(Test.directory+name+"_log.txt", 'w') as f:
        # Перенаправляем поток вывода stdout на файл
            sys.stdout = f
            #output=sys.stdout
            src.CAPythonsBook.presentation.cli.main()
            #output=1 #sys.stdout
        sys.stdout = original_stdout    
        #print(type(output))
        #print(dir(output))
        self.assertTrue(self.compare_text_files(Test.directory+name+"_ref.txt",\
                                                Test.directory+name+"_log.txt")) 

    def compare_text_files(self,file1_path, file2_path):
        with open(file1_path, 'r', encoding='utf-8') as file1, \
            open(file2_path, 'r', encoding='utf-8') as file2:
        
        # Считываем содержимое файлов
            content1 = file1.read()
            content2 = file2.read()

        # Сравниваем содержимое файлов
            return content1 == content2


if __name__=="__main__":
    unittest.main()
 