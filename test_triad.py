# Tests for T3 and T4 (Member 2). Run: python test_triad.py
import random
from itertools import permutations, combinations
from triad import triad_class, count_triads, CLASS_CODES, EDGE_BIT, canonical_code


def test_all_64_configs():
    """64 configurations -> 16 orbits -> 13 connected classes."""
    pos = list(EDGE_BIT)
    orbits, connected = set(), set()
    for code in range(64):
        es = {e for e, b in EDGE_BIT.items() if code >> b & 1}
        orbits.add(canonical_code(0, 1, 2, es))
        und = {frozenset(e) for e in es}
        # connected iff at least 2 distinct undirected pairs
        if len(und) >= 2:
            connected.add(canonical_code(0, 1, 2, es))
    assert len(orbits) == 16, len(orbits)
    assert sorted(connected) == CLASS_CODES
    print("ok: 64 -> 16 orbits -> 13 connected classes")


def test_known_classes():
    assert triad_class(0, 1, 2, {(0, 1), (0, 2)}) == 1      # code 3
    assert triad_class(0, 1, 2, {(0, 1), (1, 2), (0, 2)}) in range(1, 14)
    full = {(a, b) for a in range(3) for b in range(3) if a != b}
    assert triad_class(0, 1, 2, full) == 13                  # code 63
    assert triad_class(0, 1, 2, {(0, 1)}) is None            # not connected
    assert triad_class(0, 1, 2, set()) is None
    print("ok: known classes")


def test_order_independent():
    es = {(0, 1), (1, 2), (2, 0), (1, 0)}
    vals = {triad_class(*p, es) for p in permutations((0, 1, 2))}
    assert len(vals) == 1
    print("ok: order independent")


def brute(edges, n):
    es = set(edges)
    counts = [0] * 13
    for a, b, c in combinations(range(n), 3):
        k = triad_class(a, b, c, es)
        if k:
            counts[k - 1] += 1
    return counts


def test_count_vs_bruteforce():
    rnd = random.Random(1)
    for _ in range(200):
        n = rnd.randint(3, 9)
        edges = {(rnd.randrange(n), rnd.randrange(n)) for _ in range(rnd.randint(0, 25))}
        edges = [e for e in edges if e[0] != e[1]]
        assert count_triads(edges) == brute(edges, n)
    print("ok: count_triads == brute force on 200 random graphs")


def test_small():
    assert count_triads([(0, 1), (0, 2)]) == [1] + [0] * 12
    assert count_triads([(0, 1)]) == [0] * 13          # disconnected triples
    assert count_triads([]) == [0] * 13
    # duplicate prevention: complete graph on 3 nodes counted once
    full = [(a, b) for a in range(3) for b in range(3) if a != b]
    assert count_triads(full) == [0] * 12 + [1]
    print("ok: small cases")


if __name__ == "__main__":
    test_all_64_configs()
    test_known_classes()
    test_order_independent()
    test_small()
    test_count_vs_bruteforce()
    print("ALL TESTS PASSED")
