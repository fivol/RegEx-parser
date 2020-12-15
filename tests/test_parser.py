from regexparser.parser import RegExParser
from regexparser.state_machine import *


def string_solution(input_string):
    alpha, x, k = input_string.split()
    parser = RegExParser(alpha)
    return parser.get_min_length_with_substring(x, int(k))


def test_example():
    assert string_solution('ab+c.aba.*.bac.+.+∗ b 2') == 4
    assert string_solution('acb..bab.c.∗.ab.ba.+.+∗a. b 3') == 7


def test_other_examples():
    assert string_solution('a a 1') == 1
    assert string_solution('abc.. a 1') == 3
    assert string_solution('abb.+ b 2') == 2
    assert string_solution('ab.b. b 2') == 3
    assert string_solution('aaaa... a 3') == 4
    assert string_solution('ab.bba..+* b 3') == 5
    assert string_solution('aa.aaaa...+* a 5') == 6
    assert string_solution('ab.b. c 2') is None
    assert string_solution('b* a 1') is None
    assert string_solution('a b 1') is None


def build_ndsm(regex_str):
    parser = RegExParser(regex_str)
    return StateMachine(parser.regex)._build_ndsm(parser.regex)


def test_dsm():
    g = build_ndsm('a*')
    assert len(g.nodes) == g.nodes_pointer
    assert 4 == g.nodes_pointer
    assert g.finite_nodes == {1}

    g = build_ndsm('ab.*')
    assert len(g.nodes) == g.nodes_pointer
    assert 6 == g.nodes_pointer
    assert g.finite_nodes == {1}


def test_ndsm():
    assert StateMachine._build_dsm(build_ndsm('b*')).start_node == (0, 1, 2)
    assert StateMachine._build_dsm(build_ndsm('b*')).start_node == (0, 1, 2)
    assert len(StateMachine._build_dsm(build_ndsm('b*')).nodes) == 2
    assert StateMachine._build_dsm(build_ndsm('ab.c+')).start_node == (0, )
    assert len(StateMachine._build_dsm(build_ndsm('ab.c+*')).nodes) == 4
