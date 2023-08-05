import googlemaps
import os
import discord
import random
#from discord.ext import app_commands

#https://discord.com/api/oauth2/authorize?client_id=1137022749966082131&permissions=534723950656&scope=bot%20applications.commands
TOKEN = os.environ['TOURISTER_SECRET']
API_KEY = os.environ["GMAPS_API_KEY"]
print(TOKEN)

client = discord.Client(command_prefix='/', intents=discord.Intents().all())
#tree = app_commands.CommandTree(client)

def location_to_coordinates(gmaps, location):
    geocode_result = gmaps.geocode(location)
    if not geocode_result:
        print("Location not found.")
        return {}

    location_coords = geocode_result[0]['geometry']['location']
    
    return (location_coords["lat"], location_coords["lng"])

def get_popular_areas(location, radius=5000, keyword='point of interest'):
    places_result = gmaps.places(query=keyword, location=location, radius=radius)
    if 'results' in places_result:
        return places_result['results']
    else:
        return []

def get_place_images(api_key, place_id):
    place_details = gmaps.place(place_id=place_id, fields='photo')
    if 'photos' not in place_details['result']:
        print("No photos found for the place.")
        return []

    # Step 4: Extract the photo references from the details response
    photo_references = [photo['photo_reference'] for photo in place_details['result']['photos']]

    # Step 5: Use the "Places Photo" API to get the images based on the photo references
    image_urls = []
    for reference in photo_references:
        image_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={reference}&key={api_key}"
        image_urls.append(image_url)

    return image_urls


def get_place_main_photo(api_key, place_id, max_width=400):

    base_url = "https://maps.googleapis.com/maps/api/place/photo"
    max_width_param = f"maxwidth={max_width}"
    place_id_param = f"photoreference={place_id}"
    api_key_param = f"key={api_key}"

    url = f"{base_url}?{max_width_param}&{place_id_param}&{api_key_param}"
    return url

def get_road_distance(origin, destination, mode="driving"):
    try:
        # Get the distance matrix for the given coordinates
        result = gmaps.distance_matrix(
            origins=[origin],
            destinations=[destination],
            mode=mode,
            units="metric"
        )

        if result["rows"][0]["elements"][0]["status"] == "OK":
            distance = result["rows"][0]["elements"][0]["distance"]["value"]
            return distance
        else:
            print("Error: Unable to calculate road distance.")
            return None
    except googlemaps.exceptions.ApiError as e:
        print("Error:", e)
        return None


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    KEYWORD = 'point of interest'
    RADIUS = 5000
    try:
        if message.author == client.user:
            return
        
        if message.content.startswith("/popular"):
            place = str(message.content).split("/popular")[1]
            LOCATION = location_to_coordinates(gmaps, place)
            print(LOCATION)
            popular_areas = get_popular_areas(LOCATION, RADIUS, KEYWORD)
            random.shuffle(popular_areas)
            print(popular_areas[0])
            
            for i, place in enumerate(popular_areas):
                print(place['name'], "at", place['formatted_address'])
                #await message.channel.send(place['name'] + "at" + place['formatted_address'])
                place_id = place['place_id']
                print("this is the place id", place_id)

                destination_coordinates = (place['geometry']['location']['lat'], place['geometry']['location']['lng'])
                distance = get_road_distance(LOCATION, destination_coordinates)
                image_url = get_place_main_photo(API_KEY, place_id)
                url = f"https://www.google.com/maps/place/{place_id}"

                if distance is None:
                    distance = 'NULL'
                
                print("distance = ", distance)
                #print(image_url)

                embed=discord.Embed(title=f"{i+1}) {place['name']}", description=place['formatted_address'], color=0x772eff, url=url )
                embed.add_field(name="Rating", value=f"{place['rating']} ⭐ ({place['user_ratings_total']})", inline=False)
                embed.add_field(name="Distance", value=f"{round(distance/1000, 1)} km", inline=False)
                embed.set_image(url=image_url)
                await message.channel.send(embed=embed)
                if i == 5:
                    break


    except Exception as e:
        print(e)
        await message.channel.send("ayo something went wrong, try again")


if __name__ == "__main__":
    # Replace YOUR_API_KEY with your actual API key
    gmaps = googlemaps.Client(key=API_KEY)
    client.run(TOKEN)

    #place = input("Enter location: ")

    #LOCATION = (8.487681979172303, 76.95152664966565)
    #LOCATION = location_to_coordinates(gmaps, place)

    #print(LOCATION)

    # You can adjust the radius and keyword as needed
    #RADIUS = 10000  # in meters
    #KEYWORD = 'popular area'

    #popular_areas = get_popular_areas(LOCATION, RADIUS, KEYWORD)

    '''if popular_areas:
        print("Popular areas in the vicinity:")
        for place in popular_areas:
            print(place['name'], "at", place['formatted_address'])
    else:
        print("No popular areas found in the vicinity.")'''