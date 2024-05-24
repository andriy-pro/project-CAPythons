# hello: Displays a greeting message.
# add-note: Adds a new note.
# edit-note: Edits an existing note.
# delete-note: Deletes an existing note.      
# display-notes: Displays all notes.
# add: Adds a new contact to the address book.
# change: Changes the phone number of an existing contact.
# add-phone: Adds a new phone number to an existing contact.
# add-birthday: Adds a birthday to an existing contact.
# all: Shows all contacts in the address book.
# show-phone: Shows the phone number of a contact.
# close: Saves the address book and exits the program.
# exit: Saves the address book and exits the program.
# help: Displays this help message.
# set-language: Sets the application language.

import unittest
import sys

import os

# Додавання кореневої теки проекту до sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import СAPythonsBook
import CAPyBook.presentation
import CAPyBook.presentation.cli


class Test(unittest.TestCase):

    input_file_names=["test1"]

    directory="./tests/"

    @unittest.skip("make refs") #uncomment line for creates sample (reference) files
    def tests_CLI_make_ref(self):
        """Creates sample (reference) files with program output. 
        The names of the input files are obtained 
        from the names of the input files by adding _."""
        for name in Test.input_file_names:
            self.CLI_make_ref(name)

    def CLI_make_ref(self,name):
        
        sys.stdin = open(Test.directory+name+".txt")  
        original_stdout = sys.stdout
        with open(Test.directory+name+"_ref.txt", 'w') as f:
            sys.stdout = f
            CAPyBook.presentation.cli.main()
        sys.stdout = original_stdout    
        assert True

    #@unittest.skip("make test")
    def tests_CLI_make_test(self):
        for name in Test.input_file_names:
            self.CLI_make_test(name)

    def CLI_make_test(self,name):
        sys.stdin = open(Test.directory+name+".txt")  
        original_stdout = sys.stdout
        with open(Test.directory+name+"_log.txt", 'w') as f:
            sys.stdout = f
            CAPyBook.presentation.cli.main()
        sys.stdout = original_stdout    
        self.assertTrue(self.compare_text_files(Test.directory+name+"_ref.txt",\
                                                Test.directory+name+"_log.txt")) 

    def compare_text_files(self,file1_path, file2_path):
        with open(file1_path, 'r', encoding='utf-8') as file1, \
            open(file2_path, 'r', encoding='utf-8') as file2:

            content1 = file1.read()
            content2 = file2.read()

            return content1 == content2


if __name__=="__main__":
    unittest.main()
 