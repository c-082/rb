import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import random
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="r:", intents=intents)

@bot.event
async def on_ready():
    try:
        sync = await bot.tree.sync()
        print(f"Synced {len(sync)} commands!")
        print(f"Logged in as {bot.user}!")
    except Exception as e:
        print(f"Failed to load commands: {e}")

class Greeting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self,member):
        channel = discord.utils.get(member.guild.text_channels, name="✦-welcomes")
        if channel:
            await channel.send(f"Welcome {member.mention} to Ralsei's Castle Town!")


@bot.event
async def on_command_error(ctx,error):
    await ctx.send(f"Error: {error}")

@bot.tree.command(name="commands", description="Shows all available commands")
async def show_commands(interaction: discord.Interaction):
    embed = discord.Embed(
            title="Commands",
            description=None,
            color=discord.Color.green()
            )

    for cog_name, cog in bot.cogs.items():
        commands_list = cog.get_commands()
        app_command_list = cog.get_app_commands()

        if commands_list:

            commands_info = "\n".join([f"r:{cmd.name}" for cmd in commands_list])
            embed.add_field(
                name=f"{cog_name} Commands",
                value=commands_info,
                inline=False
            ) 
        
        if app_command_list:

            app_command_info = "\n".join([f"/{cmd.name} - {cmd.description}" for cmd in app_command_list])
            embed.add_field(
                    name=f"{cog_name} Commands",
                    value=app_command_info,
                    inline=False
                    )

    await interaction.response.send_message(embed=embed)  

@bot.event
async def on_message_sent(message):
    counter = 0
    if message.author.id == 1367051487968100443 and counter < 1:
        await ctx.send("We miss you..")
        counter += 1


async def main():
    await bot.add_cog(Greeting(bot))
    extensions = ["cogs.fun", "cogs.actions", "cogs.admin"]

    for ex in extensions:
        try:
            await bot.load_extension(ex)
            print(f"Loaded {ex}!")
        except Exception as e:
            print(f"Failed to load {ex}, reason {e}")
    await bot.start(TOKEN)

asyncio.run(main())
