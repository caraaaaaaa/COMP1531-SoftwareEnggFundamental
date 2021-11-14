'''has a push and a pop method and behaves like a standard stack'''

class Stack:
    '''behave like a standard stack'''
    def __init__(self):
        '''initialize'''
        self.stack = []

    def push(self, value):
        '''append a value in stack'''
        self.stack.append(value)

    def pop(self):
        '''pop the last value of stack'''
        if self.stack:
            self.stack.pop()
        else:
            raise ValueError()
