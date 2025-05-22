import csv
from hashmap import HashMap
from package_loader import load_packages
from delivery_simulation import run_delivery_simulation
from datetime import datetime

# ----------------------------
# Truck Class
# ----------------------------
class Truck:
    """
    Represents a delivery truck that holds and delivers packages.
    Each truck has a limited capacity, mileage tracking, and delivery timing.
    """
    def __init__(self, truck_id, max_capacity=16):
        self.truck_id = truck_id
        self.max_capacity = max_capacity
        self.packages = []
        self.miles = 0.0
        self.start_time = None  # Will be set externally
        self.end_time = None

    def load_packages(self, package_list):
        if len(package_list) > self.max_capacity:
            print(f"Truck {self.truck_id} can't load more than {self.max_capacity} packages!")
        else:
            self.packages = package_list
            print(f"Truck {self.truck_id} loaded with {len(package_list)} packages.")

    def add_miles(self, miles):
        self.miles += miles

    def set_end_time(self, end_time):
        self.end_time = end_time


# ----------------------------
# Load Distance Matrix
# ----------------------------
def load_distance_data(filename):
    distance_data = []
    with open(filename, mode='r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for row in reader:
            row_floats = [float(cell) if cell else 0.0 for cell in row]
            distance_data.append(row_floats)

    num_rows = len(distance_data)
    for i in range(num_rows):
        for j in range(num_rows):
            if j >= len(distance_data[i]):
                if i < len(distance_data[j]):
                    distance_data[i].append(distance_data[j][i])
                else:
                    distance_data[i].append(0.0)
    return distance_data


# ----------------------------
# Load Address Data
# ----------------------------
def load_address_data(filename):
    address_data = []
    with open(filename, mode='r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2:
                address = row[1].strip()
                address_data.append(address)
    return address_data


# ----------------------------
# Main Program Execution
# ----------------------------
if __name__ == "__main__":
    # 1. Load distance matrix from CSV file (Section B.1)
    distance_matrix = load_distance_data("distances_backup.csv")

    # 2. Load address list from CSV file (Section B.2)
    address_list = load_address_data("addresses.csv")

    # 3. Initialize and populate the custom HashMap with packages
    package_hash = HashMap()
    load_packages("packages.csv", package_hash, debug=True)

    # 4. Create truck instances
    truck1 = Truck(truck_id=1)
    truck2 = Truck(truck_id=2)
    truck3 = Truck(truck_id=3)

    # Assign proper datetime start times
    truck1.start_time = datetime.strptime("08:00 AM", "%I:%M %p")
    truck2.start_time = datetime.strptime("09:05 AM", "%I:%M %p")
    truck3.start_time = datetime.strptime("10:20 AM", "%I:%M %p")

    # Optional: print truck start times for verification
    print(f"Truck 1 starts at {truck1.start_time}")
    print(f"Truck 2 starts at {truck2.start_time}")
    print(f"Truck 3 starts at {truck3.start_time}")

    # 5. Load test packages into Truck 2 (example)
    truck2_packages = [
        package_hash.search(1),
        package_hash.search(2),
        package_hash.search(3),
        package_hash.search(4)
    ]
    truck2.load_packages(truck2_packages)

    # 6. Begin delivery simulation
    run_delivery_simulation(address_list, distance_matrix, package_hash, truck1, truck2, truck3)
