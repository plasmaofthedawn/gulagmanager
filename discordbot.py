import json

import discord
import database
import logger


class GClient(discord.Client):

    async def on_ready(self):

        secret = json.load(open("secrets.json"))

        logger.log_channel = self.get_channel(secret["gulaglog"])

        self.frozen_members = []

        curr = database.get_cursor()

        database.create_role_table(curr)

        self.server = self.get_guild(secret["serverID"])
        self.category = self.get_channel(secret["gulagcategory"])
        self.gulagrole = self.server.get_role(secret["gulagrole"])
        self.gulagdict = {}

        await logger.log("Starting on server " + self.server.name)

        for mem in self.server.members:
            for role in mem.roles:
                database.create_role_row(curr, mem.id, role.id)

        database.commit()
        curr.close()

    async def on_member_join(self, member):

        curr = database.get_cursor()

        roles = database.get_roles(curr, member.id)

        await logger.log("Member" + str(member.name) + " has joined, freezing")

        self.frozen_members.append(member.id)

        log = "Giving roles:\n"

        for i in roles:
            try:
                role = self.server.get_role(int(i[0]))
                await member.add_roles(role)
                log += role.name + "\n"
            except Exception as e:
                pass

        await logger.log(log)

        database.commit()
        self.frozen_members.remove(member.id)
        await logger.log("Unfreezing member " + str(member.name))
        curr.close()

    async def on_member_remove(self, member):
        await logger.log(member.name + " has left the server")
        await self.remove_gulag(member)

    async def on_member_update(self, before, after):

        new_roles = list(set(after.roles) - set(before.roles))
        old_roles = list(set(before.roles) - set(after.roles))

        if new_roles:
            await logger.log("Adding roles " + " ".join([i.name for i in new_roles]) + " to " + before.name)
        if old_roles:
            await logger.log("Removing roles " + " ".join([i.name for i in old_roles]) + " to " + before.name)

        if self.gulagrole.id in [x.id for x in new_roles]:
            await self.create_gulag(before)
        if self.gulagrole.id in [x.id for x in old_roles]:
            await self.remove_gulag(before)

        if before.id in self.frozen_members:
            await logger.log("Skipping " + before.name + " cause they was frozen.")
            return

        if not new_roles and not old_roles:
            return

        curr = database.get_cursor()
        for i in new_roles:
            database.create_role_row(curr, before.id, i.id)

        curr = database.get_cursor()
        for i in old_roles:
            database.remove_role_row(curr, before.id, i.id)

        curr.close()
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




