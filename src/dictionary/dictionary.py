from json import load

'''
This file will contain the Dictionary object that will be used
throughout the program. Creating a separate object for it 
as it is likely to be initialised with other sources later on
and it is used by multiple objects.

It is very basic for now. 
'''

class Dictionary(object):
    def __init__(self, dictionary="../../dict/dict.json"):
        with open(dictionary, "r") as f:
            self.dict = load(f)
