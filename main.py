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

bottoken = config['default']['token']
channelid = int(config['default']['channel'])
roleid = config['default']['roleid']

looptime = int(config['default']['frequency'])

waypoint = config['default']['waypointlat'], config['default']['waypointlon']
waypointname = config['default']['waypointname']
pingdist = int(config['default']['distance'])

print('channelid ' + str(channelid))
print('waypoint ' + waypointname + ' ' + str(waypoint) + ' ' + str(type(waypoint)))
print('looptime ' + str(looptime))
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
            time.sleep(looptime)
            continue
        modified = d.modified
        print()
        print('--updated at ' + modified)
        quakecords = (d.entries[0].where.coordinates[1], d.entries[0].where.coordinates[0])
        # Find Distance
        distance = geopy.distance.distance(waypoint, quakecords).miles
        print(str(d.entries[0].tags[1].term) + 'earthquake ' + str("%.2f" % distance) + ' miles away ' + str(quakecords))
        # Send Message if within distance
        if distance < pingdist:
            print('Under ' + str(pingdist) + ' sending Discord Message!!')
            await channel.send('<@&' + roleid + '>\n`' + str(d.entries[0].tags[1].term) + '` earthquake `' + str("%.2f" % distance) + '` miles from ' + waypointname + '!!\n\n' + 'Time: `' + d.entries[0] + '`\nDepth: `' + d.entries[0].georss_elev + ' Meters`\n' + d.entries[0].link)
        oldid = d.entries[0].id
        time.sleep(looptime)

client.run(bottoken)