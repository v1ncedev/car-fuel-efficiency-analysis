"""
download_data.py
----------------

Downloads the raw dataset from its public source and saves it as mpg_raw.csv.

Where the data comes from:
    This is the "mpg" dataset, a well known set of real fuel economy figures for
    234 car models from the 1999 and 2008 model years. The numbers originate
    from the United States Environmental Protection Agency (EPA), published at
    fueleconomy.gov, and the dataset became widely used through the ggplot2
    data visualisation package. We download it from the Rdatasets mirror, which
    hosts many classic datasets as plain CSV files:

        https://vincentarelbundock.github.io/Rdatasets/csv/ggplot2/mpg.csv

A copy of the data (mpg_raw.csv) is already included in this repository, so you
do not have to run this script to use the project. It is here to document
exactly where the data came from and to let anyone refresh it.

Run it with:
    python download_data.py
"""

import urllib.request

URL = "https://vincentarelbundock.github.io/Rdatasets/csv/ggplot2/mpg.csv"
OUTPUT = "mpg_raw.csv"

print(f"Downloading the fuel economy data from:\n  {URL}")
urllib.request.urlretrieve(URL, OUTPUT)
print(f"Saved to {OUTPUT}")
