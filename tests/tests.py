import src.presentation.cli  # The module which contains the call to input

import sys

class Test:
    def test_function(self):
        sys.stdin = "HELP"  # open("preprogrammed_inputs.txt")
        src.presentation.cli.main()
        output=sys.stdout
        print(output)
        assert output=="Goodbay"