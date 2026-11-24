# CS1005 Discrete Structures - Fall 2026 - Course Project
# R = 3259
# Member 4 (25I-0919): feeds the REAL Z-scores from zscores.json into
# Member 1's make_chart() (T7). Run member4_zscores.py first.
import json
import matplotlib
matplotlib.use("Agg")          # save to file only, no window needed
from part1_chart import make_chart

with open("zscores.json") as f:
    z = json.load(f)

make_chart(z["A"]["z"], z["B"]["z"], z["A"]["department_id"], z["B"]["department_id"],
           r=3259, filename="z_score_chart.png")
