import csv
import json

def read_csv_and_split(filename):
    contacts = ""

    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            contacts += ','.join(row[1:]) + ','  # Concatenate values in each row (excluding the first element)
    
    contacts_list = contacts.split(',')  # Split the concatenated string by ','
    contacts_list = [contact.strip() for contact in contacts_list if contact.strip()]  # Remove empty strings and strip whitespace

    return contacts_list

# Example usage:
csv_filename = 'schedule.csv'
contacts_list = read_csv_and_split(csv_filename)
class_numbers = sorted(list(set(contacts_list)))  # Get unique class numbers sorted in ascending order

# Save class_numbers as a JSON file
json_filename = 'class_numbers.json'
with open(json_filename, 'w') as jsonfile:
    json.dump(class_numbers, jsonfile)

print(f"Class numbers saved as '{json_filename}'.")