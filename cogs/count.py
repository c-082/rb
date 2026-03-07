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

    async def process_count(self, guild_id: int, user_id: int, number: int):
        db = await get_database()
        
        await db.execute(
            """
            INSERT OR IGNORE INTO count_state 
            (guild_id,current_count, best_count, last_user_id)
            VALUES (?, 0, 0, NULL)
            """,
            (guild_id,),
        )
        
        async with db.execute(
            "SELECT current_count, last_user_id, best_count FROM count_state WHERE guild_id = ? FOR UPDATE",
            (guild_id,)
        ) as cursor:
            row = await cursor.fetchone()
        
        if not row:
            return None, None, None
            
        current, last_id, best = row[0], row[1], row[2]
        
        if user_id == last_id:
            await db.execute(
                "UPDATE count_state SET current_count = 0, last_user_id = NULL WHERE guild_id = ?",
                (guild_id,),
            )
            await db.commit()
            return "same_user", current, best
        
        if number == current + 1:
            new_best = max(best, number)
            await db.execute(
                "UPDATE count_state SET current_count = ?, last_user_id = ?, best_count = ? WHERE guild_id = ?",
                (number, user_id, new_best, guild_id),
            )
            await db.commit()
            return "success", number, new_best
        else:
            await db.execute(
                "UPDATE count_state SET current_count = 0, last_user_id = NULL WHERE guild_id = ?",
                (guild_id,),
            )
            await db.commit()
            return "broken", current + 1, best

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

        result_type, current, best = await self.process_count(message.guild.id, message.author.id, number)

        if result_type == "same_user":
            await message.add_reaction("❌")
            await message.channel.send(
                f"{message.author.mention}, you can't count twice in a row! Reset to 0."
            )
        elif result_type == "success":
            await message.add_reaction("✅")
        elif result_type == "broken":
            await message.add_reaction("❌")
            await message.channel.send(
                    f"{message.author.mention} broke the count at **{current}**. Reset to 1."
            )



async def setup(bot):
    await bot.add_cog(Count(bot))
