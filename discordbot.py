import discord


class GClient(discord.Client):

    async def on_ready(self):

        print("a")