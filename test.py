import json
import datetime
# Load the JSON file
with open('leicester.json', 'r') as file:
    data = json.load(file)

# Count the entries
if isinstance(data, list):  # If the JSON is a list
    count = len(data)
elif isinstance(data, dict):  # If the JSON is a dictionary
    count = len(data.keys())
else:
    count = 0  # Handle other cases if necessary
print(datetime.datetime.now())
print(f"Number of entries in the JSON file: {count}")


# try:
#     with open("hotel_data.json", 'r') as f:
#         json_data = json.load(f)
#         print("JSON loaded successfully.")
# except json.JSONDecodeError as e:
#     print(f"Invalid JSON format: {e}")