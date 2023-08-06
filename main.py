import googlemaps
import os
import discord
from discord import app_commands
import requests
import asyncio

TOKEN = os.environ['TOURISTER_SECRET']
API_KEY = os.environ["GMAPS_API_KEY"]
print(TOKEN)

client = discord.Client(command_prefix='/', intents=discord.Intents().all())
tree = app_commands.CommandTree(client)

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


def get_place_main_photo(api_key, place_id, max_width=400):

    base_url = "https://maps.googleapis.com/maps/api/place/photo"
    max_width_param = f"maxwidth={max_width}"
    place_id_param = f"photoreference={place_id}"
    api_key_param = f"key={api_key}"

    url = f"{base_url}?{max_width_param}&{place_id_param}&{api_key_param}"
    return url

def get_pic_url(api_key, place_id):
    place_details = gmaps.place(place_id=place_id, fields=['photo'])
    photo_id = place_details['result']['photos'][0]['photo_reference']
    print("photo id=", photo_id)

    base_url = "https://maps.googleapis.com/maps/api/place/photo"
    params = {
        "key": api_key,
        "photoreference": photo_id,
        "maxheight": 400
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.url
    else:
        print("Error:", response.status_code, response.text)
        return None


def get_road_distance(origin, destination, mode="driving"):
    try:
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
    await tree.sync(guild=discord.Object(id=1137264222603059300))
    

@tree.command(name="test", description='description',guild=discord.Object(id=1137264222603059300))
async def test(interaction: discord.Interaction):
    try:
        await interaction.response.send_message("omg")
    
    except Exception as e:
        print(e)


#@client.event
#async def on_message(message):

@tree.command(name="locate", description='Location',guild=discord.Object(id=1137264222603059300))
async def locate(message: discord.Interaction, location: str, keyword :str, search_radius: int):

    RADIUS = search_radius
    KEYWORD = keyword
    try:
        if message:
            place = location
            LOCATION = location_to_coordinates(gmaps, place)
            print(LOCATION)
            popular_areas = get_popular_areas(LOCATION, RADIUS, KEYWORD)
            print(popular_areas[0])
            
            for i, place in enumerate(popular_areas):
                print(place['name'], "at", place['formatted_address'])
                place_id = place['place_id']
                print("this is the place id", place_id)

                destination_coordinates = (place['geometry']['location']['lat'], place['geometry']['location']['lng'])
                distance = get_road_distance(LOCATION, destination_coordinates)
                image_url = get_place_main_photo(API_KEY, place_id)
                url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"

                if distance is None:
                    distance = 'NULL'
                
                print("distance = ", distance)
                image_url = get_pic_url(API_KEY, place_id)
                print(url)

                embed=discord.Embed(title=f"{i+1}) {place['name']}", description=place['formatted_address'], color=0x772eff, url=url )
                embed.add_field(name="Rating", value=f"{place['rating']} ⭐ ({place['user_ratings_total']})", inline=False)
                embed.add_field(name="Distance", value=f"{round(distance/1000, 1)} km", inline=False)
                embed.set_image(url=image_url)

                await message.channel.send(embed=embed)
                
                if i == 1:
                    break


    except Exception as e:
        print("error is = ", e)
        await message.channel.send("ayo something went wrong, try again")


if __name__ == "__main__":
    gmaps = googlemaps.Client(key=API_KEY)
    client.run(TOKEN)