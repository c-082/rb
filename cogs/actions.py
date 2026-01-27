import random
import discord
from discord.ext import commands
from discord import app_commands


class Action(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hug", description="Hugs someone :3")
    async def hug(self, interaction: discord.Interaction, member: discord.Member):
        if member.id == 1434674677682409573:
            messages = [
                "M...M-me?!",
                "Thanks...i needed it.",
                "Can...can we marry now?",
            ]
        else:
            messages = ["Awww!", "So Adorable!!!", "Nice...Marriage when-"]

        links = [
            "https://media1.tenor.com/images/xzhJUwNq1jkAAAAC/norep-owen.gif",
            "https://media1.tenor.com/images/iDU4OvXi1dUAAAAC/ralsei-kris.gif",
            "https://media1.tenor.com/images/MUJNqPh0MhwAAAAC/pixel-art-hug.gif",
            "https://media.tenor.com/j2qBShhqdUYAAAAi/hugging-hug.gif",
        ]

        chosen_gif = random.choice(links)
        chosen_message = random.choice(messages)

        embed = discord.Embed(
            title=f"{interaction.user.display_name} has hugged {member.display_name}!",
            description=chosen_message,
            color=discord.Color.green(),
        )

        embed.set_image(url=chosen_gif)
        embed.set_footer(
            text=f"Used by {interaction.user}"
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="kiss", description="Kisses someone :3")
    async def kiss(self, interaction: discord.Interaction, member: discord.Member):
        if member.id == 1434674677682409573:
            messages = [
                "M...M-me?!",
                "Thanks...i needed it.",
                "Can...can we marry now?",
                "Ummm...UwU!",
            ]
        else:
            messages = ["Awww!", "So Adorable!!!", "Nice...Marriage when-"]

        links = [
            "https://media1.tenor.com/images/qIngZUPdp0gAAAAC/kiss-gif-kiss-gif-couple.gif",
            "https://media1.tenor.com/images/iNfNEvkkyT0AAAAC/deltarune-ralsei.gif"
            "https://media.tenor.com/3dTj9cRPU50AAAAj/ralsei-kris.gif",
        ]

        chosen_gif = random.choice(links)
        chosen_message = random.choice(messages)

        embed = discord.Embed(
            title=f"{interaction.user.display_name} has kissed {member.display_name}",
            description=chosen_message,
            color=discord.Color.green(),
        )

        embed.set_image(url=chosen_gif)

        embed.set_footer(
            text=f"Used by {interaction.user}"
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="headpat", description="Headpat somone :3")
    async def headpat(self, interaction: discord.Interaction, member: discord.Member):
        if member.id == 1434674677682409573:
            messages = [
                "T-too many headpats!!!! >_<",
                "Im...Im not a dog, Human!",
                "UwU- AH I DIDN'T MEAN TO SAY THAT IM SO SORRY- I- UHH- I- I- uwu~",
            ]

        else:
            messages = [
                "Pat pat pat pat! ^_^",
                "It's like they're petting a dog! >_O",
                "Awwwwwww!!!!",
            ]

        links = [
            "https://media.tenor.com/images/Lx6pxlvj44gAAAAC/ralsei-deltarune.gif",
            "https://media.tenor.com/images/CnXZJo9ddGIAAAAC/ralsei-cute-ralsei.gif",
            "https://media.tenor.com/lHCzlH_ez84AAAAi/cute-love.gif",
            "https://media.tenor.com/xFEinJ1BTosAAAAi/cartoon-patting.gif",
        ]

        chosen_gif = random.choice(links)
        chosen_message = random.choice(messages)

        embed = discord.Embed(
            title=f"{interaction.user.display_name} has headpatted {member.display_name}",
            description=chosen_message,
            color=discord.Color.green(),
        )

        embed.set_image(url=chosen_gif)

        embed.set_footer(
            text=f"Used by {interaction.user}"
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="slap", description="Slap anyone wwho gets in ya way >:D"
    )
    async def slap(self, interaction: discord.Interaction, member: discord.Member):
        if member.id == 1434674677682409573:
            messages = ["O-ow! >_<", "That was painful!", "Stop!!!", "Oh yeah- i mean OW!"]
        else:
            messages = [
                "damn..that looked painful",
                "oof, goddamn",
                "Whoa..wouldn't wanna be that guy, am i right?",
            ]

        chosen_message = random.choice(messages)

        embed = discord.Embed(
            title=f"{interaction.user.display_name} has slapped {member.display_name}",
            description=chosen_message,
            color=discord.Color.green(),
        )
        embed.set_footer(
            text=f"Used by {interaction.user}"
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Action(bot))
