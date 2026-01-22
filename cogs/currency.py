import aiosqlite
import discord
import random
from discord.ext import commands
from discord import app_commands
from discord.utils import get
from db.connection import get_database
import random

class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_user_cur(self, user_id: int):
        db = await get_database()

        async with db.execute("SELECT currency FROM user WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()

        return row if row and row[0] else 0

    async def update_user_cur(self, user_id: int, amount: int):
        db = await get_database()

        await db.execute("""
        UPDATE user
        SET currency = currency + ?
        WHERE user_id = ?
        """, (amount, user_id))

        await db.commit()

    def coinflip(self):
        return random.randint(1, 2)

    @commands.command(name="coinflip", aliases=["cf"])
    async def coinflip(self, ctx):
        if self.coinflip() == 1:
            await ctx.channel.send("1. Heads")
            await self.update_user_cur(ctx.author.id, random.randrange(10, 30))
        else:
            await ctx.channel.send("2. Tails")

async def setup(bot):
    await bot.add_cog(Currency(bot))
