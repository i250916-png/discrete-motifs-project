
import matplotlib.pyplot as plt

R = 3259


# Draw Z-scores for both selected departments
def make_chart(z_a, z_b, dept_a, dept_b, r=R, filename="z_score_chart.png", note=""):
    classes = list(range(1, 14))

    bar_width = 0.38

    x_a = [c - bar_width / 2 for c in classes]
    x_b = [c + bar_width / 2 for c in classes]

    plt.figure(figsize=(11, 6))

    plt.bar(x_a, z_a, width=bar_width, label=f"Department A ({dept_a})", color="#2E5597")
    plt.bar(x_b, z_b, width=bar_width, label=f"Department B ({dept_b})", color="#E07B39")

    plt.axhline(2, color="red", linestyle="--", linewidth=1.2, label="Z = +2 (motif)")
    plt.axhline(-2, color="green", linestyle="--", linewidth=1.2, label="Z = -2 (anti-motif)")
    plt.axhline(0, color="black", linewidth=0.8)

    plt.xticks(classes)
    plt.xlabel("Triad class")
    plt.ylabel("Z-score")
    plt.title(f"Network motif Z-scores, R = {r}{note}")

    plt.legend()
    plt.tight_layout()

    plt.savefig(filename, dpi=150)
    print("Chart saved as", filename)
    plt.show()


# Test the chart using sample data
if __name__ == "__main__":
    fake_z_a = [5.1, -3.2, 0.4, 8.0, -1.1, 2.6, -0.5, 12.3, 3.3, -2.4, 0.9, 6.7, 15.0]
    fake_z_b = [-1.5, 4.2, 1.1, -2.8, 3.5, -0.3, 2.2, 7.4, -3.9, 1.8, -0.7, 9.1, 11.2]

    make_chart(fake_z_a, fake_z_b, 4, 16, filename="test_chart.png", note=" (TEST DATA)")
