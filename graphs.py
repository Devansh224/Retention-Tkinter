import matplotlib.pyplot as plt
import numpy as np
'''
# Time axis (days after learning)
days = np.arange(0, 30, 1)

# Forgetting curve (exponential decay)
retention = np.exp(-0.1 * days) * 100

# Optional: curve with reinforcement (active recall)
# reinforced = np.exp(-0.05 * days) * 100

plt.figure(figsize=(8,5))
plt.plot(days, retention, label="Without Active Recall", color="red", linewidth=2)
# plt.plot(days, reinforced, label="With Active Recall", color="green", linestyle="--", linewidth=2)

# Adjusted annotation to avoid overlap
plt.annotate(
    "Rapid decline in memory",
    xy=(5, retention[5]),            # point on red curve
    xytext=(12, 85),                 # label placed higher to avoid green line
    arrowprops=dict(facecolor="black", arrowstyle="->"),
    fontsize=12,
    color="red"
)

plt.title("The Forgetting Curve", fontsize=14)
plt.xlabel("Days After Learning", fontsize=12)
plt.ylabel("Memory Retention (%)", fontsize=12)
plt.ylim(0, 100)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.show()
'''

'''

# Time axis: 0 to 21 days (3 weeks)
days = np.arange(0, 22)

# Base forgetting curve (no recall)
base_retention = np.exp(-0.15 * days) * 100

# Function to simulate recall bump continuing from base curve
def recall_bump(start_day, decay_rate, boost=95):
    bump = base_retention.copy()
    # At recall, boost retention
    bump[start_day] = boost
    # After recall, decay from boosted level
    bump[start_day+1:] = boost * np.exp(-decay_rate * (days[start_day+1:] - start_day))
    return bump

# First and second recalls
recall1 = recall_bump(5, 0.12, boost=95)
recall2 = recall_bump(12, 0.10, boost=90)

# Plotting
plt.figure(figsize=(10,6))


# Overlay recall curves on top
plt.plot(days, recall1, label="1st Recall", color="blue", linestyle='dashed', linewidth=2, zorder=2)
plt.plot(days, recall2, label="2nd Recall", color="green", linestyle='dashdot', linewidth=2, zorder=3)
# Plot base curve first (so it's always visible underneath)
plt.plot(days, base_retention, label="No Recall", color="black", linestyle='solid', linewidth=2, zorder=1)

plt.title("Memory Retention with Spaced Active Recall", fontsize=14)
plt.xlabel("Days After Learning", fontsize=12)
plt.ylabel("Memory Retention (%)", fontsize=12)
plt.ylim(0, 110)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()

plt.tight_layout()
plt.show()

'''

import networkx as nx

# Define flowchart structure
edges = [
    ("Flashcard", "Due Soon"),
    ("Due Soon", "Student Attempts Recall"),
    ("Student Attempts Recall", "Correct"),
    ("Student Attempts Recall", "Incorrect"),
    ("Correct", "Next Interval"),
    ("Incorrect", "Reset to Short Gap"),
    ("Next Interval", "Mastered"),
    ("Reset to Short Gap", "Due Soon")
]

# Create directed graph
G = nx.DiGraph()
G.add_edges_from(edges)

# Layout for flowchart
pos = nx.spring_layout(G, seed=42)

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_size=3000, node_color="lightblue")
nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")

# Draw edges
nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=20)

plt.title("Active Recall Algorithm Flowchart", fontsize=14)
plt.axis("off")
plt.show()
