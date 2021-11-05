import logging
import discord
import configparser
import feedparser
import geopy.distance

# Logging
#logger = logging.getLogger('discord')
#logger.setLevel(logging.DEBUG)
#handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
#handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#logger.addHandler(handler)

# Config
config = configparser.ConfigParser()

waypoint = (30.8715, 120.2730)
waypoint2 = (40.8715, 120.2230)

# Parser
d = feedparser.parse('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.atom')
quakecords = (d.entries[0].where.coordinates[1], d.entries[0].where.coordinates[0])
print(quakecords)
print(waypoint)
distance = geopy.distance.distance(waypoint, quakecords).miles
print("eathquake " + str(distance) + " miles away")

# Discord Bot
#client = discord.Client()

#config.read('example.ini')

#client.run('your token here')