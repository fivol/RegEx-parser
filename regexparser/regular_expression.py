from enum import Enum


class RegExOperation(Enum):
    PLUS = '+'
    CONCAT = '.'
    STAR = '*'
    UNDEFINED = '@'


class RegEx:
    def __init__(self, string=None, operation=RegExOperation.UNDEFINED, expression1=None, expression2=None):
        assert isinstance(operation, RegExOperation)
        if string:
            assert isinstance(string, str)
        if expression1:
            assert isinstance(expression1, RegEx)
        if expression2:
            assert isinstance(expression2, RegEx)
        self.string = None
        self.op = operation
        self.string = string
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

    def __repr__(self):
        if self.op == RegExOperation.UNDEFINED:
            return self.string
        if self.op == RegExOperation.STAR:
            return f'({self.ex1})*'
        if self.op == RegExOperation.PLUS:
            return f'({self.ex1} + {self.ex2})' \
                   f''
        if self.op == RegExOperation.CONCAT:
            return f'{self.ex1}{self.ex2}'
