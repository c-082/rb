import discord
from discord.ext import commands
from discord import app_commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="show_members")
    @commands.has_any_role(
        1416016772284416000, 1412776444379267082, 1412776298346184764
    )
    async def show_members(self, ctx):
        embed = discord.Embed(
            title="Server Members", description=None, color=discord.Color.green()
        )

        members = [member for member in ctx.guild.members if not member.bot]
        members_list = [f"{member.mention} - {member.name}" for member in members]
        members_text = "\n".join(members_list)

        if not members:
            await ctx.send("No members in sight")
            return

        if len(members_text) > 1024:
            chunks = []
            current_chunk = []
            current_length = 0

            for member_text in members_list:
                if current_length + len(member_text) + 1 > 1024:
                    chunks.append("\n".join(current_chunk))
                    current_chunk = [member_text]
                    current_length = len(member_text)

                else:
                    current_chunk.append(member_text)
                    current_length += len(member_text) + 1

            if current_chunk:
                chunks.append("\n".join(current_chunk))

            for i, chunk in enumerate(chunks, 1):
                embed.add_field(name="", value=chunk, inline=False)

        else:
            embed.add_field(name="Server Members", value=members_text, inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick_member(self, ctx, member: discord.Member, reason=None):
        embed = discord.Embed(
            title=None, description=f"{ctx.author}: kicked {member} \n Reason: {reason}"
        )

        if member == ctx.author:
            await ctx.send(f"You can't do that to yourself, {member} -_-")
            return

        if member.guild_permissions.administrator:
            await ctx.send("Bro that's an admin -_-")
            return

        try:
            await member.kick(reason=reason)
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send(f"BE GONE YOU FE- oh i cant do that -_-")
        except Exception as e:
            await ctx.send(f"Error: {e} -_-")

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban_member(self, ctx, member: discord.Member, reason=None):
        embed = discord.Embed(
            title=None, description=f"{ctx.author}: kicked {member} \n Reason: {reason}"
        )

        if member == ctx.author:
            await ctx.send(f"You can't do that to yourself, {member} -_-")
            return

        if member.guild_permissions.administrator:
            await ctx.send("Bro that's an admin -_-")
            return

        try:
            await member.ban(reason=reason)
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send(f"BE GONE YOU FE- oh i cant do that -_-")
        except Exception as e:
            await ctx.send(f"Error: {e} -_-")


async def setup(bot):
    await bot.add_cog(Admin(bot))
