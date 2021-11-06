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
channelid = int(config['DEFAULT']['channel'])

looptime = 15

waypoint = (30.8715, 120.2730)
waypoint2 = (40.8715, 120.2230)

print('sending to channel ' + str(channelid))
print('------')
# Discord Bot
client = discord.Client()

@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))
    print('------')
    d = feedparser.parse('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.atom')
    modified = d.modified
    while True:
        # Parser
        d = feedparser.parse('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.atom', modified=modified)
        if d.status == 304:
            #print('unchanged')
            time.sleep(looptime)
            continue
        modified = d.modified
        print('updated at ' + modified)
        quakecords = (d.entries[0].where.coordinates[1], d.entries[0].where.coordinates[0])
        print(quakecords)
        # Find Distance
        distance = geopy.distance.distance(waypoint, quakecords).miles
        print('eathquake ' + str(distance) + ' miles away')
        # Send Message if within distance
        if distance < 100:
            print('eathquake!!')
            channel = client.get_channel(channelid)
            await channel.send('earthquake!!')
        time.sleep(looptime)

client.run(bottoken)