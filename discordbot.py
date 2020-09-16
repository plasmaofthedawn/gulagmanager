import json

import discord
import database


class GClient(discord.Client):

    async def on_ready(self):

        secret = json.load(open("secrets.json"))

        db = database.connect()

        curr = db.cursor()

        curr.execute(
            """
            CREATE TABLE roles (
                id serial PRIMARY KEY,
                userid NUMERIC NOT NULL,
                roleid NUMERIC NOT NULL
            )
            """
        )

        server = self.get_guild(secret["serverID"])

        for mem in server.members:
            for role in mem.roles:
                curr.execute("INSERT INTO roles (userid, roleid) VALUES ({}, {})".format(mem.id, role.id))

        db.commit()

        curr.close()
        db.close()

        quit(21)

