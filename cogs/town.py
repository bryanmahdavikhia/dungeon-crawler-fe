import discord
from discord.ext import commands
import aiohttp
import asyncio

class Town(commands.Cog):

    def __init__(self, bot, api_url):
        self.bot = bot
        self.api_url = api_url

    @commands.Cog.listener()
    async def on_ready(self):
        print('Town is OK!')

    @commands.command(name = 'start')
    async def start(self, ctx):
        id = ctx.author.id
        await ctx.send("Choose your class: 1.swordsman 2.archer 3.mage (type number only!)")

        def check(m):
            return (m.author==ctx.author and m.channel == ctx.channel) and (m.content == '1' or m.content == '2' or m.content == '3')

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=10.0)
        except asyncio.TimeoutError:
            await ctx.send('too slow')
        else:
            heroClass = None
            if (msg.content == '1'):
                heroClass = 'SWORDSMAN'
            elif (msg.content == '2'):
                heroClass = 'ARCHER'
            else:
                heroClass = 'MAGE'
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url+'/account/create', json={'id': id, 'heroClassType': heroClass}) as resp:
                    if (resp.status == 200):
                        await ctx.send('Welcome to dungeon crawler, type *rpg stats* to check your stats')
                    elif (resp.status == 400):
                        await ctx.send('You already have an account')
                    else:
                        await ctx.send('Unknown error has occured')

    @commands.command(name = 'stats')
    async def stats(self, ctx):
        id = ctx.author.id
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url+'/account/', json={'id': id}) as resp:
                if (resp.status == 200):
                    content = await resp.json()
                    embed = discord.Embed(title="HERO STATS", colour=discord.Colour(0xe9802e), description=f"**Class: {content['heroClassType'].capitalize()}**")

                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                    embed.set_footer(text="Dungeon Crawler Beta")

                    embed.add_field(name="Progress", value=f"**Level:** {content['level']}\n**Exp:** {content['exp']}\n**Dungeon Level:** {content['dungeonLevel']}\n**Gold:** {content['gold']}")
                    embed.add_field(name="Stats", value=f"**Health:** {content['maxHealth']}\n**Mana:** {content['maxMana']}\n**Atk:** {content['attack']}\n**Def:** {content['defense']}")

                    await ctx.send(embed=embed)
                else:
                    await ctx.send('Type *rpg start* to register')
    
    @commands.command(name = 'leaderboard')
    async def leaderboard(self, ctx):
        id = ctx.author.id
        leaderboard = None
        client = discord.Client()
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url+'/town/leaderboard/', json={'leaderboard' : leaderboard}) as resp:
                if (resp.status == 200):
                    content = await resp.json()
                    embed = discord.Embed(title="LEADERBOARD", colour=discord.Colour(0x00FFFF))
                    isi = ""
                    count = 1
                    for i in content['leaderboard']:
                        user = ctx.message.guild.get_member(int(i['id']))
                        if(user == None):
                            user = i['id']
                        isi += f"{count}. {user} **Dungeon Level:** {i['dungeonLevel']}\n"
                        count+=1
                    embed.add_field(name="Dungeon Leaderboard", value=isi)
                    embed.set_footer(text="Dungeon Crawler")
                    print(isi)
                    await ctx.send(embed=embed)
                    
                elif(resp.status == 400):
                    await ctx.send('Type *rpg start* to register')
                    