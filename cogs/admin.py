import discord
from discord.ext import commands
import aiohttp
import asyncio

class Admin(commands.Cog):

    adminList = [541395285826338838, 462774660413653004, 766633452857851924, 545441234399789058]
    attributeList = ["health", "mana", "attack", "defense", "gold", "weaponlevel", "armorlevel"]
    classList = ["SWORDSMAN", "ARCHER", "MAGE"]

    def __init__(self, bot, api_url):
        self.bot = bot
        self.api_url = api_url

    async def sendRequest(self, ctx, type, id, value, heroClass, session):
        async with session.post(self.api_url+"/admin/"+type, json={'id':id, 'value':value, 'heroClassType':heroClass}) as resp:
            status = resp.status
            if (status == 200):
                await ctx.send("Success!")
            elif (status == 400):
                await ctx.send("user didn't exist in database")
            else:
                await ctx.send("Something when wrong :(")

    @commands.Cog.listener()
    async def on_ready(self):
        print('Admin is OK!')

    @commands.command(name = 'set')
    async def setValue(self, ctx, attribute, member: discord.Member, value: int):
        if (not (ctx.author.id in self.adminList)):
            await ctx.send("You are not an admin")
            return
        if (not (attribute.lower() in self.attributeList)):
            await ctx.send("Not a valid attribute")
            return
        if (value < 0):
            await ctx.send("Not a valid number")
            return
        id = member.id
        async with aiohttp.ClientSession() as session:
            await self.sendRequest(ctx, attribute.lower(), id, value, "ARCHER", session)

    @commands.command(name = 'setclass')
    async def setClass(self, ctx, member: discord.Member, value):
        if (not (ctx.author.id in self.adminList)):
            await ctx.send("You are not an admin")
            return
        if (not (value.upper() in self.classList)):
            await ctx.send("Not a valid class")
            return
        id = member.id
        async with aiohttp.ClientSession() as session:
            await self.sendRequest(ctx, "heroclasstype", id, 0, value.upper(), session)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            await ctx.send("command usage `rpg set <attribute> <user> <value>`")

                