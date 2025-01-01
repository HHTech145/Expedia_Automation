import os
import re
import urllib.request
import logging
from Database.connector import Database

class HotelImageDownloader:
    def __init__(self, db_config, base_folder="Database/image_data", log_file="hotel_image_downloader.log"):
        """
        Initialize the downloader with database connection, base folder for images, and logging.
        """
        try:
            # Setup logging
            logging.basicConfig(
                filename=log_file,
                level=logging.INFO,
                format="%(asctime)s [%(levelname)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            logging.info("Initializing HotelImageDownloader.")

            # Initialize database connection
            self.db = Database(**db_config)
            self.db.initialize_database("expedia_db")
            self.cursor = self.db.connection.cursor()

            # Base folder for images
            self.base_folder = base_folder
            if not os.path.exists(self.base_folder):
                os.makedirs(self.base_folder)
        except Exception as e:
            logging.error(f"Error initializing downloader: {e}")

    @staticmethod
    def sanitize_filename(filename):
        """
        Sanitize the filename by removing invalid characters and ensuring compatibility with file systems.
        """
        # Remove newline characters
        sanitized_name = filename.replace("\n", " ")
        # Replace invalid characters with "_"
        sanitized_name = re.sub(r'[\\/:"*?<>|]', '_', sanitized_name)
        # Replace single quotes/apostrophes
        sanitized_name = sanitized_name.replace("'", "")
        # Strip leading/trailing whitespaces and limit length
        sanitized_name = sanitized_name.strip()
        # Replace spaces with underscores
        sanitized_name = sanitized_name.replace(" ", "_")
        # Ensure it does not end with a dot or space (invalid in Windows)
        sanitized_name = sanitized_name.rstrip(". ")
        return sanitized_name
        # Add the .png extension at the end
        # return f"{sanitized_name}.png"


    @staticmethod
    def download_image(url, save_path):
        """
        Download an image using urllib and save it to the specified path.
        """
        try:
            urllib.request.urlretrieve(url, save_path)
            logging.info(f"Image downloaded: {save_path}")
        except Exception as e:
            logging.error(f"Failed to download image from {url}. Error: {e}")

    def create_folder(self, folder_name):
        """
        Create a folder inside the base path with the specified name.
        """
        sanitized_folder_name = self.sanitize_filename(folder_name)
        folder_path = os.path.join(self.base_folder, sanitized_folder_name)
        print("folder_path",folder_path)
        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print("folder created--")
                logging.info(f"Folder created: {folder_path}")
        except Exception as e:
            logging.error(f"Error creating folder {folder_path}: {e}")
        return folder_path

    def fetch_all_hotels(self):
        """
        Fetch all hotel IDs and names from the hotels table.
        """
        try:
            self.cursor.execute("SELECT hotel_id, hotel_name FROM hotels;")
            hotels = self.cursor.fetchall()
            logging.info(f"Fetched {len(hotels)} hotels from the database.")
            return hotels
        except Exception as e:
            logging.error(f"Error fetching hotels: {e}")
            return []

    def fetch_hotel_images(self, hotel_id):
        """
        Fetch image details for the given hotel_id.
        """
        try:
            self.cursor.execute(f"SELECT image_name, image_url FROM hotel_images WHERE hotel_id={hotel_id};")
            images = self.cursor.fetchall()
            logging.info(f"Fetched {len(images)} images for hotel_id {hotel_id}.")
            return images
        except Exception as e:
            logging.error(f"Error fetching images for hotel_id {hotel_id}: {e}")
            return []

    def process_single_hotel(self,hotel_name):
        """
        Process a single hotel by name, downloading its images.
        """
        try:
            # Use parameterized query to avoid SQL syntax errors and injection
            query = "SELECT hotel_id, hotel_name FROM hotels WHERE hotel_name = %s;"
            self.cursor.execute(query, (hotel_name,))
            hotel = self.cursor.fetchone()
            print(hotel,type(hotel))

            ###
            hotel_id, hotel_name = hotel
            print(f"Processing hotel_id: {hotel_id}, hotel_name: {hotel_name}")
            logging.info(f"Processing hotel_id: {hotel_id}, hotel_name: {hotel_name}")
            # folder_name = self.create_folder(f"{hotel_id}___{hotel_name.replace(' ', '_')}")
            
            # # Check if folder already exists
            # # if os.path.exists(folder_name):
            #     logging.info(f"Folder already exists for hotel_id {hotel_id}, skipping.")
            #     print(f"Folder already exists for hotel_id {hotel_id}, skipping.")
                # return
            folder_name = self.create_folder(f"{hotel_id}___{hotel_name.replace(' ', '_')}")
            images = self.fetch_hotel_images(hotel_id)
            print("_--------------------------------------",folder_name)
            if not images:
                logging.warning(f"No images found for hotel_id {hotel_id}")
                return

            for image_name, image_url in images:
                print("333333333333333333333333333333333333333333333333333333")
                sanitized_name = self.sanitize_filename(image_name)
                sanitized_name=f"{sanitized_name}.png"
                save_path = os.path.join(folder_name, sanitized_name)
                print(save_path)
                self.download_image(image_url, save_path)
                print("--------")
            
        except Exception as e:
            print(e)


    def process_hotel_images(self):
        """
        Fetch all hotels and their images, create folders, and download images.
        """
        hotels = self.fetch_all_hotels()
        if not hotels:
            logging.warning("No hotels found in the database.")
            return

        for hotel_id, hotel_name in hotels:
            try:
                if hotel_id>572:
                    print(f"Processing hotel_id: {hotel_id}, hotel_name: {hotel_name}")
                    logging.info(f"Processing hotel_id: {hotel_id}, hotel_name: {hotel_name}")
                    folder_name = self.create_folder(f"{hotel_id}___{hotel_name.replace(' ', '_')}")
                    
                    # Check if folder already exists
                    if os.path.exists(folder_name):
                        logging.info(f"Folder already exists for hotel_id {hotel_id}, skipping.")
                        print(f"Folder already exists for hotel_id {hotel_id}, skipping.")
                        continue
                    folder_name = self.create_folder(f"{hotel_id}___{hotel_name.replace(' ', '_')}")
                    images = self.fetch_hotel_images(hotel_id)

                    if not images:
                        logging.warning(f"No images found for hotel_id {hotel_id}")
                        continue

                    for image_name, image_url in images:
                        sanitized_name = self.sanitize_filename(image_name)
                        sanitized_name=f"{sanitized_name}.png"
                        save_path = os.path.join(folder_name, sanitized_name)
                        self.download_image(image_url, save_path)
            except Exception as e:
                logging.error(f"Error processing hotel_id {hotel_id}: {e}")
            # break

if __name__ == "__main__":
    # Database connection details
    db_config = {
        "host": "localhost",
        "user": "htech_ai",
        "password": "Htech786#"
    }

    # Initialize the HotelImageDownloader and process images
    downloader = HotelImageDownloader(db_config)
    # downloader.process_hotel_images()
    downloader.process_single_hotel(hotel_name="Central Park Hotel")

