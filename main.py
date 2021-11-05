import logging
import discord
import configparser
import feedparser

# Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Config
config = configparser.ConfigParser()

# Parser
feed = feedparser.parse('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.atom')


# Discord Bot
client = discord.Client()

config.read('example.ini')


client.run('your token here')