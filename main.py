from parser import RegExParser


def read_input_data() -> (str, str, int):
    """Read input parameters for task solution
    alpha - regex in alphabet {a, b, c, 1, ., +, *}
    x - char
    k - natural number
    returns (alpha, x, k)"""

    # text = input()

    with open('input.txt', 'r') as f:
        text = f.read()

    alpha, x, k = text.split()
    k = int(k)
    assert isinstance(x, str)
    assert len(alpha) > 0
    return alpha, x, k


def solution():
    alpha, x, k = read_input_data()

    parser = RegExParser(alpha)
    length = parser.get_min_length_with_substring(x, k)

    print(length)


if __name__ == '__main__':
    solution()
