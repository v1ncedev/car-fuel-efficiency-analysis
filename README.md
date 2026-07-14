# What Makes a Car Fuel Efficient?

A data project that uses real fuel economy figures for 234 cars to answer a
single clear question: what makes a car fuel efficient, and can we predict a
car's economy from a couple of basic facts about it?

It is an end to end project. It takes raw data, cleans it, loads it into a
database, analyses it with both SQL and Python, draws charts, and finishes with
a simple prediction model. The whole thing is written to be read and explained,
because being able to talk through your own work clearly matters more than using
the most advanced tools.

## The question and the answer

The headline findings, all backed by the analysis in this repository:

- **Engine size and cylinder count are the biggest drivers.** Four cylinder
  cars average about 25 mpg; eight cylinder cars average about 15 mpg.
- **Vehicle class follows the same story.** Compact and subcompact cars are the
  most efficient; SUVs and pickups are the least.
- **Manual cars beat automatics on average** in this data, roughly 22 mpg
  against 19 mpg. Note this is partly because manuals are more common in the
  smaller cars, so it is not proof that the gearbox alone causes it.
- **Fuel economy barely changed between 1999 and 2008.** The average was close
  to 20 mpg in both years, which is a genuinely interesting non-result.
- **A simple model predicts a car's economy** from just its engine size and
  cylinder count, explaining about two thirds of the variation, with a typical
  error of around 2 mpg.

## The data

The dataset is real. It contains the fuel economy of 234 popular car models
from the 1999 and 2008 model years, measured by the United States Environmental
Protection Agency (EPA) and published at fueleconomy.gov. It became widely used
through the ggplot2 data visualisation package, and is downloaded here from the
Rdatasets mirror:

    https://vincentarelbundock.github.io/Rdatasets/csv/ggplot2/mpg.csv

A copy (`data/mpg_raw.csv`) is included so the project runs offline. The script
`data/download_data.py` documents where it came from and can refresh it.

The columns, after cleaning:

| Column | Meaning |
| --- | --- |
| manufacturer | The car maker, for example audi |
| model | The model name, for example a4 |
| year | Model year, 1999 or 2008 |
| class | Vehicle class, for example compact or suv |
| displ | Engine size in litres |
| cyl | Number of cylinders |
| transmission_type | Automatic or manual |
| gears | Number of gears (blank for variable gearboxes) |
| drive | Front-wheel, Rear-wheel or Four-wheel |
| fuel | Premium, Regular, Diesel and so on |
| cty | City fuel economy, miles per gallon |
| hwy | Highway fuel economy, miles per gallon |
| avg_mpg | The average of city and highway, our headline figure |

## How the project is organised

```
car-fuel-efficiency-analysis/
  data/
    download_data.py         Documents the source and can refresh the data
    mpg_raw.csv              The raw data as downloaded
    mpg_clean.csv            The cleaned data (created by the cleaning script)
  analysis/
    1_clean_data.py          Checks quality and prepares the data
    2_explore_and_visualise.py   Analyses the data and saves charts
    3_predict_mpg.py         A simple prediction model, built with numpy
  sql/
    1_create_tables.sql      Creates the database table
    2_analysis_queries.sql   Ten analysis queries, simple to advanced
    build_database.py        Builds the database and runs the queries
    car_data.db              The SQLite database (created by build_database.py)
  charts/                    The saved chart images
  requirements.txt           The Python packages needed
  README.md                  This file
  INTERVIEW_NOTES.md         Talking points and practice questions
```

## How to run it

You need Python 3. Install the packages first:

```
pip install -r requirements.txt
```

Then run the steps in order. Each one prints what it is doing.

```
# 1. (Optional) refresh the raw data from its source
cd data
python download_data.py

# 2. Clean and prepare the data
cd ../analysis
python 1_clean_data.py

# 3. Build the database and run the SQL analysis
cd ../sql
python build_database.py

# 4. Explore the data and save the charts
cd ../analysis
python 2_explore_and_visualise.py

# 5. Build and test the prediction model
python 3_predict_mpg.py
```

## Charts

All charts are saved in the `charts` folder:

- `economy_by_class.png` Average economy for each vehicle class
- `economy_by_cylinders.png` Average economy by cylinder count
- `engine_size_vs_economy.png` Engine size against economy, one dot per car
- `economy_by_transmission.png` Automatic against manual
- `economy_by_manufacturer.png` Average economy by manufacturer
- `model_predicted_vs_actual.png` How close the model's predictions are

## What I would do next

Honest limits of this project, and the natural next steps:

- The data covers only 1999 and 2008 models, so it cannot say anything about
  today's cars, including hybrids and electric vehicles.
- The prediction model uses only two inputs. Adding class, drivetrain and
  transmission would likely improve it.
- The model is a straight-line fit, so it is least accurate for the most
  efficient cars, where the real relationship bends. A more flexible model
  would handle that better.
