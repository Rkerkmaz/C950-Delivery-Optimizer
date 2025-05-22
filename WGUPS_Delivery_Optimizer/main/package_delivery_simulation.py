import random
import time

# Initialize the simulation
def simulate_delivery(num_packages=40):
    # Create packages with random attributes
    packages = [{"id": i, "address": f"Address {i}", "priority": random.choice(['High', 'Low']), "status": 'Pending'} for i in range(num_packages)]

    # Simulate delivery vehicle
    vehicle_capacity = 10  # Assume vehicle can carry 10 packages at once
    total_delivered = 0
    failed_deliveries = []

    print("Starting delivery simulation...\n")

    # Simulate package delivery in batches
    for batch_start in range(0, num_packages, vehicle_capacity):
        batch = packages[batch_start: batch_start + vehicle_capacity]

        # Simulate each package in the batch being delivered
        for package in batch:
            print(f"Delivering package {package['id']} to {package['address']}...")
            time.sleep(0.5)  # Simulate time taken to deliver
            package['status'] = 'Delivered'
            total_delivered += 1

            # Simulate possible failure scenario (e.g., delivery exception)
            if random.random() < 0.1:  # 10% chance of failure
                package['status'] = 'Failed'
                failed_deliveries.append(package['id'])
                total_delivered -= 1
                print(f"Package {package['id']} failed delivery.")

        print(f"Batch {batch_start // vehicle_capacity + 1} delivered.\n")

    # Check if all packages were delivered
    undelivered_packages = [pkg['id'] for pkg in packages if pkg['status'] != 'Delivered']

    print(f"Total packages delivered: {total_delivered}/{num_packages}")
    print(f"Failed deliveries: {failed_deliveries}")
    print(f"Undelivered packages: {undelivered_packages}")

# Run the simulation
simulate_delivery()
