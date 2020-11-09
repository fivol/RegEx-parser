from regexparser.config import REGEX_ALPHABET
from regexparser.constants import NEUTRAL_ELEMENT
from regexparser.exceptions import IncorrectRegularExpression
from regexparser.regular_expression import RegEx
from regexparser.state_machine import StateMachine


class RegExParser:
    alphabet = REGEX_ALPHABET

    def __init__(self, regex_string: str):
        self.regex_string = regex_string.replace(' ', '')
        self.regex = self._parse_exp_string(self.regex_string)
        self.state_machine = StateMachine(self.regex)

    def get_min_length_with_substring(self, symbol: str, power: int) -> int:
        """Find answer to the task - this can be represented as
        min[len(word) for word in L(regex_string) if symbol**power in word]"""

        assert power >= 0
        if power == 0:
            return 0

        min_word_length = None
        x_begins = self.state_machine.find_particular_symbol_edges(symbol)
        for x_begin in x_begins:
            n_moves_end = self.state_machine.graph.n_moves(x_begin, symbol, power)
            if n_moves_end:
                # x_begin - node where sequence of symbol**power begin
                # n_moved_end - node after sequence of SYMBOL chars
                distance_before = self.state_machine.graph.distance_from_start(x_begin)
                distance_after = self.state_machine.graph.distance_to_finite(n_moves_end)
                # logger.info('%s, %s, %s, %s', x_begin, n_moves_end, distance_before, distance_after)

                word_length = distance_before + power + distance_after
                if min_word_length is None or word_length < min_word_length:
                    min_word_length = word_length

        return min_word_length

    @classmethod
    def _parse_exp_string(cls, regex_string) -> RegEx:
        stack = []
        for i, c in enumerate(regex_string):
            if c in cls.alphabet or c == NEUTRAL_ELEMENT:
                stack.append(RegEx(c))
            elif c == '+':
                ex2 = stack.pop()
                ex1 = stack.pop()
                stack.append(ex1 + ex2)
            elif c == '.':
                ex2 = stack.pop()
                ex1 = stack.pop()
                stack.append(ex1 * ex2)
            elif c in '*∗':
                ex = stack.pop()
                stack.append(ex.star())

        if len(stack) != 1:
            raise IncorrectRegularExpression

        return stack[0]
