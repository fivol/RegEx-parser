from regexparser.parser import RegExParser


def string_solution(input_string):
    alpha, x, k = input_string.split()
    parser = RegExParser(alpha)
    return parser.get_min_length_with_substring(x, int(k))


def test_example():
    assert string_solution('ab+c.aba.*.bac.+.+∗ b 2') == 4
    assert string_solution('acb..bab.c.∗.ab.ba.+.+∗a. b 3') == 7


def test_other_examples():
    assert string_solution('abc.. a 1') == 3
    assert string_solution('abb.+ b 2') == 2
    assert string_solution('ab.b. b 2') == 3
    assert string_solution('ab.b. c 2') is None
    assert string_solution('b* a 1') is None
    assert string_solution('ab.bba..+* b 3') == 5
    assert string_solution('a b 1') is None
    assert string_solution('a a 1') == 1
    assert string_solution('aaaa... a 3') == 4
    assert string_solution('aa.aaaa...+* a 5') == 6
