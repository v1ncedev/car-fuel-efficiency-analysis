"""
1_clean_data.py
---------------

Step 1: take the raw data and prepare it for analysis.

This dataset is real, and real data has to be checked before you trust it. Here
we do two things. First we check the data quality (missing values, duplicates).
Second we make some columns easier to work with, for example splitting the
transmission column into "type" and "number of gears", and adding a single
combined fuel economy figure. That second part is called feature preparation:
turning raw columns into fields that are more useful for answering questions.

Input:  ../data/mpg_raw.csv
Output: ../data/mpg_clean.csv

Run it with:
    python 1_clean_data.py
"""

import pandas as pd

# ---------------------------------------------------------------------------
# 1. Load the data.
# ---------------------------------------------------------------------------
cars = pd.read_csv("../data/mpg_raw.csv")
print(f"Loaded {len(cars)} rows and {len(cars.columns)} columns.")

# The first column is just a row number from the original file. We do not need
# it, so we drop it.
if "rownames" in cars.columns:
    cars = cars.drop(columns=["rownames"])

# ---------------------------------------------------------------------------
# 2. Check data quality.
# ---------------------------------------------------------------------------
# Always look before you leap. We report missing values and duplicates rather
# than assuming the data is clean. In this case the data turns out to be
# complete, and being able to say "I checked, and it was clean" is itself worth
# something.
print("\nMissing values per column:")
print(cars.isna().sum())

duplicates = cars.duplicated().sum()
print(f"\nRows that are identical to another row: {duplicates}")
# A note on those identical rows: in this dataset they are not data errors.
# They are genuinely separate car models that happen to share every listed
# specification. Deleting them would throw away real records, so we keep them.
# This is a judgement call, and the point is to make it deliberately rather than
# blindly running "remove duplicates".

# ---------------------------------------------------------------------------
# 3. Make the codes human readable.
# ---------------------------------------------------------------------------
# The raw data stores some fields as short codes. We translate them into words
# so the analysis and charts are easy to read.

# Drivetrain: f = front wheel, r = rear wheel, 4 = four wheel drive.
drive_names = {"f": "Front-wheel", "r": "Rear-wheel", "4": "Four-wheel"}
cars["drive"] = cars["drv"].map(drive_names)

# Fuel type codes.
fuel_names = {
    "p": "Premium", "r": "Regular", "e": "Ethanol", "d": "Diesel", "c": "Natural gas",
}
cars["fuel"] = cars["fl"].map(fuel_names)

# ---------------------------------------------------------------------------
# 4. Split the transmission column into two useful fields.
# ---------------------------------------------------------------------------
# The "trans" column looks like "auto(l5)" or "manual(m6)". It packs two facts
# into one messy string: whether the gearbox is automatic or manual, and how
# many gears it has. We separate them so we can analyse each on its own.

# Everything before the first bracket is the type (auto or manual).
cars["transmission_type"] = cars["trans"].str.split("(").str[0]

# The digits inside the brackets are the number of gears. We pull out the digit
# and turn it into a number. A few automatic gearboxes are listed as "auto(av)",
# which is a variable type with no fixed gear count, so those have no number. We
# record them as missing using pandas' nullable integer type (Int64), which can
# hold whole numbers alongside blanks.
cars["gears"] = cars["trans"].str.extract(r"(\d)").astype("Int64")
print(f"\nTransmissions with no fixed gear count (recorded as missing): "
      f"{cars['gears'].isna().sum()}")

# ---------------------------------------------------------------------------
# 5. Add a single combined fuel economy figure.
# ---------------------------------------------------------------------------
# The data gives city miles per gallon (cty) and highway miles per gallon (hwy)
# separately. A simple, common way to summarise overall economy is the average
# of the two. Higher means more efficient.
cars["avg_mpg"] = ((cars["cty"] + cars["hwy"]) / 2).round(1)

# ---------------------------------------------------------------------------
# 6. Tidy the column order and save.
# ---------------------------------------------------------------------------
cars = cars[[
    "manufacturer", "model", "year", "class",
    "displ", "cyl", "transmission_type", "gears", "drive", "fuel",
    "cty", "hwy", "avg_mpg",
]]

cars.to_csv("../data/mpg_clean.csv", index=False)
print(f"\nDone. Clean data has {len(cars)} rows.")
print("Saved to ../data/mpg_clean.csv")
print("\nFirst few rows:")
print(cars.head().to_string(index=False))
