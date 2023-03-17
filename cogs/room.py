from msilib.schema import Upgrade
import discord
from discord.ext import commands
import aiohttp
import asyncio
from cogs.town import Town

class Room(commands.Cog):

    def __init__(self, bot, api_url):
        self.bot = bot
        self.api_url = api_url

    @commands.Cog.listener()
    async def on_ready(self):
        print('Room is OK!')

    async def sendRequest(self, type, id, session):
        content = None
        async with session.post(self.api_url+'/room/'+type, json={'id':id}) as resp:
            if (resp.status == 200):
                content = await resp.json()
        return content

    async def isInDungeon(self, id):
        ret = False
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url+'/dungeon/check', json={'id':id}) as resp:
                if (resp.status == 200):
                    ret = True
        return ret

    @commands.command(name = 'room')
    async def room(self, ctx):
        id = ctx.author.id
        town = Town(self.bot, self.api_url)

        if (await self.isInDungeon(id)):
            await ctx.send("You are in a dungeon right now")
            return
            
        async with aiohttp.ClientSession() as session:
            #Enter the room
            await town.stats(self, ctx)
            embed = discord.Embed(title="Dungeon Crawler", colour=discord.Colour(0x00FFFF))
            embed.set_author(name=f"{ctx.author.name}'s room", icon_url=ctx.author.avatar_url)
            embed.add_field(name="What you can do inside your Room", value=f"UPGRADE ATTACK | UPGRADE DEFENSE | UPGRADE MANA CAPACITY | LEAVE\n\nUpgrade will increase your selected stat by 15\nUpgrade cost : 100 gold\n")
            await ctx.send(embed=embed)

            while(True):
                #Upgrade Stats
                try:
                    msg = await self.bot.wait_for('message', timeout=600.0)
                except asyncio.TimeoutError:
                    await ctx.send("Leaving room")
                    await town.stats(self, ctx)
                    break
                else:
                    lowerCaseMsg = msg.content.lower()
                    if lowerCaseMsg.find("upgrade") == 0:
                        upgradeMsg = lowerCaseMsg[:7]
                        task = lowerCaseMsg[8:]
                        if task == "attack" or task == "defense" or task == "mana capacity":
                            if task == "mana capacity":
                                task = task[:4]
                            taskResp = await self.sendRequest(upgradeMsg+"-"+task, id, session)
                            if taskResp['added']:
                                embed = discord.Embed(title="Upgrading Stats", colour=discord.Colour(0xe9802e))

                                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                                embed.add_field(name="Stats upgraded!", value=f"{task} has been added by 15\n")
                                await ctx.send(embed=embed)
                            else:
                                embed = discord.Embed(title="Upgrading Stats", colour=discord.Colour(0xf62811))

                                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                                embed.add_field(name="Insufficient gold!", value=f"Your current gold is insufficient for upgrading {task}\n")
                                await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(title="Upgrading Stats", colour=discord.Colour(0xf62811))

                            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                            embed.add_field(name="Wrong command!", value=f"Try again between UPGRADE ATTACK | UPGRADE DEFENSE | UPGRADE MANA CAPACITY | LEAVE\n")
                            await ctx.send(embed=embed)
                    elif lowerCaseMsg == "leave":
                        await ctx.send("Leaving room")
                        await town.stats(self, ctx)
                        break
                    else:
                        embed = discord.Embed(title="Upgrading Stats", colour=discord.Colour(0xf62811))

                        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                        embed.add_field(name="Wrong command!", value=f"Try again between UPGRADE ATTACK | UPGRADE DEFENSE | UPGRADE MANA CAPACITY | LEAVE\n")
                        await ctx.send(embed=embed)