import discord
from discord.ext import commands

class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Info is OK!')

    @commands.command(name = 'guide')
    async def guide(self, ctx):
        await ctx.send('Type `rpg start` to start playing')

    @commands.command(name = 'ping')
    async def ping(self, ctx):
        await ctx.send('pong!')