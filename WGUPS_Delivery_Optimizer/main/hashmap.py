import csv
from datetime import datetime


# ----------------------------
# Package Class
# ----------------------------

class Package:
    def __init__(self, package_id, address, city='', state='', zip_code='', deadline='', weight=0.0, notes=''):
        self.package_id = int(package_id)
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code

        # Convert deadline string to datetime.time object
        self.deadline = self.parse_deadline(deadline)

        self.weight = float(weight)
        self.notes = notes
        self.status = "Undelivered"
        self.delivery_time = None
        self.address_index = None

        # Constraint-based attributes
        self.truck_restriction = self.extract_truck_restriction(notes)
        self.must_be_delivered_with = self.extract_grouped_ids(notes)
        self.delayed_until = self.extract_delayed_time(notes)

    def parse_deadline(self, deadline_str):
        if deadline_str == "EOD":
            return datetime.strptime("5:00 PM", "%I:%M %p").time()
        elif deadline_str:
            try:
                return datetime.strptime(deadline_str.strip(), "%I:%M %p").time()
            except ValueError:
                print(f"⚠️ Warning: Could not parse deadline '{deadline_str}' for package {self.package_id}")
        return None

    def extract_truck_restriction(self, notes):
        if "Can only be on truck" in notes:
            try:
                return int(notes.split("Can only be on truck")[1].strip()[0])
            except (IndexError, ValueError):
                return None
        return None

    def extract_grouped_ids(self, notes):
        if "Must be delivered with" in notes:
            try:
                ids_part = notes.split("Must be delivered with")[1].strip()
                return [int(pid.strip()) for pid in ids_part.split(",")]
            except Exception as e:
                print(f"⚠️ Failed to extract group info from notes: '{notes}' – {e}")
        return []

    def extract_delayed_time(self, notes):
        if "Delayed on flight" in notes:
            try:
                time_str = notes.split("Delayed on flight---")[1].strip()
                return datetime.strptime(time_str, "%I:%M %p").time()
            except Exception as e:
                print(f"⚠️ Could not parse delay time from notes: '{notes}' – {e}")
        return None

    def __str__(self):
        """
        Returns a nicely formatted string representing the package.
        Useful for debugging and logging.
        """
        return (f"Package {self.package_id}: {self.address}, {self.city}, {self.state}, {self.zip_code}, "
                f"Deadline: {self.deadline}, Weight: {self.weight}kg, Notes: {self.notes}, "
                f"Status: {self.status}, Delivered at: {self.delivery_time}")

# ----------------------------
# HashMap Class
# ----------------------------

class HashMap:
    def __init__(self, initial_size=40):
        self.size = initial_size
        self.map = [[] for _ in range(self.size)]

    def _get_key(self, key):
        return int(key) % self.size

    def insert(self, key, value, debug=False):  # <<-- this must be inside the class
        if debug:
            print(f"Inserting Package {key} into the hash map.")

        key_index = self._get_key(key)
        bucket = self.map[key_index]

        for k, v in bucket:
            if k == key:
                if debug:
                    print(f"Package {key} already exists in HashMap. Skipping insertion.")
                return

        bucket.append((key, value))
        if debug:
            print(f"Inserted Package {key}: {value}")



    # ----------------------------
    # B: Lookup Function (Rubric Section B)
    # ----------------------------
    def search(self, key):
        """
        Retrieves a package from the hash map by its package ID.
        Required by Rubric B: Return all delivery data attributes.

        Returns:
            The Package object (or None if not found)
        """
        key_index = self._get_key(key)
        bucket = self.map[key_index]
        for k, v in bucket:
            if k == key:
                return v
        return None

    # ----------------------------
    # Utility: Display Entire Table
    # ----------------------------
    def display(self):
        """
        Displays all packages stored in the hash map.
        Useful for debugging or visual verification during development.
        """
        for i, bucket in enumerate(self.map):
            if bucket:
                print(f"Bucket {i}:")
                for k, v in bucket:
                    print(f"  {k}: {v}")
