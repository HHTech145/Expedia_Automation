from database.connector import Database
import json
import traceback

class PostcodeDataHandler:
    def __init__(self, db_config, json_file_path):
        self.db = Database(**db_config)
        self.json_file_path = json_file_path
        self.postcode_data = self.read_json()

    def read_json(self):
        """Read the JSON file and return the data."""
        with open(self.json_file_path, 'r') as json_file:
            return json.load(json_file)
        


    def store_data_as_json(self, postcode, restaurant_data, pub_data,demo_df):
        """Stores restaurant and pub data in JSON format against the given postcode."""
        # Create a dictionary structure
        data = {
            postcode: {
                'demographics': demo_df.to_dict(orient='records'),
                'restaurants': restaurant_data.to_dict(orient='records'),
                'pubs': pub_data.to_dict(orient='records')

            }
        }
        
        # Save to a JSON file
        filename = f"{postcode}_data.json"
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
        print(f"Data saved to {filename}")