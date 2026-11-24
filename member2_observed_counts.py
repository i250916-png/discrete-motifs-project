# Member 2 (25I-0586): T4 observed counts for both departments.
# Also checks the counts with nx.triadic_census (CHECK ONLY - not used for the
# counting itself; its class order differs from our Class 1-13 order).
# Run: python member2_observed_counts.py

import json
from part1_data import main as load_project
from triad import count_triads, CLASS_CODES, EDGE_BIT

R = 3259


def nx_check(edges, counts):
    import networkx as nx
    # Map each of our classes to an nx triad name using a representative graph.
    name_of_class = {}
    for k, code in enumerate(CLASS_CODES):
        g = nx.DiGraph()
        g.add_nodes_from(range(3))
        g.add_edges_from(e for e, b in EDGE_BIT.items() if code >> b & 1)
        census = nx.triadic_census(g)
        name_of_class[k] = [n for n, v in census.items() if v == 1][0]
    g = nx.DiGraph()
    g.add_edges_from(edges)
    census = nx.triadic_census(g)
    nx_counts = [census[name_of_class[k]] for k in range(13)]
    return nx_counts


def main():
    data = load_project()
    out = {}
    print("\nT4: Observed triad counts (R = %d)" % R)
    for name in ["A", "B"]:
        d = data["departments"][name]
        counts = count_triads(d["edges"])
        out[name] = {"department_id": d["department_id"], "counts": counts}
        print("\nDepartment %s (ID %d): %d nodes, %d edges" %
              (name, d["department_id"], len(d["nodes"]), len(d["edges"])))
        for k, c in enumerate(counts, 1):
            print("  Class %2d (code %2d): %d" % (k, CLASS_CODES[k - 1], c))
        try:
            nx_counts = nx_check(d["edges"], counts)
            print("  nx.triadic_census check (check only):",
                  "MATCH" if nx_counts == counts else "MISMATCH " + str(nx_counts))
        except ImportError:
            print("  (networkx not installed, check skipped)")
    with open("observed_counts.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nSaved observed_counts.json")


if __name__ == "__main__":
    main()
