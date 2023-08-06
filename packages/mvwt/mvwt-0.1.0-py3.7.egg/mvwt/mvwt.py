#!/usr/bin/env python3
"""Main module."""

import csv
from datetime import datetime, timedelta

DATA_TYPES = {
    "weight": {
        "units": "kg",
        "label": "Bodyweight",
    },
    "diet": {
        "units": "none",
        "label": "Diet",
    },
}


def new_entry(key, entry, days_offset=0):
    """Make new timestamped database entry.

    Args:
        key (str): Key for the kind of entry (e.g. weight or diet)
        entry (Any):  Value to be entered in database.
    """

    with open(f"/home/evan/.mvwt/{key}_log.csv", "a+") as file_pointer:
        writer = csv.writer(
            file_pointer, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL
        )
        date = (datetime.today() - timedelta(days=days_offset)).strftime("%Y-%m-%d")
        time = datetime.now().strftime("%H:%M:%S")
        label = DATA_TYPES[key]["label"]
        units = DATA_TYPES[key]["units"]
        writer.writerow([date, time, label, entry, units])
        return True
