from db.connection import get_database
import time
import math
import discord
from discord.ext import commands, tasks
from discord import app_commands, guild, user
import aiosqlite

save_interval_seconds = 60
flush_interval = 60

class LeaderboardView(discord.ui.View):
    def __init__(self, ctx: commands.Context, rows: list, bot, get_level):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.rows = rows
        self.bot = bot
        self.get_level = get_level
        self.per_page = 10
        self.page = 1
        self.total_pages = max(1, (len(rows) + self.per_page - 1) // self.per_page)
        self.update_buttons()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.ctx.author.id

    def update_buttons(self):
        self.children[0].disabled = self.page <= 1
        self.children[1].disabled = self.page >= self.total_pages

    def get_embed(self):
        start = (self.page - 1) * self.per_page
        end = start + self.per_page
        page_rows = self.rows[start:end]

        embed = discord.Embed(
            title=f"Leaderboard - Page {self.page}/{self.total_pages}",
            color=discord.Color.blue()
        )

        rank = start + 1
        for row in page_rows:
            user = self.bot.get_user(row[0])
            if user:
                level = self.get_level(row[1])
                embed.add_field(
                    name=f"#{rank} {user.name}",
                    value=f"Level: {level} | EXP: {row[1]}",
                    inline=False
                )
            rank += 1

        return embed

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.secondary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page > 1:
            self.page -= 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.secondary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page < self.total_pages:
            self.page += 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.get_embed(), view=self)

class EXP(commands.Cog):
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

        async with db.execute("SELECT user_id, exp FROM user WHERE guild_id = ? ORDER BY exp DESC", (guild_id,)) as cursor:
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
            await message.channel.send(f"{message.author.mention} has leveled up! {old_level} -> {new_level}")

    @commands.command(name="leaderboard")
    async def leaderboard(self, ctx: commands.Context):
        rows = await self.get_guild_leaderboard(ctx.guild.id)
        view = LeaderboardView(ctx, rows, self.bot, self.get_level)
        await ctx.send(embed=view.get_embed(), view=view)

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
    await bot.add_cog(EXP(bot))
