import discord
from discord import app_commands
from discord.ext import commands
import random


arr_truth = [
    "When was ya' first kiss?",
    "What's the most Femboy thing you've ever done?",
    "If you had a first date (if so then why are you here-), what was it like?",
    "Weirdest moment?",
    "How much of a nerd are you on a scale of 1-10?",
    "Have you ever had a crush on someone here?",
]

arr_dare = [
    "DM someone here a kiss and say nothing",
    "Show off your thighs to one person",
    "Show off your thighs to EVERYONE",
    "Share a recent shower thought you had",
    "Recreate this bot, now."
]


class TODView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Truth", style=discord.ButtonStyle.green)
    async def truth_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        question = random.choice(arr_truth)
        embed = discord.Embed(
            title="Truth", description=f"**{question}**", color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, view=self)

    @discord.ui.button(label="Dare", style=discord.ButtonStyle.red)
    async def dare_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        dare = random.choice(arr_dare)
        embed = discord.Embed(
            title="Dare", description=f"**{dare}**", color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, view=self)

    @discord.ui.button(label="Random", style=discord.ButtonStyle.secondary)
    async def random_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        random_tod = random.choice([random.choice(arr_truth), random.choice(arr_dare)])
        embed = discord.Embed(
            title="Random", description=f"**{random_tod}**", color=0xFFFFFE
        )

        await interaction.response.send_message(embed=embed, view=self)


class TOD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="tod", description="Play some TOD with Ralsei bot!")
    async def tod(self, interaction: discord.Interaction):
        view = TODView()
        embed = discord.Embed(
            title="Truth Or Dare",
            description="-# why did i make this",
            color=discord.Color.blue(),
        )
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(TOD(bot))
