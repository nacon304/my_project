import json
import csv

def convert_json_to_csv(input_file, output_file):
    # Open JSON file for reading in binary mode
    with open(input_file, 'rb') as f:
        # Decode file contents as UTF-8
        content = f.read().decode('utf-8')
        # Parse JSON data
        data = json.loads(content)

    # Open CSV file for writing
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Write header row
        writer.writerow(data[0].keys())

        # Write data rows
        for row in data:
            writer.writerow(row.values())

# Example usage
convert_json_to_csv("outputFull.json", "outputFull.csv")