import discord
import aiosqlite
from db.connection import get_database
from discord.ext import commands

class Stats(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def get_user_exp_stats(self, user_id: int, guild_id: int):
        db = await get_database()

        async with db.execute("SELECT exp FROM user WHERE user_id = ? AND guild_id = ?", (user_id,guild_id,)) as cursor:
            row = await cursor.fetchone()

        return row if row else 0

    async def get_user_cur_stats(self, user_id: int, guild_id: int):
        db = await get_database()

        async with db.execute("SELECT currency FROM user WHERE user_id = ? AND guild_id = ?", (user_id,guild_id,)) as cursor:
            row = await cursor.fetchone()

        return row if row else 0

    @commands.command("stats")
    async def get_user_stats(self, ctx):
        embed = discord.Embed(
            title="Stats",
            color=discord.Color.blue()
        )

        embed.add_field(name="User", value=f"{ctx.author.name}", inline=False)
        embed.add_field(name="Current EXP", value=f"{await self.get_user_exp_stats(ctx.author.id)}", inline=False)
        embed.add_field(name="Currency", value=f"{await self.get_user_cur_stats(ctx.author.id)}", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Stats(bot))

