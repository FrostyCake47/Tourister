import googlemaps
import os
import discord
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

def get_popular_areas(location, radius=10000, keyword='popular area'):
    places_result = gmaps.places(query=keyword, location=location, radius=radius)
    if 'results' in places_result:
        return places_result['results']
    else:
        return []

def get_place_images(api_key, place_id):
    place_details = gmaps.place(place_id=place_id, fields=['photos'])
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

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    KEYWORD = 'popular area'
    RADIUS = 10000
    try:
        if message.author == client.user:
            return
        
        if message.content.startswith("/popular"):
            place = str(message.content).split("/popular")[1]
            LOCATION = location_to_coordinates(gmaps, place)
            print(LOCATION)
            popular_areas = get_popular_areas(LOCATION, RADIUS, KEYWORD)
            print(popular_areas[0])
            
            for place in popular_areas:
                print(place['name'], "at", place['formatted_address'])
                #await message.channel.send(place['name'] + "at" + place['formatted_address'])

                embed=discord.Embed(title=place['name'], description=place['formatted_address'], color=0x772eff)
                await message.channel.send(embed=embed)
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
    RADIUS = 10000  # in meters
    KEYWORD = 'popular area'

    #popular_areas = get_popular_areas(LOCATION, RADIUS, KEYWORD)

    '''if popular_areas:
        print("Popular areas in the vicinity:")
        for place in popular_areas:
            print(place['name'], "at", place['formatted_address'])
    else:
        print("No popular areas found in the vicinity.")'''