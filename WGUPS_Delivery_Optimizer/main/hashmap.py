# hashmap.py

# Class to represent a package with all required delivery details
class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, notes=''):
        # Unique ID for each package
        self.package_id = package_id
        # Destination address information
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        # Deadline by which the package must be delivered
        self.deadline = deadline
        # Weight of the package
        self.weight = weight
        # Optional special notes (e.g., delivery instructions or exceptions)
        self.notes = notes
        # Current status of the package (At Hub, En Route, Delivered)
        self.status = "At Hub"
        # Timestamp when the package was delivered
        self.delivery_time = None

    def __str__(self):
        # Returns a human-readable string representation of the package
        return (f"Package {self.package_id}: {self.address}, {self.deadline}, "
                f"Status: {self.status}, Delivered at: {self.delivery_time}, Notes: {self.notes}")


# Custom HashMap implementation without using built-in Python dictionaries
# This stores packages using a hash table with chaining to handle collisions
class HashMap:
    def __init__(self):
        # Hash table with fixed number of buckets (sufficient for 40 packages)
        self.size = 40
        # Each bucket is a list to handle collisions via chaining
        self.map = [[] for _ in range(self.size)]

    # Internal method to generate a hash key using modulo arithmetic
    def _get_key(self, key):
        return int(key) % self.size

    # Inserts a new package into the hash table or updates it if it already exists
    def insert(self, key, item):
        key_index = self._get_key(key)
        bucket = self.map[key_index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                # Update existing package
                bucket[i] = (key, item)
                print(f"Updated Package {key}")
                return
        # Add new package
        bucket.append((key, item))
        print(f"Inserted Package {key}: {item}")

    # Looks up a package by ID and returns the package object
    def search(self, key):
        key_index = self._get_key(key)
        bucket = self.map[key_index]
        for k, v in bucket:
            if k == key:
                print(f"Found Package {key}: {v}")
                return v
        print(f"Package {key} not found during search.")
        return None

    # Removes a package from the hash table by ID
    def remove(self, key):
        key_index = self._get_key(key)
        bucket = self.map[key_index]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                print(f"Removed Package {key}")
                return True
        print(f"Package {key} not found during remove.")
        return False

    # Utility function to print the entire hash table for debugging
    def print_map(self):
        for i, bucket in enumerate(self.map):
            if bucket:
                print(f"Bucket {i}: {bucket}")
