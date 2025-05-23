class Truck:
    def __init__(self, name, start_time, max_capacity=16, truck_id=None):
        self.name = name
        self.truck_id = truck_id or name
        self.start_time = start_time
        self.max_capacity = max_capacity
        self.packages = []
        self.miles = 0
        self.end_time = None

    def load_packages(self, pkg_list):
        if len(self.packages) + len(pkg_list) <= self.max_capacity:
            self.packages.extend(pkg_list)
        else:
            raise ValueError(f"{self.name} cannot load that many packages")

    def is_full(self):
        return len(self.packages) >= self.max_capacity

    def add_miles(self, miles):
        self.miles += miles

    def set_end_time(self, end_time):
        self.end_time = end_time
