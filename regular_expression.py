from enum import Enum


class RegExOperation(Enum):
    PLUS = '+'
    CONCAT = '.'
    STAR = '*'
    UNDEFINED = '@'


class RegEx:
    def __init__(self, string=None, operation=RegExOperation.UNDEFINED, expression1=None, expression2=None):
        assert isinstance(operation, RegExOperation)
        self.string = None
        self.ex1 = None
        self.ex2 = None
        self.op = operation

        if string:
            assert isinstance(string, str)
            self.string = string
        elif expression1 and expression2:
            assert isinstance(expression1, RegEx)
            assert isinstance(expression2, RegEx)
            self.ex1 = expression1
            self.ex2 = expression2

    def __add__(self, other):
        """self, other -> (self + other)"""
        return RegEx(operation=RegExOperation.PLUS, expression1=self, expression2=other)

    def star(self):
        """self -> (self)*"""
        return RegEx(operation=RegExOperation.STAR, expression1=self)

    def __mul__(self, other):
        """self, other -> self.other"""
        return RegEx(operation=RegExOperation.CONCAT, expression1=self, expression2=other)

    def is_neutral(self):
        return self.op == RegExOperation.UNDEFINED and not self.string
