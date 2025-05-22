import csv

# ----------------------------
# B.1 – Load Distance Matrix (2D)
# ----------------------------

def get_distance(matrix, i, j):
    """
    Returns the distance between two addresses using the symmetric distance matrix.
    Parameters:
        matrix (List[List[float]]): 2D distance table
        i (int): index of first address
        j (int): index of second address

    Returns:
        float: distance in miles
    """
    if i > j:
        return matrix[i][j]
    return matrix[j][i]


def load_distance_data(file_path):
    """
    Loads the upper-triangle distance matrix from a CSV file.

    Returns:
        distance_matrix (List[List[float]]): Symmetric matrix of delivery distances.

    Rubric C – Supports the delivery program by allowing distance lookups between addresses.
    """
    distance_matrix = []

    with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for row in reader:
            distance_matrix.append([float(cell) if cell else 0.0 for cell in row])

    return distance_matrix


# ----------------------------
# B.2 – Load Address Data
# ----------------------------

def load_address_data(file_path):
    """
    Loads delivery addresses from CSV and returns them in a list.

    Returns:
        address_list (List[str]): Ordered address entries aligned with distance matrix.

    Rubric C – Used to convert delivery addresses to matrix indices for routing.
    """
    address_list = []

    with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2:
                combined_address = row[1].strip()
                address_list.append(combined_address)

    return address_list


# ----------------------------
# Address Lookup Utilities
# ----------------------------

def create_address_map(addresses):
    """
    Maps each address to its index in the distance matrix.

    Returns:
        dict[str, int]: Dictionary for quick address-to-index lookup.

    Rubric H – Supports optimized address indexing using native dicts.
    """
    return {address.strip(): idx for idx, address in enumerate(addresses)}


def get_location_index(address, address_map):
    """
    Attempts to get the index of a given address from the address map.
    Falls back to a partial match if exact match is not found.

    Rubric H – Provides robustness in handling address typos or formatting variations.

    Parameters:
        address (str): Delivery address from package
        address_map (dict): Precomputed {address -> index} map

    Returns:
        int: Index in distance matrix, or None if not found.
    """
    if address.strip() in address_map:
        return address_map[address.strip()]
    for key in address_map:
        if address.strip() in key:
            return address_map[key]
    return None
