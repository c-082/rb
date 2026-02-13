from db.connection import get_database
import time
import math
import discord
from discord.ext import commands, tasks
from discord import app_commands, guild, user
import aiosqlite

save_interval_seconds = 60
flush_interval = 60

class UserEXP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.buffer: dict[tuple[int, int], int] = {}
        self.last_message_time: dict[tuple[int, int], float] = {}
        self.level_cache: dict[tuple[int, int], int] = {}

        self.flush_exp.start()

    async def get_user_exp(self, user_id: int, guild_id: int) -> int:
        db = await get_database()

        async with db.execute("SELECT exp FROM user WHERE user_id = ? AND guild_id = ?", (user_id, guild_id,)) as cursor:
            row = await cursor.fetchone()
        

        return row[0] if row else 0

    async def get_guild_leaderboard(self, guild_id: int):
        db = await get_database()

        async with db.execute("SELECT user_id, exp FROM user WHERE guild_id = ? ODER BY exp", (guild_id,)) as cursor:
            rows = await cursor.fetchall()

        return list(rows) if rows else []

    def cog_unload(self):
        self.flush_exp.cancel()

    def calculate_exp(self, message: discord.Message) -> int:
        base_exp = 20
        length_bonus = min(len(message.content) // 20, 5)
        attachment_bonus = len(message.attachments) * 5 if message.attachments else 0
        return base_exp + length_bonus + attachment_bonus


    def get_level(self, exp: int) -> int:
        return int(math.sqrt(exp // 50))

    def can_gain_exp(self, user_id: int, guild_id: int ,current_time: float) -> bool:
        now = time.monotonic()
        last = self.last_message_time.get((user_id, guild_id), 0)
        if now - last < save_interval_seconds:
            return False

        self.last_message_time[(user_id, guild_id)] = now
        return True

    def add_exp_to_buffer(self, user_id: int, exp: int, guild_id):
        key = (user_id, guild_id)
        self.buffer[key] = self.buffer.get(key, 0) + exp

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild or message.content.startswith(self.bot.command_prefix):
            return

        if not self.can_gain_exp(message.author.id, message.guild.id  ,time.monotonic()):
            return

        user_id = message.author.id
        guild_id = message.guild.id

        current_exp = await self.get_user_exp(user_id, guild_id)
        buffer_exp = self.buffer.get((user_id, guild_id), 0)
        total_exp_before = current_exp + buffer_exp

        old_level = self.get_level(total_exp_before)

        gained_exp = self.calculate_exp(message)
        self.add_exp_to_buffer(user_id, gained_exp, guild_id)

        total_exp_after = total_exp_before + gained_exp
        new_level = self.get_level(total_exp_after)

        if new_level > old_level:
            await message.channel.send(f"{message.author.mention} has leveled up! \n"
                                       f"Level: {old_level} -> {new_level}"
            )
            print(f"{message.author} has leveled up {old_level} -> {new_level}")


        print(f"{message.author} gained {gained_exp} EXP (Total: {total_exp_after})")

    @commands.command(name="leaderboard")
    async def leaderboard(self, ctx: commands.Context):
        rows = await self.get_guild_leaderboard(ctx.guild.id)
        embed = discord.Embed(title="Leaderboard", color=discord.Color.blue())

        for row in rows[:10]:
            user = self.bot.get_user(row[0])
            if user:
                level = self.get_level(row[1])
                embed.add_field(name=user.name, value=f"Level: {level} | EXP: {row[1]}", inline=False)

        await ctx.send(embed=embed)



    @tasks.loop(seconds=flush_interval)
    async def flush_exp(self):
        if not self.buffer:
            return

        db = await get_database()

        for (user_id, guild_id), exp in self.buffer.items():
            await db.execute(
                """
                    INSERT INTO user (user_id, guild_id ,exp)
                    VALUES (?,?, ?)
                    ON CONFLICT(user_id, guild_id) DO UPDATE SET exp = exp + excluded.exp
                    """,
                (user_id,guild_id,exp)
            )

        await db.commit()
        self.buffer.clear()

    @flush_exp.before_loop
    async def before_flush_exp(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(UserEXP(bot))
