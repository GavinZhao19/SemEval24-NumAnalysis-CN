import json
import os

# Define the directory containing the JSON files
directory = 'test/formatted_process'

# Initialize an empty list to store the combined data
combined_data = []

# Iterate over each file in the specified directory
for filename in os.listdir(directory):
    # Check if the file is a JSON file
    if filename.endswith('.json'):
        # Construct the full file path
        file_path = os.path.join(directory, filename)
        # Open and read the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            # Load the JSON data from the file
            data = json.load(file)
            # Append the data to the combined list
            combined_data.extend(data)

file_path = "combined_data.json"

with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(combined_data, file, ensure_ascii=False, indent=4)
