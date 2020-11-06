from enum import Enum
from string import ascii_lowercase


class RegExOperation(Enum):
    PLUS = '+'
    CONCAT = '.'
    STAR = '*'
    UNDEFINED = '@'


class RegEx:
    def __init__(self, string=None, operation=None, expression1=None, expression2=None):
        assert isinstance(operation, RegExOperation)

        self.string = None
        self.ex1 = None
        self.ex2 = None
        self.op = None

        if string:
            assert isinstance(string, str)
            self.string = string
        elif expression1 and expression2:
            assert isinstance(expression1, RegEx)
            assert isinstance(expression2, RegEx)
            self.ex1 = expression1
            self.ex2 = expression2

    def get_min_length_containing_char_power(self, char: str, power: int) -> int:
        """Returns length of min word containing char^power, if does not exist - 0"""
        assert power > 0

        if self.op == RegExOperation.PLUS:
            ex1_res = self.ex1.get_min_length_containing_char_power(char, power)
            ex2_res = self.ex2.get_min_length_containing_char_power(char, power)
            if ex1_res and ex2_res:
                return min(ex1_res, ex2_res)
            return ex1_res if not ex2_res else ex2_res

        if self.op == RegExOperation.STAR:
            plain_result = self.ex2.get_min_length_containing_char_power
            single_len = self.ex1.min_word_fits_char_plus(char)
            if power % single_len == 0:
                return power
            return self.get_min_length_containing_char_power(char, power - single_len) + power
        elif self.op == RegExOperation.STAR:
            pass

    def _distributor(self, func):
        """Wraps function that returns dict with lambda funcs. Execute suitable by self.op"""
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            assert isinstance(result, dict)
            return result[self.op]()

        return wrapper

    @_distributor
    def is_fits_eps(self):
        """Check if lang by this expr contains epsilon (empty word). Return bool after decoration"""
        return {
            RegExOperation.CONCAT: lambda x: self.ex1.is_fits_eps() and self.ex2.is_fits_eps(),
            RegExOperation.PLUS: lambda x: self.ex1.is_fits_eps() or self.ex2.is_fits_eps(),
            RegExOperation.STAR: lambda x: True,
        }

    def min_word_fits_char_plus(self, char) -> int:
        """Return 0 if there no words with repeating > 0 chars (char+)
                otherwise minimum of word length owned by language containing char+"""
        if self.op == RegExOperation.STAR:
            return self.ex1.min_word_fits_char_plus(char)
        if self.op == RegExOperation.PLUS:
            ex1_res = self.ex1.min_word_fits_char_plus(char)
            ex2_res = self.ex2.min_word_fits_char_plus(char)
            if ex1_res and ex2_res:
                return min(ex1_res, ex2_res)
            return ex1_res if not ex2_res else ex2_res
        if self.op == RegExOperation.CONCAT:
            ex1_res = self.ex1.min_word_fits_char_plus(char)
            ex2_res = self.ex2.min_word_fits_char_plus(char)
            if ex1_res and ex2_res:
                return ex1_res + ex2_res
            if ex1_res and self.ex2.is_fits_eps():
                return ex1_res
            return ex2_res

        return int(self.string == char)


class RegExParser:
    alphabet = set(ascii_lowercase)

    def __init__(self, exp_str: str, alphabet=None):
        if alphabet:
            assert isinstance(alphabet, set)
            self.alphabet = alphabet
        self.exp_str = exp_str
        self.reg_exp = None
        self._parse_exp_string()

    def get_min_length_with_substring(self, char: str, power: int) -> int:
        assert power >= 0
        if power == 0:
            return 0
        return self.reg_exp.get_min_length_containing_char_power(char, power)

    def _parse_exp_string(self):
        exp = RegEx()
        for i, c in enumerate(self.exp_str):
            if c in self.alphabet:
                exp += RegEx(c)
