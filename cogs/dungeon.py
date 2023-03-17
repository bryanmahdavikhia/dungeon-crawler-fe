import discord
from discord.ext import commands
import aiohttp
import asyncio
from tools.dungeonEmbedCreator import DungeonEmbedCreator

class Dungeon(commands.Cog):

    def __init__(self, bot, api_url):
        self.bot = bot
        self.api_url = api_url

    async def isInDungeon(self, id):
        ret = False
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url+'/dungeon/check', json={'id':id}) as resp:
                if (resp.status == 200):
                    ret = True
        return ret

    async def sendRequest(self, type, id, itemIndex, session):
        content = None
        async with session.post(self.api_url+'/dungeon/'+type, json={'id':id, 'itemIndex':itemIndex}) as resp:
            if (resp.status == 200):
                content = await resp.json()
        return content

    @commands.Cog.listener()
    async def on_ready(self):
        print('Dungeon is OK!')

    @commands.command(name = 'dungeon')
    async def dungeonStart(self, ctx):
        id = ctx.author.id
        if (await self.isInDungeon(id)):
            await ctx.send("You are in a dungeon right now")
            return
        state = ''
        embedCreator = DungeonEmbedCreator()
        content = None

        def normalCheck(m):
            isValid = m.author==ctx.author and m.channel == ctx.channel
            resp = m.content.lower()
            isCommand = resp == 'attack' or resp == 'skill' or resp == 'item'
            return isValid and isCommand

        def winCheck(m):
            isValid = m.author==ctx.author and m.channel == ctx.channel
            resp = m.content.lower()
            isCommand = resp == 'continue' or resp == 'leave'
            return isValid and isCommand

        def itemCheck(m):
            isValid = m.author==ctx.author and m.channel == ctx.channel
            isCommand = m.content.isdigit()
            return isValid and isCommand

        async with aiohttp.ClientSession() as session:
            # Start Dungeon
            content = await self.sendRequest('start', id, 0, session)
            if (content != None):
                embed = embedCreator.normalEmbed(content, ctx)
                state = content['dungeonState']
                await ctx.send(embed=embed)
            else:
                state = 'LEAVE'
                await ctx.send("Dungeon handler can't be reached right now")
            
            while (state != 'LEAVE' and state != 'DEATH' and state != 'FINISH'):
                check = None
                if state == 'NORMAL':
                    check = normalCheck
                elif state == 'WIN':
                    check = winCheck
                else:
                    check = itemCheck
                    if (len(content['logs']) == 0):
                        await ctx.send("You don't have any item")
                        state = 'NORMAL'
                        continue

                try:
                    msg = await self.bot.wait_for('message', check=check, timeout=600.0)
                except asyncio.TimeoutError:
                    content = await self.sendRequest('timeout', id, 0, session)
                    if (content != None):
                        embed = embedCreator.deathEmbed(content, ctx)
                        state = content['dungeonState']
                        await ctx.send(embed=embed)
                    else:
                        state = 'LEAVE'
                        await ctx.send("Dungeon handler can't be reached right now")
                else:
                    lowerCaseMsg = msg.content.lower()
                    if (not lowerCaseMsg.isdigit()):
                        content = await self.sendRequest(lowerCaseMsg, id, 0, session)
                        if (content != None):
                            state = content['dungeonState']
                            embed = embedCreator.createEmbed(state, content, ctx)
                            await ctx.send(embed=embed)
                        else:
                            state = 'LEAVE'
                            await ctx.send("Dungeon handler can't be reached right now")
                    else:
                        numberMsg = int(lowerCaseMsg)
                        if (numberMsg>0 and numberMsg<=len(content['logs'])):
                            content = await self.sendRequest('useitem', id, numberMsg, session)
                            if (content != None):
                                state = content['dungeonState']
                                embed = embedCreator.createEmbed(state, content, ctx)
                                await ctx.send(embed=embed)
                            else:
                                state = 'LEAVE'
                                await ctx.send("Dungeon handler can't be reached right now")
                        else:
                            await ctx.send("That's not a valid number, try again")
