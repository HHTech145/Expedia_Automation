import json

class JsonDataHandler:
    def __init__(self, file_path="hotel_data_new.json"):
        """
        Initializes the JsonDataHandler class with the specified file path.
        :param file_path: Path to the JSON file to store and load data (default: "hotel_data.json")
        """
        self.file_path = file_path
        self.hotel_data=self.load_from_json()

    def save_to_json(self, hotel_name, hotel_details, hotel_amenities, room_details,images_data,neighbourhood):
        """
        Saves the hotel and room details into a JSON file.
        :param hotel_name: The name of the hotel to use as a key
        :param hotel_details: A dictionary containing hotel details (e.g., address, stars)
        :param hotel_amenities: A list of hotel amenities
        :param room_details: A dictionary containing room details (e.g., highlights, amenities)
        """
        data = {
            hotel_name: {
                'hotel_details': hotel_details,
                'hotel_amenities': hotel_amenities,
                'hotel_neighbourhood_data':neighbourhood,
                'room_details': room_details,
                'images_data':images_data
            }
        }

        # Load existing data from the file, if any
        existing_data = self.load_from_json()

        # Update the existing data with the new hotel data
        existing_data.update(data)

        # Save the updated data back to the JSON file
        self._write_json(existing_data)
        print(f"Data for {hotel_name} has been saved successfully.")

    def load_from_json(self):
        """
        Loads the entire JSON data from the file.
        :return: The data stored in the JSON file (returns an empty dictionary if file not found or is empty).
        """
        try:
            with open(self.file_path, 'r') as f:
                # Check if the file is empty
                if f.read(1):
                    f.seek(0)  # Move back to the beginning of the file after reading
                    return json.load(f)
                else:
                    print(f"{self.file_path} is empty. Returning empty data.")
                    return {}
        except FileNotFoundError:
            print(f"{self.file_path} not found. Returning empty data.")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON in {self.file_path}. Returning empty data.")
            return {}

    def get_hotel_data(self, hotel_name):
        """
        Retrieves the details for a specific hotel by its name.
        :param hotel_name: The name of the hotel to fetch data for
        :return: The hotel data if found, or None if the hotel is not found
        """
        # data = self.load_from_json()
        return self.hotel_data.get(hotel_name, None)

    def _write_json(self, data):
        """
        Writes the data to the JSON file.
        :param data: The data to write to the file
        """
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def hotel_exists(self, hotel_name):
        """
        Checks if a hotel exists in the JSON data.
        :param hotel_name: The name of the hotel to check
        :return: True if the hotel exists, False otherwise
        """
        data = self.load_from_json()
        return hotel_name in data
    


if __name__ == "__main__":
    # Example Usage:
    handler = JsonDataHandler()

    # Check if a hotel exists
    print(handler.hotel_exists("White Fort Hotel"))  # Returns True or False

    # # Save new hotel data
    # handler.save_to_json(
    #     hotel_name="Grand Stay",
    #     hotel_details={"address": "123 Main St", "stars": 5},
    #     hotel_amenities=["Pool", "Free Wi-Fi", "Gym"],
    #     room_details={"Room 101": {"highlights": ["Sea View"], "amenities": ["TV", "AC"]}},
    #     images_data=["image1.jpg", "image2.jpg"],
    #     neighbourhood={"nearby": ["Beach", "Mall"]}
    # )

    # Check again if the hotel exists
    print(handler.hotel_exists("Grand Stay"))  # Returns True