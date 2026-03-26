import discord
from discord.ext import commands
from db.connection import get_database

class Inventory(commands.Cog, name="Shop/Inventory"):
    def __init__(self, bot):
        self.bot = bot

    async def get_user_inventory(self, user_id, guild_id):
        db = await get_database()
        async with db.execute("SELECT item_id, item_name, quantity FROM user_inventory WHERE user_id = ? AND guild_id = ?", (user_id, guild_id,)) as cursor:
            rows = await cursor.fetchall()

        return rows if rows else None

    async def add_item(self, user_id, guild_id, item_id, item_name, quantity):
        db = await get_database()
        await db.execute("""
            INSERT INTO user_inventory (user_id, guild_id, item_id, item_name, quantity)
            VALUES (?,?,?,?,?)
            ON CONFLICT(user_id, guild_id, item_id)
            DO UPDATE SET quantity = quantity + ?
            """, (user_id, guild_id, item_id, item_name, quantity, quantity,))

        await db.commit()

    async def remove_item(self, user_id, guild_id, item_id, quantity):
        db = await get_database()
        async with db.execute("SELECT quantity FROM user_inventory WHERE user_id = ? AND guild_id = ? AND item_id = ?", (user_id, guild_id, item_id,)) as cursor:
            row = await cursor.fetchone()

        if not row or row[0] < quantity:
            return False

        if row[0] == quantity:
            await db.execute("DELETE FROM user_inventory WHERE user_id = ? AND guild_id = ? AND item_id = ?", (user_id, guild_id, item_id,))
            await db.commit()
        else:
            await db.execute("UPDATE user_inventory SET quantity = quantity - ? WHERE user_id = ? AND guild_id = ? AND item_id = ?", (quantity, user_id, guild_id, item_id,))
            await db.commit()

        return True

    async def get_shop_items(self, guild_id):
        db = await get_database()
        async with db.execute("SELECT item_id, item_name, price FROM shop WHERE guild_id = ?", (guild_id,)) as cursor:
            rows = await cursor.fetchall()
        return rows if rows else None

    async def add_shop_item(self, guild_id, item_id, item_name, price):
        db = await get_database()
        await db.execute("""
            INSERT INTO shop (guild_id, item_id, item_name, price)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(guild_id, item_id)
            DO UPDATE SET price = ?, item_name = ?
        """, (guild_id, item_id, item_name, price, price, item_name))
        await db.commit()

    async def remove_shop_item(self, guild_id, item_id, item_name):
        db = await get_database()

        async with db.execute("SELECT item_name, item_id FROM user_inventory WHERE guild_id = ? AND item_id = ? AND item_name = ?", (guild_id, item_id, item_name)) as cursor:
            row = await cursor.fetchone()

        if not row or not row[0]:
            return False

        if row[0]:
            await db.execute("DELETE FROM user_inventory WHERE guild_id = ? AND item_id = ? AND item_name = ?", (guild_id, item_id, item_name,))
            await db.commit()

        return True

    @commands.hybrid_command(name="inventory", aliases=["inv"], description="See all of your Items ")
    async def view_inventory(self, ctx, member: discord.Member | None = None):
        member = member or ctx.author
        guild_id = ctx.guild.id
        user_id = member.id

        inventory = await self.get_user_inventory(user_id, guild_id)

        if not inventory:
            await ctx.send(f"{member.display_name} has no items in their inventory. -_-")
            return

        embed = discord.Embed(title=f"{member.display_name}'s Inventory", color=discord.Color.blurple())
        for item_id, item_name, quantity in inventory:
            embed.add_field(name=item_name, value=f"Qty: {quantity}", inline=True)

        await ctx.send(embed=embed)


    @commands.command(name="add-item", aliases=["add"])
    @commands.has_permissions(administrator=True)
    async def add_to_shop(self, ctx, item_name: str, price: int):
        guild_id = ctx.guild.id
        db = await get_database()
        async with db.execute("SELECT MAX(CAST(item_id AS INTEGER)) FROM shop WHERE guild_id = ?", (guild_id,)) as cursor:
            row = await cursor.fetchone()
            max_id = row[0] if row[0] is not None else -1
            item_id = str(max_id + 1)
        await self.add_shop_item(guild_id, item_id, item_name, price)
        await ctx.send(f"Added {item_name} to shop for {price} currency!")

    @commands.command(name="remove-item")
    @commands.has_permissions(administrator=True)
    async def remove_from_shop(self, ctx, item_name: str):
        guild_id = ctx.guild.id
        items = await self.get_shop_items(guild_id)

        for item_id, inv_name, price in items:
            if inv_name.lower() == item_name.lower():
                db = await get_database()
                await db.execute("DELETE FROM shop WHERE guild_id = ? AND item_id = ?", (guild_id, item_id,))
                await db.commit()
                await ctx.send(f"Removed {item_name} from the shop!")
                return

        await ctx.send(f"{item_name} is not in the shop.")

    @add_to_shop.error
    async def add_to_shop_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need administrator permissions bro -_-")

    @remove_from_shop.error
    async def remove_from_shop_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need administrator permissions bro -_-")

    @commands.hybrid_command(name="shop")
    async def shop(self, ctx):
        guild_id = ctx.guild.id
        items = await self.get_shop_items(guild_id)

        if not items:
            await ctx.send("There isn't any Items in the shop. -_-")
            return

        embed = discord.Embed(
            title="Shop",
            description="Buy items with `r:buy <item_name>` or `r:buy <item_name> <quantity>`\nAdd items with `r:add-item <name> <price>`\n Remove an item with `r:remove-item <name>`",
            color=discord.Color.gold()
        )
        
        item_lines = []
        for item_id, item_name, price in items:
            item_lines.append(f"`{item_id} {item_name}` - **{price}** currency")
        
        embed.add_field(
            name="Available Items",
            value="\n".join(item_lines) if item_lines else "No items available",
            inline=False
        )
        
        embed.set_footer(text=f"Total items: {len(items)}")

        await ctx.send(embed=embed)

    @commands.command(name="buy")
    async def buy_item(self, ctx, item_name: str, quantity: int = 1):
        user_id = ctx.author.id
        guild_id = ctx.guild.id

        items = await self.get_shop_items(guild_id)
        
        for item_id, inv_name, price in items:
            if inv_name.lower() == item_name.lower():
                total_price = price * quantity

                currency_cog = self.bot.get_cog("Currency")
                if not currency_cog:
                    await ctx.send("Currency system not loaded!")
                    return

                current_balance = await currency_cog.get_user_cur(user_id, guild_id)
                if current_balance < total_price:
                    await ctx.send(f"You need {total_price} coins but only have {current_balance}!")
                    return

                success = await currency_cog.update_user_cur(user_id, -total_price, guild_id)
                if success:
                    await self.add_item(user_id, guild_id, item_id, inv_name, quantity)
                    await ctx.send(f"Bought {quantity} {inv_name} for {total_price} coins!")
                return

        await ctx.send(f"{item_name} is not sold in the shop.")

    @commands.command(name="sell")
    async def sell_item(self, ctx: commands.Context, item_name: str, quantity: int = 1):
        user_id = ctx.author.id
        guild_id = ctx.guild.id

        if quantity < 1:
            await ctx.send("Quantity must be at least 1!")
            return

        inventory = await self.get_user_inventory(user_id, guild_id)
        if not inventory:
            await ctx.send("You don't have any items to sell!")
            return

        for item_id, inv_name, item_qty in inventory:
            if inv_name.lower() == item_name.lower():
                if item_qty < quantity:
                    await ctx.send(f"You only have {item_qty} {inv_name}!")
                    return

                shop_items = await self.get_shop_items(guild_id)
                sell_price = 0
                for shop_item_id, shop_name, shop_price in shop_items:
                    if shop_name.lower() == inv_name.lower():
                        sell_price = shop_price // 2
                        break

                if sell_price == 0:
                    await ctx.send(f"{inv_name} doesn't have a sell price! (Not in shop)")
                    return

                total_price = sell_price * quantity

                success = await self.remove_item(user_id, guild_id, item_id, quantity)
                if success:
                    currency_cog = self.bot.get_cog("Currency")
                    if currency_cog:
                        await currency_cog.update_user_cur(user_id, total_price, guild_id)
                    await ctx.send(f"Sold {quantity} {inv_name} for {total_price} coins!")
                return

        await ctx.send(f"You don't have {item_name} in your inventory!")

async def setup(bot):
    await bot.add_cog(Inventory(bot))
