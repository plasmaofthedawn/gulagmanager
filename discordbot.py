import json
import os

import discord
from database import database
import logger


class GClient(discord.Client):

    async def on_ready(self):

        secret = json.loads(os.environ.get('SECRETS'))

        logger.log_channel = self.get_channel(secret["gulaglog"])

        self.frozen_members = []

        database.create_role_table()

        self.server = self.get_guild(secret["serverID"])
        self.category = self.get_channel(secret["gulagcategory"])
        self.gulagrole = self.server.get_role(secret["gulagrole"])
        self.gulagdict = {}

        await logger.log("Starting on server " + self.server.name)

        pairs = []
        for mem in self.server.members:
            for role in mem.roles:
                pairs.append((mem.id, role.id))

        database.create_role_rows(pairs)

        database.commit()

    async def on_member_join(self, member):

        roles = database.get_roles(member.id)

        await logger.log("Member" + str(member.name) + " has joined, freezing")

        self.frozen_members.append(member.id)

        log = "Giving roles:\n"

        for i in roles:
            try:
                role = self.server.get_role(int(i[0]))
                await member.add_roles(role)
                log += role.name + "\n"
            except Exception:
                pass

        await logger.log(log)

        database.commit()
        self.frozen_members.remove(member.id)
        await logger.log("Unfreezing member " + str(member.name))

    async def on_member_remove(self, member):
        await logger.log(member.name + " has left the server")
        await self.remove_gulag(member)

    async def on_member_update(self, before, after):

        new_roles = list(set(after.roles) - set(before.roles))
        old_roles = list(set(before.roles) - set(after.roles))

        if new_roles:
            await logger.log("Adding roles " + " ".join([i.name for i in new_roles]) + " to " + before.name)
            database.create_role_rows([(before.id, x.id) for x in new_roles])
        if old_roles:
            await logger.log("Removing roles " + " ".join([i.name for i in old_roles]) + " to " + before.name)
            database.remove_role_row([(before.id, x.id) for x in old_roles])

        if self.gulagrole.id in [x.id for x in new_roles]:
            await self.create_gulag(before)
        if self.gulagrole.id in [x.id for x in old_roles]:
            await self.remove_gulag(before)

        if before.id in self.frozen_members:
            await logger.log("Skipping " + before.name + " cause they was frozen.")
            return

        if not new_roles and not old_roles:
            return

        database.commit()

    async def remove_gulag(self, member):
        try:
            await logger.log("Removing gulag for " + member.name)
            await self.gulagdict[member.id].delete()
            del self.gulagdict[member.id]
        except KeyError as e:
            pass

    async def create_gulag(self, member):
        overwrites = {
            self.server.default_role: discord.PermissionOverwrite(read_messages=False),
            self.server.get_role(737416636302229515): discord.PermissionOverwrite(read_messages=True),
            self.server.me: discord.PermissionOverwrite(read_messages=True),
            member: discord.PermissionOverwrite(read_messages=True)
        }

        await member.add_roles(self.gulagrole)
        ch = await self.server.create_text_channel("gulag-" + str(member.id), category=self.category, overwrites=overwrites)

        await ch.send("pog")

        self.gulagdict[member.id] = ch
        await logger.log("Created gulag for " + member.name)




