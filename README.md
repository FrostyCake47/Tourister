![Screenshot 2023-08-06 233538](https://github.com/FrostyCake47/Tourister/assets/47393739/2d12343e-bb40-45f9-9e24-99d197515c2b)# TOURISTER

This is a project made using GMaps API and represented as a discord chatbot. It allows us to quickly search for a variety of places in locality with our point of interests, such as 'popular places', historical sites', 'tourist attraction'. High flexiblity is also provided as one can search location with custon keywords also like 'restaurants', 'hotels' etc making planning for the trips easier.
<br /> It also comes with addional functionalities like <br /> ৹ Calculating a distance between two location and providing the time required for the travel <br /> ৹ Converting Address to Coordinates and vice versa

# Team name - iostream

# Team members

[Akash P](https://github.com/FrostyCake47) <br />
[Niranjana V](https://github.com/Niranjana-2003) <br />
[Muhammed Muhnis](https://github.com/) <br />

# Youtube Demo

# How the tool works
The tool works using Google maps API to retrieve data and process and location and uses Discord API to give a visual representation to the clients <br /> 
It has 4 main prompts <br /> <br />

```/locate [location] [key_word] [search_radius]``` <br /> 
Returns an discord embed of 5 top results matching the inputs <br/> 
1) location of your preferred city <br />
2) keyword indicates your point of interests, eg - 'popular places', 'historic building, 'restaurants' <br />
3) Search radius in km <br /> <br />
![locate](/screenshot/1.png)
![locate](/screenshot/2.png)
![locate](/screenshot/9.png)


```/distance [location1] [location2]```  <br />
Returns the distance between location1 and location2 and also the time required to travel between the two points <br /> <br /> 
![locate](/screenshot/3.png)
![locate](/screenshot/4.png)

```/loc_to_coord [location]``` <br /> 
Converts the Adress of given location and returns the coordinates of the point <br /> <br /> 
![locate](/screenshot/5.png)
![locate](/screenshot/6.png)

```/coord_to_loc [lat] [lng]``` <br /> 
Converts the given latitiute and longitude and returns the address of the location. <br /> <br /> 
![locate](/screenshot/7.png)
![locate](/screenshot/8.png)

```/help``` <br /> 
Provides the command and infos in discord chat <br />


# Libraries used
Google Maps API and Discord API

# How to configure
1) open cmd and enter ```pip install googlemaps``` and ```pip install discord.py```

# How to Run
open and run _main.py_
