import requests
import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "theoriginalralsei"
REPO_NAME = "ralsei-bot"


def get_commits(owner=REPO_OWNER, repo=REPO_NAME, count=10):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(url, headers=headers, params={"per_page": count})

    if response.status_code == 200:
        commits = response.json()
        return [
            {
                "sha": c["sha"],
                "author": c["commit"]["author"]["name"],
                "message": c["commit"]["message"].split("\n")[0],
                "date": c["commit"]["author"]["date"],
                "url": c["html_url"],
            }
            for c in commits
        ]
    return None


class Progression(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="commits", aliases=["latest", "recent"])
    async def commits(self, ctx):
        commits = get_commits()
        if not commits:
            embed = discord.Embed(
                title="Error",
                description="Could not fetch commits",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title=f"Latest {len(commits)} Commits",
            description=f"Recent commits for [ralsei-bot](https://github.com/theoriginalralsei/ralsei-bot)",
            color=discord.Color.green(),
        )

        for c in commits:
            embed.add_field(
                name=f"{c['sha'][:7]} - {c['author']}",
                value=f"[{c['message']}]({c['url']})",
                inline=False,
            )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Progression(bot))
