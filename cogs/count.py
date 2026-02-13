import discord
import ast
import operator
from discord.ext import commands
from db.connection import get_database

class Count(commands.Cog):
    def __init__(self, bot):
        self.allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Mod: operator.mod,
            ast.FloorDiv: operator.floordiv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
        }

        self.bot = bot

    def safe_eval(self, expr):
        def eval_node(node):
            if isinstance(node, ast.Constant):
                return node.value
            if isinstance(node, ast.BinOp):
                left = eval_node(node.left)
                right = eval_node(node.right)
                opt_type = type(node.op)

                if opt_type in self.allowed_operators:
                    return self.allowed_operators[opt_type](left, right)
            if isinstance(node, ast.UnaryOp):
                operand = eval_node(node.operand)
                opt_type = type(node.op)
                if opt_type in self.allowed_operators:
                    return self.allowed_operators[opt_type](operand)
            
            raise ValueError("Invalid expression")

        paresed = ast.parse(expr, mode='eval')
        return eval_node(paresed.body)



    async def ensure_guild_entry(self, guild_id: int):
        db = await get_database() 
        await db.execute(
            """
            INSERT OR IGNORE INTO count_state 
            (guild_id,current_count, best_count, last_user_id)
            VALUES (?, 0, 0, NULL)
            """,
            (guild_id,),
        )

        await db.commit()

    async def get_count_channel(self, guild_id: int):
        db = await get_database()
        async with db.execute(
            "SELECT counting_channel FROM server WHERE guild_id = ?", (guild_id,)
        ) as cursor:
            row = await cursor.fetchone()
            
        return row[0] if row and row[0] else None

    async def get_current_count(self, guild_id: int):
        await self.ensure_guild_entry(guild_id)
        
        db = await get_database()
        async with db.execute(
            "SELECT current_count, last_user_id, best_count FROM count_state WHERE guild_id = ?", (guild_id,)
        ) as cursor:
            row = await cursor.fetchone()

        return row if row else (0, None, 0)

    async def update_count(self, guild_id: int, current: int, last_user: int | None, best: int):
        db = await get_database()
        await db.execute(
            """
            UPDATE count_state
            SET current_count = ?, last_user_id = ?, best_count = ?
            WHERE guild_id = ?
            """,
            (current, last_user, best, guild_id),
            )
        await db.commit()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        counting_channel = await self.get_count_channel(message.guild.id)
        if not counting_channel or message.channel.id != counting_channel:
            return

        try:
            result = self.safe_eval(message.content.strip())

            if not isinstance(result, int):
                return

            if result != int(result):
                return

            number = int(result)
        except Exception as e:
            return

        current, last_id, best = await self.get_current_count(message.guild.id)

        if message.author.id == last_id:
            await message.add_reaction("❌")
            await message.channel.send(
                f"{message.author.mention}, you can't count twice in a row! Reset to 0."
            )
            await self.update_count(message.guild.id, 0, None, best)
            return

        if number == current + 1: 
            new_best = max(best, number)
            await self.update_count(message.guild.id, number, message.author.id, new_best)
            await message.add_reaction("✅")
        else:
            await message.add_reaction("❌")
            await message.channel.send(
                    f"{message.author.mention} broke the count at **{current + 1}**. Reset to 1."
            )

            await self.update_count(message.guild.id, 0, None, best)



async def setup(bot):
    await bot.add_cog(Count(bot))
