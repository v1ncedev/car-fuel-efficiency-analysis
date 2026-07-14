"""
3_predict_mpg.py
----------------

Step 3: build a simple model that predicts a car's fuel economy from two facts
about it: its engine size and its number of cylinders.

This is a linear regression. The idea is easy to picture: we find the straight
line (really a flat surface, because we use two inputs) that comes as close as
possible to all the real data points. "As close as possible" means the line
that makes the total squared gap between predictions and reality as small as it
can be. That is the whole idea behind least squares, which is what we use here.

We build it with numpy rather than a machine learning library on purpose, so
that nothing is hidden. Every step below is something you can explain.

Input:  ../data/mpg_clean.csv
Output: prints the model and its accuracy, and saves one chart.

Run it (after cleaning the data) with:
    python 3_predict_mpg.py
"""

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

CHART_DIR = "../charts"

cars = pd.read_csv("../data/mpg_clean.csv")

# ---------------------------------------------------------------------------
# 1. Choose the inputs and the target.
# ---------------------------------------------------------------------------
# Inputs (the things we know about a car): engine size and cylinder count.
# Target (the thing we want to predict): average miles per gallon.
X_inputs = cars[["displ", "cyl"]].values
y_target = cars["avg_mpg"].values

# ---------------------------------------------------------------------------
# 2. Set up the maths.
# ---------------------------------------------------------------------------
# A linear model looks like:
#     predicted_mpg = b0 + b1 * displ + b2 * cyl
# b0 is the starting value, and b1 and b2 say how much mpg changes for each unit
# of engine size and each extra cylinder. To let the model learn b0, we add a
# column of ones to the inputs. This is a standard trick.
ones = np.ones((len(cars), 1))
X = np.hstack([ones, X_inputs])   # columns are: [1, displ, cyl]

# numpy's least squares solver finds the b0, b1, b2 that fit the data best.
coefficients, _, _, _ = np.linalg.lstsq(X, y_target, rcond=None)
b0, b1, b2 = coefficients

print("The model learned this formula:")
print(f"  predicted_mpg = {b0:.2f} + ({b1:.2f} x engine_litres) + ({b2:.2f} x cylinders)")
print()
print("In plain English:")
print(f"  - Start from about {b0:.1f} mpg.")
print(f"  - Every extra litre of engine size changes it by about {b1:.1f} mpg.")
print(f"  - Every extra cylinder changes it by about {b2:.1f} mpg.")
print("  (Engine size and cylinders rise together, so they share the credit.)")

# ---------------------------------------------------------------------------
# 3. Measure how good the model is.
# ---------------------------------------------------------------------------
# We compare the model's predictions to the real values.
predictions = X @ coefficients

# R squared tells us the share of the variation in mpg that the model explains.
# It runs from 0 (useless) to 1 (perfect). We work it out from the errors.
errors = y_target - predictions
ss_residual = np.sum(errors ** 2)                       # how far off we were
ss_total = np.sum((y_target - y_target.mean()) ** 2)    # variation to explain
r_squared = 1 - ss_residual / ss_total

# The typical size of a prediction error, in mpg, is easier to picture than R2.
average_error = np.mean(np.abs(errors))

print()
print(f"R squared: {r_squared:.2f}  (share of the variation the model explains)")
print(f"Typical prediction error: {average_error:.1f} mpg")

# ---------------------------------------------------------------------------
# 4. Try the model on an example.
# ---------------------------------------------------------------------------
# A 2 litre, 4 cylinder car (a typical small family car).
example = np.array([1, 2.0, 4])
predicted = example @ coefficients
print()
print(f"Example: a 2.0 litre, 4 cylinder car is predicted to do "
      f"{predicted:.1f} mpg on average.")

# ---------------------------------------------------------------------------
# 5. Save a chart of predicted versus actual.
# ---------------------------------------------------------------------------
# If the model were perfect, every dot would sit on the diagonal line. The
# closer the dots hug that line, the better the model.
plt.figure(figsize=(8, 8))
plt.scatter(y_target, predictions, alpha=0.5, color="#4C72B0")
limits = [y_target.min() - 2, y_target.max() + 2]
plt.plot(limits, limits, color="#C44E52", linestyle="--", label="perfect prediction")
plt.title("Predicted vs Actual Fuel Economy")
plt.xlabel("Actual mpg")
plt.ylabel("Predicted mpg")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/model_predicted_vs_actual.png", dpi=120)
plt.close()

print()
print("Saved chart: model_predicted_vs_actual.png")
