from hashmap import HashMap, Package  # Import HashMap and Package from hashmap.py
from package_loader import load_packages  # Import the load_packages function

def main():
    # Initialize the hash map for packages
    package_hash = HashMap()

    # Load packages into the hash map
    load_packages("packages.csv", package_hash)

    # Optional: Print loaded packages to verify
    for package_id in range(1, 41):  # Assuming 40 packages
        package = package_hash.search(package_id)
        if package:
            print(package)

    # Demonstrate searching for a specific package
    package_id_to_search = 1
    found_package = package_hash.search(package_id_to_search)
    if found_package:
        print(f"Found: {found_package}")
    else:
        print(f"Package with ID {package_id_to_search} not found.")

    # Demonstrate removing a package
    package_id_to_remove = 1
    if package_hash.remove(package_id_to_remove):
        print(f"Package with ID {package_id_to_remove} removed.")
    else:
        print(f"Package with ID {package_id_to_remove} not found for removal.")

    # Try searching for the package again after removal
    found_package = package_hash.search(package_id_to_remove)
    if found_package:
        print(f"Found: {found_package}")
    else:
        print(f"Package with ID {package_id_to_remove} not found.")

if __name__ == "__main__":
    main()
