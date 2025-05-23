# package_loader.py

import csv
import re
from datetime import datetime
from hashmap import Package  # Package class is defined in hashmap.py


# ----------------------------
# Parse Notes for Constraints
# ----------------------------

def parse_notes(notes):
    """
    Extracts delivery constraints from the 'Special Notes' column in the CSV.
    Returns:
        truck_restriction (int or None)
        must_be_delivered_with (list of int)
        delayed_until (datetime.time or None)
    """
    truck_restriction = None
    must_be_delivered_with = []
    delayed_until = None

    # Match specific truck requirement
    truck_match = re.search(r'truck (\d+)', notes, re.IGNORECASE)
    if truck_match:
        truck_restriction = int(truck_match.group(1))

    # Match grouped delivery requirement
    delivered_with_match = re.search(r'must be delivered with ([\d, ]+)', notes, re.IGNORECASE)
    if delivered_with_match:
        must_be_delivered_with = [int(x.strip()) for x in delivered_with_match.group(1).split(',')]

    # Match delivery delay time (more robust)
    if 'until' in notes.lower():
        print(f"[Debug] Trying to parse delay time from: '{notes}'")
        delayed_match = re.search(r'until (\d{1,2}:\d{2} ?[ap]m)', notes, re.IGNORECASE)
        if delayed_match:
            try:
                time_str = delayed_match.group(1).lower().replace(' ', '')
                delayed_until = datetime.strptime(time_str, '%I:%M%p').time()
            except ValueError:
                print(f"[Warning] Failed to parse delay time from note: '{notes}'")

    return truck_restriction, must_be_delivered_with, delayed_until

# ----------------------------
# C.1 – Load Package Data into HashMap
# ----------------------------
def load_packages(filename, package_hash, debug=False):
    """
    Loads package data from a CSV file into a custom HashMap data structure.
    This function fulfills Rubric Requirement C.1 and supports A and B.

    For each package:
    - Extracts ID, address, deadline, city, zip code, weight, and status
    - Parses any delivery constraints from the "Special Notes" field
    - Instantiates a Package object
    - Inserts it into the provided custom HashMap (no built-in dict used)

    Args:
        filename (str): Path to the 'WGUPS Package File' CSV
        package_hash (HashMap): Custom hash table to populate
        debug (bool): Optional flag to print debug information during load
    """
    with open(filename, newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        print(f"Headers: {headers}")  # Optional debugging of field names

        for row in reader:
            # Extract base package data
            package_id = int(row['Package ID'])
            package_address = row['Address']
            package_city = row['City']
            package_state = row['State']
            package_zip = row['Zip']
            package_deadline = row['Delivery Deadline']
            package_weight = float(row['Weight Kilo'])
            package_notes = row.get('Special Notes', '')

            # Parse delivery constraints (supports rubric constraints on delays/grouped deliveries)
            truck_restriction, must_be_delivered_with, delayed_until = parse_notes(package_notes)

            if debug:
                print(f"Loading Package ID: {package_id}, Deadline: {package_deadline}, "
                      f"Truck Restriction: {truck_restriction}, Grouped: {must_be_delivered_with}, "
                      f"Delayed Until: {delayed_until}")

            # Create Package object
            package = Package(
                package_id, package_address, package_city, package_state,
                package_zip, package_deadline, package_weight, package_notes
            )

            # Attach delivery constraints
            package.truck_restriction = truck_restriction
            package.must_be_delivered_with = must_be_delivered_with
            package.delayed_until = delayed_until

            # Debug: Print when inserting into the hash map
            if debug:
                print(f"Inserting Package ID: {package.package_id} into the hash map.")

            # Insert into custom hash map (Rubric A: Insert Function)
            package_hash.insert(package.package_id, package, debug)
