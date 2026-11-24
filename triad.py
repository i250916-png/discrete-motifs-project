# CS1005 Discrete Structures - Fall 2026 - Course Project
# R = 3259 (916 + 586 + 838 + 919)
# Member 2 (25I-0586): T3 triad_class + T4 count_triads
#
# Edge encoding (fixed by the handout). For an ordering (x0, x1, x2):
#   bit:  0     1     2     3     4     5
#   edge: 0->1  0->2  1->0  1->2  2->0  2->1
# canonical code of a triad = minimum 6-bit code over all 6 orderings.
# The 13 connected canonical codes, sorted ascending = Class 1..13.

from itertools import permutations, combinations

EDGE_BIT = {(0, 1): 0, (0, 2): 1, (1, 0): 2, (1, 2): 3, (2, 0): 4, (2, 1): 5}
CLASS_CODES = [3, 6, 7, 10, 11, 15, 21, 23, 25, 27, 30, 31, 63]
CODE_TO_CLASS = {code: k + 1 for k, code in enumerate(CLASS_CODES)}


def code_of_ordering(order, edge_set):
    """6-bit code of the triad when its nodes are read in the given order."""
    code = 0
    for (i, j), bit in EDGE_BIT.items():
        if (order[i], order[j]) in edge_set:
            code |= 1 << bit
    return code


def canonical_code(a, b, c, edge_set):
    """Minimum code over all 3! = 6 orderings of {a, b, c}."""
    return min(code_of_ordering(p, edge_set) for p in permutations((a, b, c)))


def triad_class(a, b, c, edge_set):
    """T3: class (1..13) of the triad on {a, b, c}, or None if it is not
    connected (canonical code not one of the 13 connected codes).
    edge_set is a set of directed edges (u, v)."""
    return CODE_TO_CLASS.get(canonical_code(a, b, c, edge_set))


def count_triads(edges):
    """T4: returns a list of 13 counts (Class 1..13).
    Every connected triple has a node adjacent to the other two, so for each
    node we take all pairs of its neighbours (in- or out-), store each triple
    as a sorted tuple in a set (removes duplicates), then classify it."""
    edge_set = set(edges)
    neighbours = {}
    for u, v in edge_set:
        if u == v:
            continue
        neighbours.setdefault(u, set()).add(v)
        neighbours.setdefault(v, set()).add(u)

    triples = set()
    for centre, ns in neighbours.items():
        for x, y in combinations(sorted(ns), 2):
            triples.add(tuple(sorted((centre, x, y))))

    counts = [0] * 13
    for a, b, c in triples:
        k = triad_class(a, b, c, edge_set)
        if k is not None:
            counts[k - 1] += 1
    return counts


def hand_example():
    """Hand-worked example for the video / README (T3)."""
    edge_set = {(10, 20), (20, 30), (30, 10), (20, 10)}
    print("Triad on nodes 10, 20, 30 with edges:", sorted(edge_set))
    for p in permutations((10, 20, 30)):
        print("  order", p, "-> code", code_of_ordering(p, edge_set))
    c = canonical_code(10, 20, 30, edge_set)
    print("Canonical (minimum) code =", c, "-> Class", CODE_TO_CLASS[c])


if __name__ == "__main__":
    hand_example()
