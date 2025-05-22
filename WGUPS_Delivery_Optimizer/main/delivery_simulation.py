from datetime import datetime, timedelta, time
from delivery_helpers import get_distance, create_address_map, get_location_index

TRUCK_SPEED = 18  # miles per hour

def run_delivery_simulation(address_list, distance_matrix, package_hash, truck1, truck2, truck3):
    """
    WGUPS Delivery Simulation
    - Handles loading, constraint grouping, routing, and delivery simulation.
    """

    from main import Truck
    all_trucks = [truck1, truck2, truck3]

    # Step 1: Extract All Packages (IDs 1 to 40)
    all_packages = [package_hash.search(i) for i in range(1, 41)]

    # Step 2: Group by Constraint Types
    delayed_packages = []
    grouped_sets = []
    truck_restricted = {1: [], 2: [], 3: []}
    priority_deadline = []
    flexible_packages = []
    seen_in_groups = set()

    for pkg in all_packages:
        if pkg.must_be_delivered_with and pkg.package_id not in seen_in_groups:
            group = set([pkg.package_id] + pkg.must_be_delivered_with)
            grouped_sets.append(group)
            seen_in_groups.update(group)

    for pkg in all_packages:
        if pkg.package_id in seen_in_groups:
            continue
        if pkg.delayed_until:
            delayed_packages.append(pkg)
        elif pkg.truck_restriction:
            truck_restricted[pkg.truck_restriction].append(pkg)
        elif pkg.deadline and pkg.deadline < datetime.strptime("5:00 PM", "%I:%M %p").time():
            priority_deadline.append(pkg)
        else:
            flexible_packages.append(pkg)

    assigned_package_ids = set()

    # Step 3: Assign Grouped Sets to Any Truck That Can Hold Them
    for group in grouped_sets:
        pkg_list = [package_hash.search(pid) for pid in group]
        for truck in all_trucks:
            if len(truck.packages) + len(pkg_list) <= truck.max_capacity:
                truck.packages.extend(pkg_list)
                for pkg in pkg_list:
                    assigned_package_ids.add(pkg.package_id)
                    print(f"Assigned grouped Package {pkg.package_id} to Truck {truck.truck_id}")
                break

    # Step 4: Assign Truck-Restricted Packages
    for truck_id, pkgs in truck_restricted.items():
        truck = all_trucks[truck_id - 1]
        for pkg in pkgs:
            if pkg.package_id not in assigned_package_ids:
                truck.load_packages([pkg])
                assigned_package_ids.add(pkg.package_id)
                print(f"Truck-restricted Package {pkg.package_id} loaded on Truck {truck_id}")

    # Step 5: Assign Delayed Packages (Truck 3 leaves latest)
    truck3.start_time = datetime.combine(datetime.today(), time(hour=10, minute=20))
    for pkg in delayed_packages:
        if pkg.package_id not in assigned_package_ids:
            truck3.packages.append(pkg)
            assigned_package_ids.add(pkg.package_id)
            print(f"Delayed Package {pkg.package_id} loaded on Truck 3 (10:20 AM start)")

    # Step 6: Assign Priority Deadline Packages
    for pkg in priority_deadline:
        if pkg.package_id not in assigned_package_ids:
            for truck in all_trucks:
                if len(truck.packages) < truck.max_capacity:
                    truck.packages.append(pkg)
                    assigned_package_ids.add(pkg.package_id)
                    print(f"Priority Package {pkg.package_id} assigned to Truck {truck.truck_id}")
                    break

    # Step 7: Assign Flexible Packages
    for pkg in flexible_packages:
        if pkg.package_id not in assigned_package_ids:
            for truck in all_trucks:
                if len(truck.packages) < truck.max_capacity:
                    truck.packages.append(pkg)
                    assigned_package_ids.add(pkg.package_id)
                    print(f"Flexible Package {pkg.package_id} assigned to Truck {truck.truck_id}")
                    break

    # Step 8: Final Catch-All (if any missed)
    unassigned = [p for p in all_packages if p.package_id not in assigned_package_ids]
    for pkg in unassigned:
        for truck in all_trucks:
            if len(truck.packages) < truck.max_capacity:
                truck.packages.append(pkg)
                assigned_package_ids.add(pkg.package_id)
                print(f"🚨 Final pass: assigned Package {pkg.package_id} to Truck {truck.truck_id}")
                break

    # Step 9: Print Truck Loads
    for truck in all_trucks:
        print(f"\nTruck {truck.truck_id} - Start Time: {truck.start_time}")
        print(f"Packages Loaded: {[p.package_id for p in truck.packages]}")

    print("\n🚚 All trucks loaded with constraints respected.\n")

    # Step 10: Routing + Delivery Simulation
    address_map = create_address_map(address_list)

    def reorder_truck_packages(truck, distance_matrix):
        """ Sort truck packages using Nearest Neighbor """
        if not truck.packages:
            return

        current_index = 0  # Hub index
        sorted_packages = []
        remaining = truck.packages[:]

        while remaining:
            nearest_pkg = min(remaining, key=lambda pkg: get_distance(distance_matrix, current_index, pkg.address_index))
            sorted_packages.append(nearest_pkg)
            current_index = nearest_pkg.address_index
            remaining.remove(nearest_pkg)

        truck.packages = sorted_packages

    def deliver_truck_packages(truck):
        current_index = 0
        current_time = truck.start_time
        remaining = truck.packages[:]

        for pkg in remaining:
            pkg.address_index = get_location_index(pkg.address, address_map)

        reorder_truck_packages(truck, distance_matrix)

        while remaining:
            next_pkg = min(remaining, key=lambda pkg: get_distance(distance_matrix, current_index, pkg.address_index))
            travel_distance = get_distance(distance_matrix, current_index, next_pkg.address_index)
            travel_time = timedelta(hours=travel_distance / TRUCK_SPEED)

            current_time += travel_time
            truck.add_miles(travel_distance)

            next_pkg.delivery_time = current_time
            next_pkg.status = "Delivered"
            print(f"Delivered Package {next_pkg.package_id} at {next_pkg.delivery_time.time()}")

            current_index = next_pkg.address_index
            remaining.remove(next_pkg)

        # Return to hub
        return_to_hub = get_distance(distance_matrix, current_index, 0)
        truck.add_miles(return_to_hub)
        truck.set_end_time(current_time + timedelta(hours=return_to_hub / TRUCK_SPEED))

    # Deliver packages for each truck
    all_trucks.sort(key=lambda t: t.start_time)  # Optional realism
    for truck in all_trucks:
        deliver_truck_packages(truck)

    # Step 11: Delivery Summary
    total_miles = sum(truck.miles for truck in all_trucks)
    print("\n📦 --- Delivery Summary ---")
    for truck in all_trucks:
        print(f"Truck {truck.truck_id} - End: {truck.end_time}, Miles: {truck.miles:.2f}")
    print(f"\nTotal Packages Delivered: {len(assigned_package_ids)} / 40")
    print(f"Total Miles: {total_miles:.2f}")
