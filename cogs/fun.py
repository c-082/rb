import discord
from discord.ext import commands
import random
from discord import app_commands



class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="Scream", aliases=["scream", "s"])
    async def Scream(self, ctx):
        embed = discord.Embed(
            title=None,
            description="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
            color=discord.Color.green(),
        )

        await ctx.send(embed=embed)

    @commands.command(name="Speak", aliases=["speak", "sp"])
    async def Speak(self, ctx, *msg):
        embed = discord.Embed(
            title=None,
            description=f"**{ctx.author}: {' '.join(msg)}**",
            color=discord.Color.green(),
        )

        await ctx.send(embed=embed)

    @app_commands.command(name="8ball", description="Talk with Ralsei of True Wisdom and Knowledge")
    async def ball(self, interaction: discord.Interaction, message: str):
        embed = discord.Embed(
            title="8ball",
            description=f"Question: {message}",
            color=discord.Color.green(),
        )

        embed.add_field(
            name="\u200b",
            value="Ralsei of True Wisdom and Knowledge says...",
            inline=True,
        )

        responses = [
            "https://www.demirramon.com/gen/undertale_text_box.png?text=Of%20course!%20It%27s%20in%20the%20Prophecy%20after%20all!&box=deltarune&character=deltarune-ralsei&expression=excited-grin&size=2&t=1764838835",
            "https://www.demirramon.com/gen/undertale_text_box.png?text=Mehhhh...nah&box=deltarune&character=deltarune-ralsei&expression=uninterested&size=2&t=1764838934",
            "https://www.demirramon.com/gen/undertale_text_box.png?text=Hmmm....%0AOf%20course!&box=deltarune&character=deltarune-ralsei&expression=excited&size=2&t=1764839027",
            "https://www.demirramon.com/gen/undertale_text_box.png?text=Don%27t&box=deltarune&character=deltarune-ralsei&expression=shadow&size=2&t=1764839390",
            "https://www.demirramon.com/gen/undertale_text_box.png?text=It%27s%20in%20Prophecy%20little%20bro.&box=deltarune&character=deltarune-ralsei&expression=winking&size=2&t=1764839486",
            "https://www.demirramon.com/gen/undertale_text_box.png?text=UwU%0Acolor%3D%23808080%20(%20it%27s%20ralsei%27s%20way%20of%20saying%20yes%20)%20color%3Dwhite&box=deltarune&character=deltarune-ralsei&expression=excited-grin&size=2&t=1764839634",
            "https://www.demirramon.com/gen/undertale_text_box.png?text=You%20shouldn%27t.%20&box=deltarune&character=deltarune-ralsei&expression=shadow&size=1&t=1765851328"
            "https://www.demirramon.com/gen/undertale_text_box.png?text=I%20mean%20ig%20idrk%20&box=deltarune&character=deltarune-ralsei&expression=uninterested&size=1&t=1765851450"
            "https://www.demirramon.com/gen/undertale_text_box.png?text=WHAT%20KINDA%20QUESTION%20IS%20THAT%3F%3F%3F%3F%3F%3F%3F&box=deltarune&character=deltarune-ralsei&expression=screaming&size=1&t=1765851556"
            "https://www.demirramon.com/gen/undertale_text_box.png?text=Fuck%20you%20mean%2C%20mate%3F&box=deltarune&character=deltarune-ralsei&expression=surprised-looking-away&size=1&t=1765851501",
        ]

        embed.set_image(url=random.choice(responses))

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Fun(bot))
