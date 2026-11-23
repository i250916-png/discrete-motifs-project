# CS1005 Discrete Structures – Fall 2026
## Finding Network Motifs in an Email Network

## Group Responsibilities

| Member | Roll Number | Tasks |
|---|---|---|
| Member 1 | 25I-0916 | T1, T2, T7 / chart function |
| Member 2 | 25I-0586 | T3, T4 / triad classification and observed counts |
| Member 3 | 25I-0838 | T5 / directed double-edge-swap randomization |
| Member 4 | 25I-0919 | T6, T8 / Z-scores and interpretation |

## Project Parameters

- **R** = 916 + 586 + 838 + 919 = **3259**
- Pair number: 3259 mod 190 = 29 → **(1, 12)**
- Department A = **4**
- Department B = **16**
- Random networks per department = **24**
- Swap attempts per randomized network = **6 × number of edges in the department**
- Random seed = **3259**

## Dataset

We used the SNAP Email-Eu-core dataset, which contains email communication between members of a university.

Original graph:
- Nodes: 1005
- Directed edges: 25571

After cleaning:
- Nodes: 1005
- Directed edges: 24929
- Departments: 42

We removed self-loops and duplicate directed edges before performing our analysis.

Dataset source: https://snap.stanford.edu/data/email-Eu-core.html

## Files

| File | Description |
|---|---|
| `email-Eu-core.txt.gz`, `email-Eu-core-department-labels.txt.gz` | Input dataset |
| `part1_data.py` | Dataset cleaning, parameters, and department subgraphs (T1/T2) |
| `part1_chart.py` | Chart function used for the Z-score chart (T7) |
| `triad.py`, `test_triad.py` | Triad classification, counting, and tests (T3) |
| `member2_observed_counts.py`, `observed_counts.json` | Observed triad counts and NetworkX verification (T4) |
| `randomize.py`, `test_randomize.py` | Directed edge-swap randomization and tests (T5) |
| `member3_randomized_runs.py`, `randomized_counts.json` | 24 randomized networks per department (T5) |
| `member4_zscores.py`, `zscores.json`, `zscore_table.txt` | Mean, population standard deviation, Z-scores, and labels (T6) |
| `member4_make_chart.py`, `z_score_chart.png` | Chart generated from the real Z-scores (T7) |
| `t8_comparison.md` | Written comparison of the two departments (T8) |

## Setup

Python 3 is required. The project uses NetworkX and Matplotlib.

Install the required libraries if needed:

```bash
python -m pip install networkx matplotlib
```

On Windows, use `py` instead of `python` if `python` is not found.

## How to Run the Project

Run the commands from inside the `motif_project` folder, in the following order:

```bash
python part1_data.py
python test_triad.py
python triad.py
python member2_observed_counts.py
python test_randomize.py
python member3_randomized_runs.py
python member4_zscores.py
python member4_make_chart.py
```

On Windows, if `python` is not recognized, use `py` in place of `python` in the commands above.

`member2_observed_counts.py` and `member3_randomized_runs.py` also call the data preparation code as needed.

Run `member3_randomized_runs.py` before `member4_zscores.py`, because T6 reads `randomized_counts.json`.

Run `member4_zscores.py` before `member4_make_chart.py`, because the chart uses `zscores.json`.

## T1 – Data Loading and Cleaning

We loaded the directed email network and the department labels. We removed self-loops and duplicate directed edges to prepare a clean graph for the analysis.

The cleaned graph contains 1005 nodes and 24929 directed edges across 42 departments.

## T2 – Department Subgraphs

We counted the internal directed edges for each department and ranked the departments in descending order. In case of a tie, the department with the smaller ID was ranked first.

The top 20 departments were indexed from 0 to 19. The selected department pair was determined using our value of R.

| Selected Department | Department ID | Nodes | Internal Edges |
|---|---:|---:|---:|
| Department A | 4 | 109 | 1167 |
| Department B | 16 | 25 | 236 |

We extracted the induced subgraphs of Departments 4 and 16, keeping the directed edges between members of each selected department.

## T3 – Triad Classification

A triad is a group of three nodes and the directed connections between them. We classified triads into 13 possible directed triad classes.

For each triad, we represented the six possible directed edges using a six-bit code. We calculated the code for all six possible node orderings and selected the smallest code as the canonical code. This canonical code was then mapped to one of the 13 triad classes.

### Hand-Worked Example

Nodes: 10, 20, 30

Edges:
- 10 → 20
- 20 → 10
- 20 → 30
- 30 → 10

For the ordering (20, 30, 10), the six-bit code is 011011, which gives:

The code is: 1 + 2 + 8 + 16 = 27

We calculated the code for all six node orderings:

| Node Ordering | Code |
|---|---:|
| (10, 20, 30) | 29 |
| (10, 30, 20) | 54 |
| (20, 10, 30) | 39 |
| (20, 30, 10) | 27 |
| (30, 10, 20) | 57 |
| (30, 20, 10) | 46 |

The smallest code is 27, so the canonical code is 27. This corresponds to **Class 10**.

The triad classification is independent of the original node ordering because the smallest code among all six orderings is used.

## T4 – Observed Triad Counts

We counted all 13 triad classes in the observed department networks.

For each node, we generated candidate triads using pairs of its neighbours instead of checking all possible combinations of three nodes. Candidate triads were counted once, and duplicates were removed.

The observed triad counts were verified against NetworkX's triadic census for both selected departments.

## T5 – Random Network Generation

We generated randomized networks using directed double-edge swaps.

In each swap, two directed edges (a, b) and (c, d) are selected and replaced with (a, d) and (c, b).

A swap is rejected if it creates a self-loop or if either of the new edges already exists in the graph. Rejected attempts are counted.

In a successful swap, edges (a, b) and (c, d) are removed and (a, d) and (c, b) are added. Nodes a and c each lose one outgoing edge and gain one outgoing edge, so their out-degrees stay the same. Nodes b and d each lose one incoming edge and gain one incoming edge, so their in-degrees stay the same.

One random generator was created once with seed 3259 and reused for all randomized networks of both departments, so the networks are different from each other.

Each randomized network starts from a fresh copy of the original department graph. We generated 24 randomized networks for each department, using 6 × the department's number of edges as swap attempts per network.

## T6 – Z-Score Calculation

We calculated the Z-score using this formula:

```text
Z = (Observed - Mean) / Standard Deviation
```

- **Observed** is the count in the real department network.
- **Mean** is the average count over the 24 randomized networks.
- **Standard Deviation** shows how much the random counts vary around that average.

Z tells us how many standard deviations the real count is above or below what we expect by chance.

**Example:** Department 4, Class 8. Observed = 3,498, Mean = 916.96, Standard Deviation = 99.83.

Z = (3498 - 916.96) / 99.83 = 25.85

This means the real network has far more of this triad than random networks do.

We used the population standard deviation of the 24 randomized counts. If the standard deviation was zero, the Z-score was set to zero.

- **Motif:** Z > 2
- **Anti-motif:** Z < −2
- Otherwise, the triad was considered neither a motif nor an anti-motif.

## T7 – Z-Score Visualization

We created a grouped bar chart comparing the Z-scores of the 13 triad classes for Departments 4 and 16.

The chart includes:
- Separate bars for the two departments.
- Triad classes 1–13 on the x-axis.
- Z-scores on the y-axis.
- Dashed horizontal reference lines at Z = +2 and Z = −2.
- A legend showing the department IDs.

The chart title contains **R = 3259**, and the legend shows the department IDs.

The chart was generated using the actual Z-scores calculated in T6.

## T8 – Comparison of the Two Departments

The two departments showed different triad patterns when compared with their randomized networks. Department 4 had some triad classes that were strongly overrepresented and others that were underrepresented. Department 16 had Z-scores closer to zero for most classes, meaning its observed counts were generally closer to what we expected in randomized networks. The anti-motif triads have no two-way pairs or only one, which suggests that these one-way communication patterns were less common than expected in Department 4. Overall, the results show that the two departments had different communication patterns.

## Verification Performed

The following checks were performed on the combined project:

- `test_triad.py`: all test groups passed, including comparison with brute force on 200 random graphs.
- `test_randomize.py`: all test groups passed, including in-/out-degree preservation and reproducibility checks.
- `member2_observed_counts.py`: NetworkX triadic-census verification reported `MATCH` for Departments 4 and 16.
- `member3_randomized_runs.py`: completed 24 randomized runs for each department and saved `randomized_counts.json`.
- `member4_zscores.py`: self-tests passed and generated Z-score results.
- `member4_make_chart.py`: generated `z_score_chart.png`.
