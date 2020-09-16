import discordbot
import database
import json



if __name__ == '__main__':
    secrets = json.load(open("secrets.json"))
    client = discordbot.GClient()
    # database.connect()
    client.run(secrets["discordtoken"])
