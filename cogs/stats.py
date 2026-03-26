from math import sqrt, floor
import discord
import aiosqlite
from db.connection import get_database
from discord.ext import commands

class Stats(commands.Cog, name="User Stats"):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def get_user_exp_stats(self, user_id: int, guild_id: int):
        db = await get_database()

        async with db.execute("SELECT exp FROM user WHERE user_id = ? AND guild_id = ?", (user_id,guild_id,)) as cursor:
            row = await cursor.fetchone()

        return row[0] if row else 0

    async def get_user_cur_stats(self, user_id: int, guild_id: int):
        db = await get_database()

        async with db.execute("SELECT currency FROM user WHERE user_id = ? AND guild_id = ?", (user_id,guild_id,)) as cursor:
            row = await cursor.fetchone()

        return row[0] if row else 0

    def get_level(self, exp):
        return floor(sqrt(exp//50))

    @commands.command("stats")
    async def get_user_stats(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        user_icon = ctx.author.avatar.url if ctx.author.avatar else None
        embed = discord.Embed(
            title="Stats",
            color=discord.Color.blue()
        )

        embed.set_footer(text=f"Used by {ctx.author}", icon_url=user_icon)

        embed.add_field(name="User", value=f"{member.name}", inline=False)
        embed.add_field(name="Current EXP", value=f"{await self.get_user_exp_stats(member.id, ctx.guild.id)}", inline=False)
        embed.add_field(name="Current Level", value=f"{self.get_level(await self.get_user_exp_stats(member.id, ctx.guild.id))}", inline=False)
        embed.add_field(name="Currency", value=f"{await self.get_user_cur_stats(member.id, ctx.guild.id)}", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Stats(bot))

