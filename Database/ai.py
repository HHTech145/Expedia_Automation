import openai
import json

# Set up your OpenAI API key
openai.api_key = "your-api-key"

class HotelImageCategorizer:
    def __init__(self, api_key):
        openai.api_key = api_key

    def create_prompt(self, image_names,room_names):
        # Create a structured prompt using f-string for dynamic insertion of room names and image names
        prompt = f"""
        You are an AI trained to categorize hotel images based on their names. Your goal is to organize these images into categories that make sense for a hotel. The categories are as follows:


        Here are the image names that need to be categorized:
        {json.dumps(image_names)}

        room names : {json.dumps(room_names)}
        Check room names pick one room and check which image belongs to it.

        For each image, decide which category it belongs to based on its name and group similar images together under the appropriate category. Please categorize the images into one or more of the following groups: Room Types, Amenities, Hotel Services, and Hotel Spaces.

        Be sure to provide each image with a clear, relevant category, keeping in mind that some images may belong to multiple categories. Your output should clearly reflect the appropriate grouping of these images by their respective types and functions within the hotel.

        Thank you for organizing these images efficiently and accurately.
        """
        return prompt

    def categorize_images(self, image_names,room_names):
        """
        Takes a list of image names and returns the categorized list in JSON format.
        """
        prompt = self.create_prompt(image_names,room_names)

        # Request a response from OpenAI's new API format
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # or any other model like gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )

        # Parse the response
        categorized_data = response['choices'][0]['message']['content']
        return categorized_data


def categorize_hotel_images(image_names, room_names,api_key):
    """
    A function to categorize hotel images by room type, amenities, services, and spaces using OpenAI.
    """
    categorizer = HotelImageCategorizer(api_key)
    categorized_images = categorizer.categorize_images(image_names,room_names)
    return categorized_images


# Example usage:

if __name__ == "__main__":
    # List of image names (this would be your actual image names to categorize)

    image_names=['Restaurant', 'Room, 1 Queen Bed | Premium bedding, down comforters, minibar, in-room safe', 'Lobby', 'Sauna, spa tub, steam room, body treatments, hot stone massages', 'Exterior', 'Indoor pool', 'Junior Suite | Premium bedding, down comforters, minibar, in-room safe', 'Property amenity', 'Daily English breakfast (GBP 24 per person)', 'Meeting facility', 'Family Room, 1 Double Bed, City View | Bathroom | Combined shower/tub, rainfall showerhead, designer toiletries', 'Bar (on property)', 'Premium bedding, down comforters, minibar, in-room safe', 'Combined shower/tub, rainfall showerhead, designer toiletries', 'In-room dining', 'Fitness facility', 'Superior Room, 2 Twin Beds, City View | Bathroom | Combined shower/tub, rainfall showerhead, designer toiletries', 'Superior Room, 1 Queen Bed, City View | Bathroom | Combined shower/tub, rainfall showerhead, designer toiletries', 'Superior Room, 2 Twin Beds, City View | Premium bedding, down comforters, minibar, in-room safe', 'Lobby lounge', 'Family Room, 1 Double Bed, City View | Premium bedding, down comforters, minibar, in-room safe', 'Reception', 'Superior Room, 1 Queen Bed, City View | Premium bedding, down comforters, minibar, in-room safe', 'Standard Room, 1 Queen Bed, City View | Premium bedding, down comforters, minibar, in-room safe']
    room_names= ['Standard Room, 1 Queen Bed, City View', 'Junior Suite', 'Superior Room, 1 Queen Bed, City View', 'Room, 1 Queen Bed, View', 'Superior Room, 2 Twin Beds, City View']
    # Your OpenAI API key
    api_key = "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"  # Replace with your OpenAI API key
    
    # Get the categorized result
    categorized_images = categorize_hotel_images(image_names,room_names, api_key)
    
    # Output the result
    print("Categorized Images:", categorized_images)
