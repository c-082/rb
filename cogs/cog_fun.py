from discord.ext import commands
from discord import app_commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def coinflip(self):
        return random.randint(1,2) 

    @commands.command(name="coinflip", aliases=["cf"])
    async def coinflip_message(self, ctx):
        if self.coinflip() == 1:
            await ctx.channel.send("1. Heads")
        else:
             await ctx.channel.send("2. Tails")


    @commands.command(name="UwU", aliases=["uwu"])
    async def UwU(self, ctx):
        await ctx.channel.send("OwO")

    @commands.command(name="FiddleM", aliases=["fiddlem, Fiddlem, fiddleM"])
    async def FiddleM(self,ctx):
        await ctx.channel.send(f"I'm not doing that.")

    @commands.command(name="FiddleS", aliases=["fiddles", "Fiddles", "fiddleS"])
    async def FiddleS(self,ctx):
        await ctx.channel.send(f"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

    @commands.command(name="FiddleW", aliases=["fiddlew", "Fiddlew", "fiddleW"])
    async def FiddleW(self,ctx, *msg):
        await ctx.channel.send(" ".join(msg))

async def setup(bot):
    await bot.add_cog(Fun(bot))

