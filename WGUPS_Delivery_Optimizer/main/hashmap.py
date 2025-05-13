# hashmap.py
# RUBRIC A: Custom Hash Table Implementation
# STUDENT ID: 010683870

# ----------------------------
# Package Class
# ----------------------------
class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, notes=''):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = "At Hub"
        self.delivery_time = None
        self.address_index = None

    def __str__(self):
        return (f"Package {self.package_id}: {self.address}, {self.deadline}, "
                f"Status: {self.status}, Delivered at: {self.delivery_time}, Notes: {self.notes}")


# ----------------------------
# HashMap Class
# ----------------------------
class HashMap:
    def __init__(self):
        self.size = 40
        self.map = [[] for _ in range(self.size)]

    def _get_key(self, key):
        return int(key) % self.size

    # A: Insert function
    def insert(self, key, item, debug=False):
        key_index = self._get_key(key)
        bucket = self.map[key_index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                if debug:
                    print(f"Package {key} already exists in HashMap. Skipping insertion.")
                return
        bucket.append((key, item))
        if debug:
            print(f"Inserted Package {key}: {item}")

    # B: Search function
    def search(self, key):
        key_index = self._get_key(key)
        bucket = self.map[key_index]
        for k, v in bucket:
            if k == key:
                return v  # Found package, return package object
        return None  # Package not found
