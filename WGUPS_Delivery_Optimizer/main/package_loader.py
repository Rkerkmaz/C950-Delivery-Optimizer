import csv
from hashmap import Package

def load_packages(filename, package_hash):
    with open(filename, newline='', encoding='utf-8-sig') as file:  # Notice the encoding='utf-8-sig'
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        print(f"Headers: {headers}")  # This will help you verify if the BOM is removed

        for row in reader:
            package = Package(
                int(row['Package ID']),
                row['Address'],
                row['City'],
                row['State'],
                row['Zip'],
                row['Delivery Deadline'],
                float(row['Weight Kilo']),
                row.get('Special Notes', '')
            )
            package_hash.insert(package.package_id, package)
