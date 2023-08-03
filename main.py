#
import googlemaps
import os


def location_to_coordinates(gmaps, location):
    # Geocode the given location to get its coordinates
    geocode_result = gmaps.geocode(location)
    if not geocode_result:
        print("Location not found.")
        return {}

    location_coords = geocode_result[0]['geometry']['location']
    
    return (location_coords["lat"], location_coords["lng"])

def get_popular_areas(location, radius=10000, keyword='popular area'):
    places_result = gmaps.places(query=keyword, location=location, radius=radius)
    if 'results' in places_result:
        return places_result['results']
    else:
        return []


if __name__ == "__main__":
    # Replace YOUR_API_KEY with your actual API key
    API_KEY = os.environ["GMAPS_API_KEY"]
    gmaps = googlemaps.Client(key=API_KEY)

    place = input("Enter location: ")

    # Replace LATITUDE and LONGITUDE with the coordinates of the location you want to search around
    #LOCATION = (8.487681979172303, 76.95152664966565)
    LOCATION = location_to_coordinates(gmaps, place)

    print(LOCATION)

    # You can adjust the radius and keyword as needed
    RADIUS = 10000  # in meters
    KEYWORD = 'popular area'

    """popular_areas = get_popular_areas(LOCATION, RADIUS, KEYWORD)

    if popular_areas:
        print("Popular areas in the vicinity:")
        for place in popular_areas:
            print(place['name'], "at", place['formatted_address'])
    else:
        print("No popular areas found in the vicinity.")"""