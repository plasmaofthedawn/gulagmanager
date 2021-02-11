import os

import discordbot
import json
import discord

if __name__ == '__main__':

    intents = discord.Intents(members=True, guilds=True, messages=True)

    secrets = json.loads(os.environ.get('SECRETS'))
    client = discordbot.GClient(intents=intents)
    client.run(secrets["discordtoken"])
