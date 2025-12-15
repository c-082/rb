from discord.ext import commands
from discord import app_commands

class Admin_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ShowMembers", description="Shows every member in the server")
    @commands.has_role(1416016772284416000, 1412776444379267082)
    async def show_members(self, interaction: discord.Interaction):
        embed = discord.Embed(
                title="Members",
                description=None,
                color=discord.Color.green()
                )

        for mem in ctx.guild.members:
            embed.add_field(
                    name=mem,
                    inline=False
                    )
        await interaction.response.send(embed)

async def setup(bot):
    await bot.add_cog(Admin_Commands(bot))
