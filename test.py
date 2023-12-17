from urllib.parse import urlparse, parse_qs

def extract_coordinates_from_url(url):
    # Parse the URL
    parsed_url = urlparse(url)

    # Extract the query parameters
    query_params = parse_qs(parsed_url.query)

    # Extract the latitude and longitude
    if 'q' in query_params:
        coordinates = query_params['q'][0].split(',')
        latitude = float(coordinates[0])
        longitude = float(coordinates[1])
        return latitude, longitude
    else:
        return None

# Example URL
url = "https://maps.google.com/maps?q=41.42406235873679,33.80087691534251&hl=es;z=14&amp;output=embed"

# Extract coordinates
coordinates = extract_coordinates_from_url(url)

if coordinates:
    print("Latitude:", coordinates[0])
    print("Longitude:", coordinates[1])
else:
    print("Coordinates not found in the URL.")