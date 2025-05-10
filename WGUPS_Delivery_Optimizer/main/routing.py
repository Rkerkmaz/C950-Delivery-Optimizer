import datetime

TRUCK_SPEED_MPH = 18


def get_location_index(address, location_names):
    for i, location in enumerate(location_names):
        if address in location:
            return i
    return None


def calculate_travel_time(distance):
    hours = distance / TRUCK_SPEED_MPH
    return datetime.timedelta(hours=hours)


def run_delivery_simulation(location_names, distance_matrix, package_hash):
    start_time = datetime.datetime(2023, 1, 1, 8, 0, 0)  # Start at 8:00 AM
    current_time = start_time
    current_location_index = 0  # Assume starting from the hub (index 0)

    undelivered = [package_hash.search(i) for i in range(1, 41)]

    while undelivered:
        nearest_package = None
        nearest_distance = float('inf')
        nearest_index = None

        for package in undelivered:
            destination_index = get_location_index(package.address, location_names)
            if destination_index is not None:
                distance = distance_matrix[current_location_index][destination_index]
                if distance < nearest_distance:
                    nearest_package = package
                    nearest_distance = distance
                    nearest_index = destination_index

        # Deliver the nearest package
        travel_time = calculate_travel_time(nearest_distance)
        current_time += travel_time
        nearest_package.status = "Delivered"
        nearest_package.delivery_time = current_time
        print(f"Delivered Package {nearest_package.package_id} at {current_time.time()}")

        # Remove from undelivered and update location
        undelivered.remove(nearest_package)
        current_location_index = nearest_index
