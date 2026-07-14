"""
2_explore_and_visualise.py
--------------------------

Step 2: explore the cleaned data with pandas and save charts as image files.

This answers the same kinds of questions as the SQL queries, but in Python.
Doing it both ways on purpose shows you can reach an answer with either tool,
which is a useful thing to be able to talk about.

Every chart is saved into the ../charts folder as a PNG image.

Input:  ../data/mpg_clean.csv
Output: PNG charts in ../charts/

Run it (after cleaning the data) with:
    python 2_explore_and_visualise.py
"""

import pandas as pd
import matplotlib

matplotlib.use("Agg")  # save charts to file without needing a screen
import matplotlib.pyplot as plt

CHART_DIR = "../charts"

cars = pd.read_csv("../data/mpg_clean.csv")
print(f"Loaded {len(cars)} clean rows.")

print("\nA few quick facts:")
print(f"  Model years: {sorted(cars['year'].unique())}")
print(f"  Vehicle classes: {cars['class'].nunique()}")
print(f"  Most efficient car: {cars.loc[cars['avg_mpg'].idxmax(), 'model']} "
      f"({cars['avg_mpg'].max()} mpg)")
print(f"  Least efficient car: {cars.loc[cars['avg_mpg'].idxmin(), 'model']} "
      f"({cars['avg_mpg'].min()} mpg)")


# ---------------------------------------------------------------------------
# Chart 1: Average economy by vehicle class.
# ---------------------------------------------------------------------------
by_class = cars.groupby("class")["avg_mpg"].mean().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
by_class.plot(kind="bar", color="#4C72B0")
plt.title("Average Fuel Economy by Vehicle Class")
plt.xlabel("Class")
plt.ylabel("Average mpg (city and highway)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/economy_by_class.png", dpi=120)
plt.close()
print("\nSaved chart: economy_by_class.png")


# ---------------------------------------------------------------------------
# Chart 2: Average economy by number of cylinders.
# ---------------------------------------------------------------------------
by_cyl = cars.groupby("cyl")["avg_mpg"].mean()

plt.figure(figsize=(8, 6))
by_cyl.plot(kind="bar", color="#55A868")
plt.title("Average Fuel Economy by Number of Cylinders")
plt.xlabel("Cylinders")
plt.ylabel("Average mpg")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/economy_by_cylinders.png", dpi=120)
plt.close()
print("Saved chart: economy_by_cylinders.png")


# ---------------------------------------------------------------------------
# Chart 3: Engine size against economy (a scatter plot).
# ---------------------------------------------------------------------------
# Each dot is one car. This shows the clear downward trend: bigger engines use
# more fuel. It also sets up the prediction model in the next script.
plt.figure(figsize=(9, 6))
plt.scatter(cars["displ"], cars["avg_mpg"], alpha=0.5, color="#C44E52")
plt.title("Engine Size vs Fuel Economy")
plt.xlabel("Engine size (litres)")
plt.ylabel("Average mpg")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/engine_size_vs_economy.png", dpi=120)
plt.close()
print("Saved chart: engine_size_vs_economy.png")


# ---------------------------------------------------------------------------
# Chart 4: Automatic versus manual.
# ---------------------------------------------------------------------------
by_trans = cars.groupby("transmission_type")["avg_mpg"].mean().sort_values(ascending=False)

plt.figure(figsize=(7, 6))
by_trans.plot(kind="bar", color=["#4C72B0", "#DD8452"])
plt.title("Average Fuel Economy: Automatic vs Manual")
plt.xlabel("Transmission type")
plt.ylabel("Average mpg")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/economy_by_transmission.png", dpi=120)
plt.close()
print("Saved chart: economy_by_transmission.png")


# ---------------------------------------------------------------------------
# Chart 5: Most efficient manufacturers (at least five cars each).
# ---------------------------------------------------------------------------
counts = cars["manufacturer"].value_counts()
big_makers = counts[counts >= 5].index
by_maker = (
    cars[cars["manufacturer"].isin(big_makers)]
    .groupby("manufacturer")["avg_mpg"].mean()
    .sort_values()
)

plt.figure(figsize=(10, 6))
by_maker.plot(kind="barh", color="#937860")
plt.title("Average Fuel Economy by Manufacturer (5 or more models)")
plt.xlabel("Average mpg")
plt.ylabel("Manufacturer")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/economy_by_manufacturer.png", dpi=120)
plt.close()
print("Saved chart: economy_by_manufacturer.png")

print("\nDone. All five charts are in the charts folder.")
