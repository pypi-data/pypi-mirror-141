from magic_lib.magicfunctions import *
class MagicClass:
    """
    Instantiate the Magic class.
    all magic functions can be called by this class through 'magicFunction' method
    
    """
    def __init__(self):
        pass

    def magicFunction(str, *args):
        if str == "reverseString":
            return magicFunction1(args[0])
        elif str == "fibonacciSearch":
            return magicFunction2(args[0], args[1])
        elif str == "fizzBuzz":
            return magicFunction3(args[0], args[1])
        else:
            print("This function does not exist")
            return -1
