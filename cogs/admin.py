import discord
from discord.ext import commands

class Admin(commands.Cog, name="Admin Only Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="admin", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def admin_group(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @admin_group.command(name="show_members")
    async def show_members(self, ctx):
        embed = discord.Embed(title="Server Members", description=None, color=discord.Color.green())

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
                embed.add_field(name=i, value=chunk, inline=False)

        else:
            embed.add_field(name="Server Members", value=members_text, inline=False)

        await ctx.send(embed=embed)

    @admin_group.command(name="purge")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        if amount <= 0:
            await ctx.send(f"Enter a positive value to delete message, {ctx.author.mention}")
            return

        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"{amount} messages purged.", delete_after=3.0) 

    @admin_group.command(name="kick")
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
            await ctx.send("BE GONE YOU FE- oh i cant do that -_-")
        except Exception as e:
            await ctx.send(f"Error: {e} -_-")

    @admin_group.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban_member(self, ctx, member: discord.Member, reason=None):
        embed = discord.Embed(description=f"{ctx.author}: banned {member} \n Reason: {reason}")

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
