import json

import discord
import database


class GClient(discord.Client):

    async def on_ready(self):

        self.frozen_members = []

        secret = json.load(open("secrets.json"))

        curr = database.get_cursor()

        database.create_role_table(curr)

        self.server = self.get_guild(secret["serverID"])
        self.category = self.get_channel(secret["gulagcategory"])
        self.gulagrole = self.server.get_role(secret["gulagrole"])

        for mem in self.server.members:
            for role in mem.roles:
                database.create_role_row(curr, mem.id, role.id)

        database.commit()
        curr.close()

    async def on_message(self, message):
        try:
            await self.create_gulag(self.server.get_member(int(message.content)))
        except ValueError:
            pass

    async def on_member_join(self, member):

        curr = database.get_cursor()

        roles = database.get_roles(curr, member.id)

        self.frozen_members.append(member.id)

        print(roles)

        for i in roles:
            try:
                await member.add_roles(self.server.get_role(int(i[0])))
            except Exception as e:
                pass

        database.commit()
        self.frozen_members.remove(member.id)
        curr.close()

    async def on_member_update(self, before, after):
        if before.id in self.frozen_members:
            print("skipping", before.id)
            return

        new_roles = list(set(after.roles) - set(before.roles))
        old_roles = list(set(before.roles) - set(after.roles))

        if not new_roles and not old_roles:
            return

        print(before.name, [i.name for i in new_roles], [i.name for i in old_roles])

        curr = database.get_cursor()
        for i in new_roles:
            database.create_role_row(curr, before.id, i.id)

        curr = database.get_cursor()
        for i in old_roles:
            database.remove_role_row(curr, before.id, i.id)

        curr.close()
        database.commit()

    async def create_gulag(self, member):
        overwrites = {
            self.server.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True)
        }

        await member.add_roles(self.gulagrole)

        await self.server.create_text_channel(str(member.id) + "-gulag", category=self.category, overwrites=overwrites)



