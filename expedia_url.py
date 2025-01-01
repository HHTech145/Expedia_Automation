from urllib.parse import urlencode, urlparse

# Original URL
base_url = "https://www.expedia.co.uk/London-Hotels-Great-Cumberland-Place.h21659.Hotel-Information"

# Parse the URL to get the path
parsed_url = urlparse(base_url)

# Extract the property name from the URL path (second-to-last part before `.hXXXXX`)
path_parts = parsed_url.path.split('/')
property_name = path_parts[-2].replace('-', ' ')  # Replace hyphens with spaces

# Define the query parameters as a dictionary with f-string for dynamic property name
params = {
    "chkin": "2024-12-29",
    "chkout": "2024-12-31",
    "x_pwa": "1",
    "rfrr": "HSR",
    "pwa_ts": "1734959065478",
    "referrerUrl": "aHR0cHM6Ly93d3cuZXhwZWRpYS5jby51ay9Ib3RlbC1TZWFyY2g%3D",
    "useRewards": "false",
    "rm1": "a2",
    "regionId": "553248621538637513",
    "destination": f"{property_name.replace(' ', '+')}",  # Dynamically set destination
    "destType": "MARKET",
    "selected": "7763320",
    "latLong": "53.421071,-2.998314",
    "sort": "RECOMMENDED",
    "top_dp": "323",
    "top_cur": "GBP",
    "userIntent": "",
    "selectedRoomType": "200714388",
    "selectedRatePlan": "203654355",
    "searchId": "6bd23021-5d37-4613-8940-64d0ec3160e7",
    "propertyName": f"{property_name.replace(' ', '+')}"  # Dynamically set propertyName
}

# Create the full URL with query parameters
full_url = f"{base_url}?{urlencode(params)}"

# Print the resulting URL
print("-------------url:",full_url)



