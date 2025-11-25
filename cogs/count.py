import discord
from discord.ext import commands
from discord import app_commands

class Count(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.counter = 0

    @commands.Cog.listener()
    async def on_message_send(self, message):
        if int(message) == self.counter + 1 and message.channel.id == 1416249596757282859:
            print(True)
        elif int(message) != self.counter + 1 and message.channel.id == 1416249596757282859:
            print(False)

async def setup(bot):
    await bot.add_cog(Count(bot))
