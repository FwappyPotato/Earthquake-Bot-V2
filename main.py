import logging
import discord
import configparser
import feedparser
import geopy.distance
import time
import asyncio

# Logging
#logger = logging.getLogger('discord')
#logger.setLevel(logging.DEBUG)
#handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
#handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#logger.addHandler(handler)

logging.basicConfig(level=logging.INFO)

# Config
config = configparser.ConfigParser()
config.read('conf.ini')

bottoken = config['default']['token']
channelid = int(config['default']['channel'])
roleid = config['default']['roleid']

looptime = int(config['default']['frequency'])

waypoint1 = (float(config['default']['waypoint1lat']), float(config['default']['waypoint1lon']))
waypoint1name = config['default']['waypoint1name']
waypoint2 = (float(config['default']['waypoint2lat']), float(config['default']['waypoint2lon']))
waypoint2name = config['default']['waypoint2name']
waypoint3 = (float(config['default']['waypoint3lat']), float(config['default']['waypoint3lon']))
waypoint3name = config['default']['waypoint3name']

pingdist = int(config['default']['distance'])

print('channelid ' + str(channelid))
print('roleid ' + str(roleid))
print('waypoint1 ' + waypoint1name + ' ' + str(waypoint1) + ' ' + str(type(waypoint1)))
print('waypoint2 ' + waypoint2name + ' ' + str(waypoint2) + ' ' + str(type(waypoint2)))
print('waypoint3 ' + waypoint3name + ' ' + str(waypoint3) + ' ' + str(type(waypoint3)))
print('pingdist ' + str(pingdist) + ' miles')
print('looptime ' + str(looptime) + ' seconds')

# Discord Bot
client = discord.Client()

@client.event
async def on_ready(): # Yes this is bad, I know... Tell me how to do it better
    print('------------')
    print('logged in as {0.user}'.format(client))
    print('------------')
    # Setup
    channel = client.get_channel(channelid)
    d = feedparser.parse('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.atom')
    modified = d.modified
    oldid = d.entries[0].id
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="USGS Earthquakes"))
    #print(d)
    # Main Loop
    while True:
        # Parser
        d = feedparser.parse('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.atom', modified=modified)
        if d.status == 304 or d.entries[0].id == oldid:
            #print('unchanged')
            await asyncio.sleep(looptime)
            continue
        modified = d.modified
        print()
        print('--updated at ' + modified)
        quakecords = (float(d.entries[0].where.coordinates[1]), float(d.entries[0].where.coordinates[0]))
        # Find Distance
        distance1 = geopy.distance.distance(waypoint1, quakecords).miles
        distance2 = geopy.distance.distance(waypoint2, quakecords).miles
        distance3 = geopy.distance.distance(waypoint3, quakecords).miles
        print(str("%.2f" % distance1) + ' miles away ' + ' --- ' + str(d.entries[0].title) + ' ' + str(quakecords))
        # Send Message if within distance
        if distance1 < pingdist or distance2 < pingdist or distance3 < pingdist:
            print('Under ' + str(pingdist) + ' miles sending Discord Message!!')
            await channel.send('<@&' + roleid + '>\n**' + str(d.entries[0].title) + '**\n`' + str("%.2f" % distance1) + '` miles from ' + waypoint1name + '\n`' + str("%.2f" % distance2) + '` miles from ' + waypoin2tname + '\n`' +str("%.2f" % distance3) + '` miles from ' + waypoint3name + '\n\n' + 'Time: `' + d.entries[0].updated + '`\nDepth: `' + d.entries[0].georss_elev + ' Meters`\nLocation: `' + str(quakecords) + '`\n' + d.entries[0].link)
        oldid = d.entries[0].id
        await asyncio.sleep(looptime)

client.run(bottoken)