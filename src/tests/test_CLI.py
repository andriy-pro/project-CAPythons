import src.presentation.cli  # The module which contains the call to input

import sys

class Test:
    def test_function(self):
        sys.stdin = open("./src/tests/preprogrammed_inputs.txt")  # open("preprogrammed_inputs.txt")
        src.presentation.cli.main()
        output=sys.stdout
        with open("firstout.txt","w") as file: 
            for chunk in output:
                file.write(chunk)    

        print(output)
        assert output=="Goodbay"