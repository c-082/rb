import discord
from discord.ext import commands
from db.connection import get_database
import random

class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        
        if result == 1:
            await ctx.channel.send("Heads. You win")
            winnings = random.randint(bet_amount, bet_amount * 2)
            success = await self.update_user_cur(ctx.author.id, winnings, ctx.guild.id)
            if success:
                await ctx.channel.send(f"You won {winnings} currency")
        else:
            await ctx.channel.send("Tails. You lose!")
            success = await self.update_user_cur(ctx.author.id, -bet_amount, ctx.guild.id)
            if success:
                await ctx.channel.send(f"You lost {bet_amount} currency")

async def setup(bot):
    await bot.add_cog(Currency(bot))
