import logging
import discord
import configparser
import feedparser
import geopy.distance
import time

# Logging
#logger = logging.getLogger('discord')
#logger.setLevel(logging.DEBUG)
#handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
#handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#logger.addHandler(handler)

# Config
config = configparser.ConfigParser()
config.read('conf.ini')

bottoken = config['DEFAULT']['token']
channelid = config['DEFAULT']['channel']
print('sending to channel ' + channelid)
looptime = 3

waypoint = (30.8715, 120.2730)
waypoint2 = (40.8715, 120.2230)

# Discord Bot
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print('------')
    while True:
        # Parser
        d = feedparser.parse('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.atom')
        quakecords = (d.entries[0].where.coordinates[1], d.entries[0].where.coordinates[0])
        print(quakecords)
        print(waypoint)
        distance = geopy.distance.distance(waypoint, quakecords).miles
        print('eathquake ' + str(distance) + ' miles away')
        #^ this part works great ^
        if distance < 10000:
            print('eathquake!!')
            channel = client.get_channel(channelid)
            await channel.send('earthquake!!')
        time.sleep(looptime)
       


client.run(bottoken)