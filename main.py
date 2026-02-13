import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
from db.connection import get_database
import time
import aiosqlite

load_dotenv()
TOKEN = os.getenv("TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="r:", intents=intents)
starter_time = time.perf_counter()


@bot.event
async def on_ready():
    sync = await bot.tree.sync()
    print(f"Synced {len(sync)} app commands!")
    print(f"Logged in as {bot.user}!")

async def setup_database():
    async with aiosqlite.connect("database.db") as db:
        with open("db/setup.sql", "r") as f:
            await db.executescript(f.read())
        await db.commit()


class app_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="ping")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        await ctx.send((f"Aaaand pong! in {latency}ms"))

    @commands.command(name="welcome", description="Setup your Welcome channel")
    @commands.default_permissions(administrator=True)
    async def set_welcome(self, interaction: discord.Interaction, channel: discord.TextChannel):
        await interaction.response.defer()

        db = await get_database()

        await db.execute(
            """
                INSERT INTO server (guild_id, welcome_channel)
                VALUES (?, ?)
                ON CONFLICT(guild_id) 
                DO UPDATE SET welcome_channel = excluded.welcome_channel 
            """,
            (interaction.guild.id, channel.id),
        )

        await db.commit()
        try:
            await interaction.followup.send(f"Welcome channel set to {channel.mention}")
        except Exception as e:
            await interaction.followup.send(f"Error: {e}", ephemeral=True)

    @app_commands.command(name="counting", description="Set up your counting channel")
    @app_commands.default_permissions(administrator=True)
    async def set_counting(self, interaction: discord.Interaction, channel: discord.TextChannel):
        await interaction.response.defer()

        db = await get_database()

        await db.execute(
            """
                INSERT INTO server (guild_id, counting_channel)
                VALUES (?, ?)
                ON CONFLICT(guild_id) DO UPDATE SET counting_channel = excluded.counting_channel 
             """,
            (interaction.guild.id, channel.id),
        )

        await db.commit()
        try:
            await interaction.followup.send(f"Counting channel set to {channel.mention}")
        except Exception as e:
            await interaction.followup.send(f"Error: {e}", ephemeral=True)

    @app_commands.command(name="modlog", description="Set up your modlog channel")
    @app_commands.default_permissions(administrator=True)
    async def set_modlog(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        await interaction.response.defer()

        db = await get_database()

        await db.execute(
            """
                INSERT INTO server (guild_id, log_channel)
                VALUES (?, ?)
                ON CONFLICT(guild_id) 
                DO UPDATE SET log_channel = excluded.log_channel 
            """,
            (interaction.guild.id, channel.id),
        )

        await db.commit()

        try: 
            await interaction.followup.send(f"Log channel set to {channel.mention}")
        except Exception as e:
            await interaction.followup.send(f"Error: {e}", ephemeral=True)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        db = await get_database()

        async with db.execute(
            "SELECT welcome_channel FROM server WHERE guild_id = ?", (member.guild.id,)
        ) as cursor:
            row = await cursor.fetchone()

        if row and row[0]:
            channel = member.guild.get_channel(int(row[0]))
            if channel:
                try:
                    await channel.send(
                        f"Welcome {member.mention} to {member.guild.name}!"
                    )
                except discord.Forbidden:
                    print(f"Missing permissions to welcome message in {channel}")

    @app_commands.command(name="commands")
    async def show_commands(self, ctx: discord.ext.commands.Context):
        embed = discord.Embed(
            title="Commands", description=None, color=discord.Color.green()
        )

        for cog_name, cog in self.bot.cogs.items():
            commands_list = cog.get_commands()
            slash_commands = cog.get_app_commands()
            if commands_list or slash_commands:
                commands_info = " ".join([f"`r:{cmd.name}`" for cmd in commands_list])
                app_info = " ".join([f"`/{cmd.name}`" for cmd in slash_commands])
                embed.add_field(
                    name=f"{cog_name}",
                    value=f"{commands_info} {app_info}",
                    inline=False,
                )

        await ctx.send(embed=embed)


async def main():
    await setup_database()
    extensions = [
        "cogs.fun",
        "cogs.actions",
        "cogs.count",
        # NOTE: cogs.ai is VERY slow if you don't have a CUDA GPU ( and could slow down your CPU ). If you want, remove the next line
        "cogs.ai"
        "cogs.logs",
        "cogs.tod",
        "cogs.exp",
        "cogs.stats",
        "cogs.admin"] 

    for ex in extensions:
        try:
            await bot.load_extension(ex)
            print(f"Loaded {ex}!")
        except Exception as e:
            print(f"Failed to load {ex}, reason {e}")
    await bot.add_cog(app_commands(bot))
    await bot.start(TOKEN)


asyncio.run(main())
