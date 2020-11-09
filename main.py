from regexparser.constants import WRONG_ANSWER_MESSAGE, ERROR_MESSAGE
from regexparser.exceptions import IncorrectRegularExpression
from regexparser.parser import RegExParser


def read_input_data() -> (str, str, int):
    """Read input parameters for task solution
    alpha - regex in alphabet {a, b, c, 1, ., +, *}
    x - char
    k - natural number
    returns (alpha, x, k)"""

    # text = input()

    with open('regexparser/input.txt', 'r') as f:
        text = f.read()

    alpha, x, k = text.split()
    k = int(k)
    assert isinstance(x, str)
    assert len(alpha) > 0
    return alpha, x, k


def solution():
    alpha, x, k = read_input_data()

    try:
        parser = RegExParser(alpha)
        length = parser.get_min_length_with_substring(x, k)
        if length is None:
            print(WRONG_ANSWER_MESSAGE)
        else:
            print(length)
    except IncorrectRegularExpression:
        print(ERROR_MESSAGE)


if __name__ == '__main__':
    solution()
