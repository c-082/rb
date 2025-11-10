import random
import discord
from discord.ext import commands
from discord import app_commands

class Action(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="hug", description="Hugs someone :3")
    async def hug(self, interaction: discord.Interaction, member: discord.Member):
        messages = [
                "Awww!",
                "So Adorable!!!",
                "Nice...Marriage when-"
                ]

        links = [
                "https://media1.tenor.com/m/xzhJUwNq1jkAAAAC/norep-owen.gif",
                "https://media1.tenor.com/m/iDU4OvXi1dUAAAAC/ralsei-kris.gif",
                "https://media1.tenor.com/m/MUJNqPh0MhwAAAAC/pixel-art-hug.gif",
                "https://media.tenor.com/j2qBShhqdUYAAAAi/hugging-hug.gif" 
                ] 

        chosen_gif = random.choice(links)
        chosen_message = random.choice(messages)

        embed = discord.Embed(
               title=f"{interaction.user.mention} has hugged {member.mention}",
               description=chosen_message,
               color=discord.Color.green()
               )
        
        embed.set_image(url=chosen_gif)

        await interaction.response.send_message(embed=embed)
  
    @app_commands.command(name="kiss", description="Kisses someone :3")
    async def kiss(self, interaction: discord.Interaction, member: discord.Member):
        messages = [
                "Awww!",
                "So Adorable!!!",
                "Nice...Marriage when-"
                ]

        links = [
                "https://media1.tenor.com/m/qIngZUPdp0gAAAAC/kiss-gif-kiss-gif-couple.gif",
                "https://media1.tenor.com/m/-OT2lXTKZ4wAAAAC/kralsei-deltarune.gif",
                "https://media1.tenor.com/m/iNfNEvkkyT0AAAAC/deltarune-ralsei.gif"
                ] 

        chosen_gif = random.choice(links)
        chosen_message = random.choice(messages)

        embed = discord.Embed(
               title=f"{interaction.user.display_name} has kissed {member.display_name}",
               description=chosen_message,
               color=discord.Color.green()
               )
         
        embed.set_image(url=chosen_gif)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="headpat", description="Headpat somone :3")
    async def headpat(self, interaction: discord.Interaction, member: discord.Member):
        messages = [
                "Pat pat pat pat! ^_^",
                "It's like they're petting a dog! >_O",
                "Awwwwwww!!!!"
                ]


        links = [
               "https://media.tenor.com/m/Lx6pxlvj44gAAAAC/ralsei-deltarune.gif",
               "https://media.tenor.com/m/CnXZJo9ddGIAAAAC/ralsei-cute-ralsei.gif",
               "https://media.tenor.com/lHCzlH_ez84AAAAi/cute-love.gif",
               "https://media.tenor.com/xFEinJ1BTosAAAAi/cartoon-patting.gif"
               ] 

        chosen_gif = random.choice(links)
        chosen_message = random.choice(messages)

        embed = discord.Embed(
               title=f"{interaction.user.display_name} has headpatted {member.display_name}",
               description=chosen_message,
               color=discord.Color.green()
               )
        
        embed.set_image(url=chosen_gif)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Action(bot))
