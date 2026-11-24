# CS1005 Discrete Structures - Fall 2026 - Course Project
# R = 3259 (916 + 586 + 838 + 919)
# Department pair number = 29 -> (1, 12) -> Department A = 4, Department B = 16
# Random networks = 24, swap attempts = 6 x edges, seed = 3259
#
# Member 4 (25I-0919): T6 - mean, population standard deviation, Z-scores,
# motif / anti-motif labels.   (T8 numbers are also printed here.)
#
# Inputs  : observed_counts.json    (Member 2, T4)
#           randomized_counts.json  (Member 3, T5)
# Outputs : zscores.json            (read by Member 1's chart function)
#           zscore_table.txt        (T6 table for README / video)
#
# Run: python member4_zscores.py

import json
import math

R = 3259
NUM_CLASSES = 13
NUM_NETWORKS = 24


def mean(values):
    """Arithmetic mean of a list of numbers."""
    return sum(values) / len(values)


def population_std(values):
    """Population standard deviation: sqrt( sum((x - mu)^2) / N ).
    N (not N-1) is used because the handout asks for the population SD."""
    mu = mean(values)
    variance = sum((x - mu) ** 2 for x in values) / len(values)
    return math.sqrt(variance)


def z_score(observed, mu, sigma):
    """Z = (observed - mu) / sigma.  If sigma == 0, report Z = 0 (handout rule)."""
    if sigma == 0:
        return 0.0
    return (observed - mu) / sigma


def label(z):
    """Motif if Z > 2, anti-motif if Z < -2, otherwise neither."""
    if z > 2:
        return "motif"
    if z < -2:
        return "anti-motif"
    return "-"


def compute_department(observed, random_vectors):
    """T6 for one department.
    observed       : list of 13 observed counts
    random_vectors : list of 24 lists, each with 13 counts
    Returns dict with mu, sigma, z and labels for all 13 classes."""
    assert len(observed) == NUM_CLASSES
    assert len(random_vectors) == NUM_NETWORKS
    assert all(len(v) == NUM_CLASSES for v in random_vectors)

    mus, sigmas, zs, labels = [], [], [], []

    for k in range(NUM_CLASSES):
        column = [vector[k] for vector in random_vectors]  # class k over the 24 networks
        mu = mean(column)
        sigma = population_std(column)
        z = z_score(observed[k], mu, sigma)

        mus.append(mu)
        sigmas.append(sigma)
        zs.append(z)
        labels.append(label(z))

    return {"mu": mus, "sigma": sigmas, "z": zs, "label": labels}


def self_test():
    """Small hand-checkable test of the three formulas."""
    values = [2, 4, 4, 4, 5, 5, 7, 9]          # classic example: mean 5, population SD 2
    assert mean(values) == 5
    assert population_std(values) == 2.0
    assert z_score(9, 5, 2.0) == 2.0           # exactly +2 is NOT a motif (needs Z > 2)
    assert label(2.0) == "-" and label(2.01) == "motif" and label(-2.01) == "anti-motif"
    assert z_score(10, 3, 0) == 0.0            # sigma = 0 -> Z = 0
    print("ok: mean / population SD / Z-score / sigma=0 rule / motif labels")


def main():
    self_test()

    with open("observed_counts.json") as f:
        observed = json.load(f)
    with open("randomized_counts.json") as f:
        randomized = json.load(f)

    results = {}
    lines = []

    header = "T6: Z-scores (R = %d)  |  %d random networks per department" % (R, NUM_NETWORKS)
    lines.append(header)

    for name in ["A", "B"]:
        dept_id = observed[name]["department_id"]
        assert dept_id == randomized[name]["department_id"]

        res = compute_department(observed[name]["counts"], randomized[name]["counts"])
        res["department_id"] = dept_id
        res["observed"] = observed[name]["counts"]
        results[name] = res

        lines.append("")
        lines.append("Department %s (ID %d)" % (name, dept_id))
        lines.append("%-6s %9s %10s %9s %9s  %s" %
                     ("Class", "Observed", "Mean", "Std", "Z", "Label"))
        for k in range(NUM_CLASSES):
            lines.append("%-6d %9d %10.2f %9.2f %9.2f  %s" %
                         (k + 1, res["observed"][k], res["mu"][k],
                          res["sigma"][k], res["z"][k], res["label"][k]))

        motifs = [k + 1 for k in range(NUM_CLASSES) if res["label"][k] == "motif"]
        antis = [k + 1 for k in range(NUM_CLASSES) if res["label"][k] == "anti-motif"]
        lines.append("Motifs (Z > 2):       classes %s" % motifs)
        lines.append("Anti-motifs (Z < -2): classes %s" % antis)

    text = "\n".join(lines)
    print(text)

    with open("zscore_table.txt", "w") as f:
        f.write(text + "\n")
    with open("zscores.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved zscores.json and zscore_table.txt")


if __name__ == "__main__":
    main()
