# import pymysql
from connector import Database
import spacy
from collections import defaultdict
import pprint
import openai





# Load spaCy model for NLP
nlp = spacy.load("en_core_web_sm")







def fetch_room_names(hotel_id,cursor):

    # Execute query to fetch image names
    query = f"SELECT room_name FROM expedia_db.rooms where hotel_id={hotel_id};"
    cursor.execute(query)
    result = cursor.fetchall()

    # Extract image names into a list
    room_names = [row[0] for row in result]

    return room_names


def fetch_image_names(hotel_id,cursor):
    # Database connection details
    try:
        # Execute query to fetch image names
        query = f"SELECT image_name FROM hotel_images WHERE hotel_id={hotel_id};"
        cursor.execute(query)
        result = cursor.fetchall()

        # Extract image names into a list
        image_names = [row[0] for row in result]

        return image_names

    except Exception as e:
        print(f"Error: {e}")
        return []
    
def categorize_images(image_names):
    # Initialize categories dictionary
    categories = defaultdict(list)

    # Process each image name
    for image_name in image_names:
        # Convert image name to lowercase for uniformity
        image_name_lower = image_name.lower()

        # Category assignment based on content of image names
        if any(keyword in image_name_lower for keyword in ["room", "suite", "bed", "twin", "double"]):
            category = "Rooms"
        elif any(keyword in image_name_lower for keyword in ["bathroom", "shower", "towels", "toiletries"]):
            category = "Bathroom"
        elif any(keyword in image_name_lower for keyword in ["breakfast", "buffet", "dining", "restaurant", "meal"]):
            category = "Dining"
        elif any(keyword in image_name_lower for keyword in ["sports", "gym", "facility", "fitness"]):
            category = "Sports & Fitness"
        elif any(keyword in image_name_lower for keyword in ["exterior", "entrance", "view", "property"]):
            category = "Exterior"
        elif any(keyword in image_name_lower for keyword in ["interior", "reception", "lobby", "hall", "common"]):
            category = "Interior"
        else:
            category = "Miscellaneous"

        # Add the image name to the appropriate category
        categories[category].append(image_name)

    return categories


if __name__ == "__main__":

    db = Database(host="localhost", user="htech_ai", password="Htech786#")
    # db.create_database("expedia_db")
    # Initialize the database (connect to it)
    db.initialize_database("expedia_db")

    cursor = db.connection.cursor()


    # Fetch image names for hotel ID 10
    hotel_id = 800

    image_names = fetch_image_names(hotel_id,cursor)
    print("images names: ")
    print(image_names)

    print("-------------------------------------------------------------------------------------")
    room_names=fetch_room_names(hotel_id,cursor)
    print("room names : ")
    print(room_names)

    # Categorize the image names
    categories = categorize_images(image_names)

    # Display the results
    for category, images in categories.items():
        print(f"{category}:")
        for image in images:
            print(f"  - {image}")

    # if image_names:
    #     # Categorize images based on their names
    #     categorized_images = categorize_images(image_names)

    #     # Display the categorized results
    #     import pprint
    #     pprint.pprint(categorized_images)
    # else:
    #     print("No images found for the given hotel ID.")


    # images=fetch_image_names(cursor)
    # print(images)






