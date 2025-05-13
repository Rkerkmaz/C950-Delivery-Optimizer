# main.py
# STUDENT ID: 010683870

from package_loader import load_packages  # C: Support file for loading packages
from hashmap import HashMap               # A: Custom hash table implementation (now includes search)
from load_addresses import load_addresses # C: Address loading
from delivery_simulation import run_delivery_simulation
from delivery_helpers import load_distance_matrix, create_address_map  # C: Distance + address mapping

def main():
    # A: Creating custom hash table instance
    package_hash = HashMap()

    # A: Load package data into the hash table from CSV
    # Each package includes all required fields (address, deadline, city, zip, weight, status)
    load_packages("packages.csv", package_hash, debug=True)

    # B: Use the search function to look up a specific package (e.g., package_id = 1)
    package = package_hash.search(1)  # Example of searching for package with ID 1
    if package:
        print(f"Package {package.package_id} found: {package}")

    # C: Load addresses used in distance calculations
    location_names = load_addresses("addresses.csv")
    print(location_names)  # Optional debug output

    # C: Load distance matrix for routing logic
    distance_matrix = load_distance_matrix("distances.csv")

    # C: Map address names to indices for distance lookup
    location_map = create_address_map(location_names)

    print("\n--- Normalized location keys in address map ---")
    for k in location_map.keys():
        print(f"  {k}")

    # C, D, E:
    # - Runs delivery simulation for all trucks and packages
    # - Tracks and updates time, status, and mileage
    # - Supports time-based delivery reports and total mileage summary
    run_delivery_simulation(location_names, distance_matrix, package_hash, location_map)


# Entry point
if __name__ == "__main__":
    main()
