import csv
from hashmap import HashMap
from package_loader import load_packages
from delivery_simulation import run_delivery_simulation
from delivery_helpers import load_distance_data, load_address_data
from datetime import datetime
from truck import Truck  # Import Truck here

# --- Main ---
if __name__ == "__main__":
    distance_matrix = load_distance_data("distances_backup.csv")
    address_list = load_address_data("addresses.csv")

    package_hash = HashMap()
    load_packages("packages.csv", package_hash, debug=True)

    truck1 = Truck(name="Truck 1", start_time=datetime.strptime("08:00 AM", "%I:%M %p"))
    truck2 = Truck(name="Truck 2", start_time=datetime.strptime("09:05 AM", "%I:%M %p"))
    truck3 = Truck(name="Truck 3", start_time=datetime.strptime("10:20 AM", "%I:%M %p"))

    print(f"Truck 1 starts at {truck1.start_time}")
    print(f"Truck 2 starts at {truck2.start_time}")
    print(f"Truck 3 starts at {truck3.start_time}")

    truck2_packages = [package_hash.search(i) for i in [1, 2, 3, 4]]
    truck2.load_packages(truck2_packages)

    run_delivery_simulation(address_list, distance_matrix, package_hash, truck1, truck2, truck3)
