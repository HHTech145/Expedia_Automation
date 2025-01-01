import mysql.connector
import json
from mysql.connector import Error
from time import sleep

class Database:
    def __init__(self, host="localhost", user="root", password="", database=None):
        """
        Initialize the connection to the MySQL database.
        If a database is provided, it will connect to that database.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.connect()

    def connect(self):
        """Establish a connection to the MySQL server"""
        try:
            if self.database:
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
            else:
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password
                )
            if self.connection.is_connected():
                print("Connection successful!")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")

    def create_database(self, db_name):
        """Create a new database"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print(f"Database '{db_name}' created successfully!")
        except Error as e:
            print(f"Error creating database: {e}")
        finally:
            cursor.close()

    def initialize_database(self, db_name):
        """Select and initialize the database"""
        try:
            self.connection.database = db_name
            print(f"Database '{db_name}' selected.")
        except Error as e:
            print(f"Error selecting database: {e}")
                        
    def create_tables(self):
        try:
            cursor = self.connection.cursor()
            # SQL statements to create tables
            sql_statements = [
                """
                CREATE TABLE IF NOT EXISTS hotels (
                    hotel_id INT AUTO_INCREMENT PRIMARY KEY,
                    hotel_name VARCHAR(255) NOT NULL, -- Hotel name must be provided
                    hotel_address TEXT NOT NULL,      -- Hotel address must be provided
                    hotel_rating DECIMAL(5, 2) DEFAULT NULL, -- Allow NULL for unspecified ratings
                    additional_rating DECIMAL(5, 2) DEFAULT NULL, -- Allow NULL for additional ratings
                    hotel_description TEXT DEFAULT NULL, -- Optional description
                    url VARCHAR(2083) DEFAULT NULL,      -- Increased length for URLs, optional
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Automatically set to current time
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP -- Auto-update on change
                );
                """,
                """
                CREATE TABLE hotel_neighborhoods (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    hotel_id INT NOT NULL,  -- Foreign key to link with the hotel information
                    neighborhood_data JSON,  -- JSON column to store all the neighborhood details
                    FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id) ON DELETE CASCADE
                );
                """,                
                """
                CREATE TABLE IF NOT EXISTS rooms (
                    room_id INT AUTO_INCREMENT PRIMARY KEY,
                    hotel_id INT,
                    room_name VARCHAR(255),
                    highlights JSON,
                    room_details JSON,
                    amenities_list JSON,
                    price_details JSON,
                    FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id)
                );

                """,
                """
                CREATE TABLE IF NOT EXISTS hotel_amenities (
                    amenity_id INT AUTO_INCREMENT PRIMARY KEY,
                    hotel_id INT,
                    amenity_name VARCHAR(255) NOT NULL,  -- Ensure amenity name is provided
                    amenity_details JSON DEFAULT NULL,   -- Allow NULL for amenity details
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Automatically set the timestamp when a record is created
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- Auto-update timestamp when a record is modified
                    FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id) ON DELETE CASCADE  -- Cascade delete if hotel is deleted
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS room_prices (
                    price_id INT AUTO_INCREMENT PRIMARY KEY,
                    room_id INT,
                    price_details JSON DEFAULT NULL,   -- Allow NULL for price details
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Automatically set the timestamp when a record is created
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- Auto-update timestamp when a record is modified
                    FOREIGN KEY (room_id) REFERENCES rooms(room_id) ON DELETE CASCADE  -- Cascade delete if room is deleted
                );
                """,
                """
            CREATE TABLE IF NOT EXISTS hotel_images (
                image_id INT AUTO_INCREMENT PRIMARY KEY,
                hotel_id INT,
                image_name VARCHAR(255) NOT NULL,  -- Ensure image name is provided
                image_url TEXT NOT NULL,           -- Ensure image URL is provided
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Automatically set the timestamp when a record is created
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- Auto-update timestamp when a record is modified
                FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id) ON DELETE CASCADE  -- Cascade delete if hotel is deleted
            );
                """
            ]


            # Execute each statement
            for sql in sql_statements:
                cursor.execute(sql)
            self.connection.commit()
            print("Tables created successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
   
    def insert_hotel_data(self, hotel_data):
        try:
            cursor = self.connection.cursor()
            hotel_details = hotel_data['hotel_details']
            # hotel_details = hotel_data['hotel_details']
            hotel_name = hotel_details['hotel_name']

            # Check if hotel already exists by name
            cursor.execute("""
                SELECT hotel_id FROM hotels WHERE hotel_name = %s
            """, (hotel_name,))
            
            # Fetch the result and ensure no unread results
            existing_hotel = cursor.fetchone()

            if existing_hotel:
                print(f"Hotel '{hotel_name}' already exists in the database. Skipping insertion.")
                # cursor.close()
                cursor.fetchall()
                return  # Skip the insertion if hotel exists


            hotel_rating = hotel_details.get('hotel_rating', None)
            # If hotel_rating is the string 'null', set it to None (SQL NULL)
            if hotel_rating == 'null':
                hotel_rating = None
            # Insert hotel data
            cursor.execute("""
                INSERT INTO hotels (hotel_name, hotel_address, hotel_rating, additional_rating, hotel_description, url)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                hotel_details['hotel_name'],
                hotel_details['hotel_address'],
                hotel_rating,
                hotel_details['additional_rating'],
                hotel_details['hotel_description'],
                hotel_details['url']
            ))
            hotel_id = cursor.lastrowid  # Get the inserted hotel's id

            # Insert neighborhood data
            neighborhood_data = hotel_data.get('hotel_neighbourhood_data', {})
            if neighborhood_data:
                cursor.execute("""
                    INSERT INTO hotel_neighborhoods (hotel_id, neighborhood_data)
                    VALUES (%s, %s)
                """, (
                    hotel_id,
                    json.dumps(neighborhood_data)  # Store neighborhood data as JSON
                ))

                        # Check if room_details is not None
            room_details = hotel_data.get('room_details', None)
            if room_details is not None:

                # Insert room data
                for room_name, room in hotel_data['room_details'].items():
                    cursor.execute("""
                        INSERT INTO rooms (hotel_id, room_name, highlights, room_details, amenities_list, price_details)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        hotel_id,
                        room_name,
                        json.dumps(room['highlights']),  # Store highlights as JSON
                        json.dumps(room['room_details']),  # Store room details as JSON
                        json.dumps(room['amenities_list']),  # Store amenities list as JSON
                        json.dumps(room['price_detail'])  # Store price details as JSON
                    ))
                    room_id = cursor.lastrowid  # Get the inserted room's id

                    # Insert room prices
                    price_detail=room['price_detail']

                    for price_detail in room['price_detail']:
                        cursor.execute("""
                            INSERT INTO room_prices (room_id, price_details)
                            VALUES (%s, %s)
                        """, (room_id, json.dumps(price_detail)))

            # Insert hotel images (store image name and URL)
            for image_name, image_data in hotel_data['images_data'].items():
                # Extract image URL
                image_url = image_data['src_url']
                # Insert into hotel_images table
                cursor.execute("""
                    INSERT INTO hotel_images (hotel_id, image_name, image_url)
                    VALUES (%s, %s, %s)
                """, (hotel_id, image_name, image_url))

            # Insert amenities if they exist (check if 'hotel_amenities' is not None)
            hotel_amenities = hotel_data.get('hotel_amenities', None)
            if hotel_amenities:
                for amenity_name, amenity_details in hotel_amenities.items():
                    cursor.execute("""
                        INSERT INTO hotel_amenities (hotel_id, amenity_name, amenity_details)
                        VALUES (%s, %s, %s)
                    """, (hotel_id, amenity_name, json.dumps(amenity_details)))

            # Commit the transaction
            self.connection.commit()
            print("Hotel data inserted successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()

    # def insert_hotel_data(self, hotel_data):
    #     try:
    #         cursor = self.connection.cursor()
    #         hotel_details = hotel_data['hotel_details']
    #         # Insert hotel data
            
    #         cursor.execute("""
    #             INSERT INTO hotels (hotel_name, hotel_address, hotel_rating, additional_rating, hotel_description, url)
    #             VALUES (%s, %s, %s, %s, %s, %s)
    #         """, (
    #             hotel_details['hotel_name'],
    #             hotel_details['hotel_address'],
    #             hotel_details['hotel_rating'],
    #             hotel_details['additional_rating'],
    #             hotel_details['hotel_description'],
    #             hotel_details['url']
    #         ))
    #         hotel_id = cursor.lastrowid  # Get the inserted hotel's id

    #         # Insert room data
    #         for room_name, room in hotel_data['room_details'].items():
    #             cursor.execute("""
    #                 INSERT INTO rooms (hotel_id, room_name, highlights, room_details, amenities_list, price_details)
    #                 VALUES (%s, %s, %s, %s, %s, %s)
    #             """, (
    #                 hotel_id,
    #                 room_name,
    #                 json.dumps(room['highlights']),  # Store highlights as JSON
    #                 json.dumps(room['room_details']),  # Store room details as JSON
    #                 json.dumps(room['amenities_list']),  # Store amenities list as JSON
    #                 json.dumps(room['price_detail'])  # Store price details as JSON
    #             ))
    #             room_id = cursor.lastrowid  # Get the inserted room's id

    #         # Insert hotel images (store image name and URL)
    #         for image_name, image_data in hotel_data['images_data'].items():
    #             # Extract image URL
    #             image_url = image_data['src_url']
    #             # Insert into hotel_images table
    #             cursor.execute("""
    #                 INSERT INTO hotel_images (hotel_id, image_name, image_url)
    #                 VALUES (%s, %s, %s)
    #             """, (hotel_id, image_name, image_url))

    #         # Insert amenities
    #         for amenity_name, amenity_details in hotel_data['hotel_amenities'].items():
    #             cursor.execute("""
    #                 INSERT INTO hotel_amenities (hotel_id, amenity_name, amenity_details)
    #                 VALUES (%s, %s, %s)
    #             """, (hotel_id, amenity_name, json.dumps(amenity_details)))

    #         # Commit the transaction
    #         self.connection.commit()
    #         print("Hotel data inserted successfully.")
    #     except mysql.connector.Error as err:
    #         print(f"Error: {err}")
    #     finally:
    #         cursor.close()

    def load_json(self, file_path):
        try:
            with open(file_path, "r") as file:
                hotel_data = json.load(file)
                hotels_list = [value for key, value in hotel_data.items()]
                # hotels_list = [{"name": key, "details": value} for key, value in hotel_data.items()]

            return hotels_list
        except FileNotFoundError as err:
            print(f"File not found: {err}")
            return []
        except json.JSONDecodeError as err:
            print(f"Error decoding JSON: {err}")
            return []

    def process_and_insert_single_hotel(self,hotel_data):
        try:
            print("in process_and_insert")
            # print(f"Inserting hotel: {hotel_data.get('hotel_details', {}).get('hotel_name', 'Unknown')}")
            print("hotel_data__________________________________________________",hotel_data)
            self.insert_hotel_data(hotel_data)
            # break
        except Exception as err:
            print(f"Error inserting hotel data: {err}")        

    def process_and_insert(self, data):
        for hotel_data in data:
            try:
                print(f"Inserting hotel: {hotel_data.get('hotel_details', {}).get('hotel_name', 'Unknown')}")
                self.insert_hotel_data(hotel_data)
                # break
            except Exception as err:
                print(f"Error inserting hotel data: {err}")

    def close_connection(self):
        if self.connection.is_connected():
            # self.cursor.close()
            self.connection.close()
            print("Connection closed.")

# Usage Example

if __name__ == "__main__":
    # db = Database(host='localhost', user='your_username', password='your_password', database='hotel_db')

    db = Database(host="localhost", user="htech_ai", password="Htech786#")
    # db.create_database("expedia_db")
    # Initialize the database (connect to it)
    db.initialize_database("expedia_db")

    file_path=r"D:\work\automation\air world tour\Expedia\hotel_data.json"
    data=db.load_json(file_path=file_path)

    # for i in data:
        # print("data: --------------------",i)
        # db.insert_hotel_data(hotel_data=i)
    db.process_and_insert(data)
    #     # print(data)
        # sleep(20000)

    # db.process_and_insert(data=data)
    # Create tables in the database
    # db.create_tables()
    # Close the connection
    # Close the database connection
    db.close_connection()