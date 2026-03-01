import discord
import asyncio
from discord.ext import commands
from db.connection import get_database
import random
import time

class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_daily_bonus(self, user_id: int, guild_id: int) -> int:
        try:
            db = await get_database()

            async with db.execute("SELECT last_time_collected FROM user WHERE user_id = ? AND guild_id = ?", (user_id, guild_id,)) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0
        except Exception as e:
            print(f"Error getting daily bonus: {e}")
            return 0

    async def get_user_cur(self, user_id: int, guild_id: int) -> int:
        try:
            db = await get_database()

            async with db.execute("SELECT currency FROM user WHERE user_id = ? AND guild_id = ?", (user_id, guild_id,)) as cursor:
                row = await cursor.fetchone()

            return row[0] if row and row[0] else 0
        except Exception as e:
            print(f"Error getting user currency: {e}")
            return 0

    async def update_user_cur(self, user_id: int, amount: int, guild_id: int):
        if amount < 0:
            current_balance = await self.get_user_cur(user_id, guild_id)
            if current_balance + amount < 0:
                return False
        
        try:
            db = await get_database()

            await db.execute("""
            UPDATE user
            SET currency = currency + ?
            WHERE user_id = ? AND guild_id = ?
            """, (amount, user_id, guild_id,))

            await db.commit()
            return True
        except Exception as e:
            print(f"Error updating user currency: {e}")
            return False

    def coinflip(self):
        return random.randint(1, 2)

    @commands.command(name="coinflip", aliases=["cf"])
    async def coinflip_command(self, ctx, bet_amount: int = 10):
        if bet_amount <= 0:
            await ctx.channel.send("Error: Bet amount must be positive")
            return
        
        current_balance = await self.get_user_cur(ctx.author.id, ctx.guild.id)
        if current_balance < bet_amount:
            await ctx.channel.send("You don't have enough.")
            return

        result = self.coinflip()
        heads_or_tails = ["heads", "tails"]
        
        if result == 1:
            winnings = random.randint(bet_amount, bet_amount * 2)
            success = await self.update_user_cur(ctx.author.id, winnings, ctx.guild.id)
            if success:
                message = await ctx.channel.send(f"It landed on {random.choice(heads_or_tails)} and...")
                await asyncio.sleep(1)
                await message.edit(content=f"It landed on heads and you won {winnings} currency")
        else:
            fail = await self.update_user_cur(ctx.author.id, -bet_amount, ctx.guild.id)
            if fail:
                message = await ctx.channel.send(f"It landed on {random.choice(heads_or_tails)} and...")
                await asyncio.sleep(1)
                await message.edit(content=f"It landed on {random.choice(heads_or_tails)} and you lost {bet_amount} currency")

    @commands.command(name="dice", aliases=["di"])
    async def dice_command(self, ctx, bet_amount: int = 10, guess: int = 1):
        if bet_amount <= 0:
            await ctx.channel.send("Error: Bet amount must be positive")
            return

        current_balance = await self.get_user_cur(ctx.author.id, ctx.guild.id)
        if current_balance < bet_amount:
            await ctx.send("You don't have enough to bet")

        if guess == random.randint(1, 6):
            winnings = random.randint(bet_amount, bet_amount * 6)
            success = await self.update_user_cur(ctx.author.id, winnings, ctx.guild.id)
            if success:
                message = await ctx.send(f"You guesssed {guess} and...") 
                await asyncio.sleep(1)
                await message.edit(content=f"You guesssed {guess} and won {winnings} currency")
        else:
            success = await self.update_user_cur(ctx.author.id, -bet_amount, ctx.guild.id)
            if success:
                message = await ctx.send(f"You guesssed {guess} and...") 

                await asyncio.sleep(1)

                await message.edit(content=f"You guesssed {guess} and lost {bet_amount} currency")

    @commands.command(name="daily")
    async def daily_command(self, ctx):
        user_id = ctx.author.id
        guild_id = ctx.guild.id
        current_time = int(time.time())
        last_collected = await self.get_daily_bonus(user_id, guild_id)
        
        if current_time - last_collected < 86400:
            await ctx.send("You can only claim daily once per day!")
            return
        
        daily_amount = random.randint(10, 90)
        success = await self.update_user_cur(user_id, daily_amount, guild_id)
        
        if success:
            db = await get_database()
            await db.execute("""
            UPDATE user
            SET last_time_collected = ?
            WHERE user_id = ? AND guild_id = ?
            """, (current_time, user_id, guild_id,))
            await db.commit()
            await ctx.send(f"You claimed your daily reward of {daily_amount} currency!")
        else:
            await ctx.send("Failed to claim daily reward.")


async def setup(bot):
    await bot.add_cog(Currency(bot))
