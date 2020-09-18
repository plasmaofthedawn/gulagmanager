import discordbot
import json

if __name__ == '__main__':
    secrets = json.load(open("secrets.json"))
    client = discordbot.GClient()
    client.run(secrets["discordtoken"])
