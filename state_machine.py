from config import REGEX_ALPHABET
from constants import EPSILON, NEUTRAL_ELEMENT
from regular_expression import RegEx, RegExOperation
from collections import defaultdict
from functools import reduce
from queue import Queue


class NDSMGraph:
    """Directional Graph data structure to access edges by key. Vertexes are ints. Start node is 0"""

    def __init__(self):
        self.graph = defaultdict(lambda x: defaultdict(set))
        self.nodes = set()
        self.finite_nodes = set()

    def add_edge(self, source, target, key):
        self.nodes.add(source)
        self.nodes.add(target)
        self.graph[source][key].add(target)

    def add_finite_node(self, node):
        self.finite_nodes.add(node)

    def is_finite_node(self, node):
        return node in self.finite_nodes

    def get_edges_form(self, source, key):
        return self.graph[source][key]

    def get_new_node(self):
        return len(self.nodes)

    def get_last_node(self):
        return len(self.nodes) - 1

    def get_reachable_nodes(self, node, symbol):
        """Return set of noted, that can be reached from node by passing by symbol and then by any number
        of EPSILON transactions"""
        in_processing = set()
        reachable_nodes = set()

        if symbol == EPSILON:
            in_processing.add(node)
        else:
            in_processing = self.get_edges_form(node, symbol)

        while in_processing:
            curr_node = in_processing.pop()
            reachable_nodes.add(curr_node)
            in_processing |= self.get_reachable_nodes(curr_node, EPSILON) - reachable_nodes

        return reachable_nodes

    def get_reachable_nodes_from(self, nodes, symbol):
        return reduce(lambda a, b: a | b, map(lambda node: self.get_reachable_nodes(node, symbol), nodes))

    def get_neighbors(self, node):
        return reduce(lambda a, b: a | b, self.graph[node].values())


class DSMGraph(NDSMGraph):
    def __init__(self):
        super(DSMGraph, self).__init__()

    def get_next_node(self, node, symbol):
        reachable_nodes = self.get_reachable_nodes(node, symbol)
        return reachable_nodes.pop() if reachable_nodes else None

    def is_exist_node(self, node: tuple):
        return node in self.nodes

    @classmethod
    def get_begin_node(cls):
        return 0,

    def n_moves(self, node, symbol, moves_count):
        for i in range(moves_count):
            node = self.get_next_node(node, symbol)
            if not node:
                return None
        return node

    def bfs(self, source, target):
        queue = Queue()
        queue.put((source, 0))
        used = set()
        while not queue.empty():
            curr_node = queue.get()
            used.add(curr_node[0])
            if curr_node == target:
                return curr_node[1]
            for node in self.get_neighbors(curr_node) - used:
                queue.put((node, curr_node[1] + 1))

        return None

    def distance_from_start(self, node):
        return self.bfs(self.get_begin_node(), node)

    def distance_to_finite(self, node):
        queue = Queue()
        queue.put((node, 0))
        used = set()
        while not queue.empty():
            curr_node = queue.get()
            used.add(curr_node[0])
            if self.is_finite_node(curr_node[0]):
                return curr_node[1]
            for node in self.get_neighbors(curr_node) - used:
                queue.put((node, curr_node[1] + 1))

        return None


class StateMachine:

    def __init__(self, regex: RegEx):
        """Initialize state machine from given regular expression
            NDSM - nondeterministic finite state machine
            DSM - deterministic finite state machine
            First build ndsm from regular expression
            Then generate dsm from ndsm
        """
        self.regex = regex

        # Nondeterministic finite state machine graph
        ndsm_graph = self._build_ndsm(regex)

        # Deterministic finite state machine graph
        self.graph = self._build_dsm(ndsm_graph)

    @classmethod
    def _build_ndsm(cls, regex: RegEx):
        graph = NDSMGraph()
        start_node = 0
        cls._parse_regex(graph, regex, start_node)
        graph.add_finite_node(graph.get_last_node())
        return graph

    @classmethod
    def _build_dsm(cls, ndsm_graph: NDSMGraph):
        graph = DSMGraph()
        graph.get_new_node()

        stack = list()
        stack.append(DSMGraph.get_begin_node())
        while stack:
            curr_node = stack.pop()
            is_finite = any(map(lambda node: ndsm_graph.is_finite_node(node), curr_node))
            if is_finite:
                graph.add_finite_node(curr_node)

            for sym in REGEX_ALPHABET:
                next_node = tuple(ndsm_graph.get_reachable_nodes_from(curr_node, sym))
                if next_node:
                    if not graph.is_exist_node(next_node):
                        stack.append(next_node)
                    graph.add_edge(curr_node, next_node, sym)

        return graph

    @classmethod
    def _parse_regex(cls, graph, regex, begin_node: int):
        end_node = graph.get_new_node()

        if regex.op == RegExOperation.PLUS:
            end_node1 = cls._parse_regex(graph, regex.ex1, begin_node)
            end_node2 = cls._parse_regex(graph, regex.ex2, begin_node)
            graph.add_edge(end_node1, end_node, EPSILON)
            graph.add_edge(end_node2, end_node, EPSILON)

        elif regex.op == RegExOperation.CONCAT:
            first_end_node = cls._parse_regex(graph, regex.ex1, begin_node)
            second_end_node = cls._parse_regex(graph, regex.ex2, first_end_node)
            graph.add_edge(second_end_node, end_node)

        elif regex.op == RegExOperation.STAR:
            reg_end_node = cls._parse_regex(graph, regex.ex1, begin_node)
            end_node = graph.get_new_node()
            graph.add_edge(reg_end_node, end_node, EPSILON)
            graph.add_edge(reg_end_node, begin_node, EPSILON)

        elif regex.is_neutral():
            graph.add_edge(begin_node, end_node, EPSILON)

        elif regex.op == RegExOperation.UNDEFINED:
            graph.add_edge(begin_node, end_node, regex.string)

        return end_node

    def find_particular_symbol_edges(self, symbol):
        return filter(lambda node: self.graph.get_next_node(node, symbol) is not None, self.graph.nodes)
