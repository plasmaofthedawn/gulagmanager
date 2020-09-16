import discord
import json
import flask



if __name__ == '__main__':
    secrets = json.load(open("secrets.json"))
    client = discord.Client()

    client.run(secrets["discordtoken"])
