import random
from pathlib import Path

import pandas as pd

REPLACEMENT_RAW_DIR = "replacement_lists/raw/"


def generate_locations():
    location_list = []
    with open(Path(REPLACEMENT_RAW_DIR / "uk-towns-and-cities-a.txt", "r")) as f:
        for line in f:
            name = line.strip()
            location_list.append(name)

    return location_list


def generate_forenames():
    forenames_df = pd.read_csv(Path(REPLACEMENT_RAW_DIR / "Forename_Autumn2014.csv"))
    return forenames_df["Forename"].to_list()


def generate_surnames():
    surnames_df = pd.read_csv(Path(REPLACEMENT_RAW_DIR / "Forename_Autumn2014.csv"))
    return surnames_df["Surname"].to_list()


def generate_names(num=1000):
    forenames = generate_forenames()
    surnames = generate_surnames()

    names = []
    for i in range(num):
        names.append(f"{random.choice(forenames)} {random.choice(surnames)}")

    return names
