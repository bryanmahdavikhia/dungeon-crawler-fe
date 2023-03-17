import discord
from discord.ext import commands

class Help(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Help is OK!')
    
    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(title = "Help", description = "Use rpg help <command> for extended information on a command.", colour=discord.Colour(0x00FFFF))
        
        embed.add_field(name="Town Command", value="stats | leaderboard")
        embed.add_field(name="Shop Command", value="shop | buy")
        embed.add_field(name="Room Command", value="room")
        embed.add_field(name="Dungeon Command", 
                        value="""
                        dungeon
                        \n
                        stats -> see your progress and hero stats
                        leaderboard -> see dungeon leaderboard
                        shop -> see item list at the shop
                        buy -> buy item at the shop
                        room -> to upgrade your stats
                        dungeon -> start a dungeon
                        """)
        embed.set_footer(text="Dungeon Crawler")
        await ctx.send(embed=embed)
    
    @help.command()
    async def stats(self, ctx):
        embed = discord.Embed(title="Stats", 
                              description="to see your hero stats (health,mana,attack,defense) and progress (level,exp,dungeon level,gold)", colour=discord.Colour(0x00FFFF))
        embed.add_field(name="**Syntax**", value="rpg stats")
        embed.set_footer(text="Dungeon Crawler")
        
        await ctx.send(embed=embed)
    
    @help.command()
    async def leaderboard(self, ctx):
        embed = discord.Embed(title="Leaderboard",
                              description="to see the leaderboard of dungeon crawler player based on dungeon level", colour=discord.Colour(0x00FFFF))
        embed.add_field(name="**Syntax**", value="rpg leaderboard")
        embed.set_footer(text="Dungeon Crawler")
        await ctx.send(embed=embed)
    
    @help.command()
    async def shop(self, ctx):
        embed = discord.Embed(title="Shop",
                              description="to see the item that you can buy in the shop, you can buy item for dungeon or you can upgrade your equipment here", colour=discord.Colour(0x00FFFF))
        embed.add_field(name="**Syntax**", value="rpg shop")
        embed.set_footer(text="Dungeon Crawler")
        await ctx.send(embed=embed)
    
    @help.command()
    async def buy(self, ctx):
        embed = discord.Embed(title="Buy",
                              description="to buy the item that you want to buy at the shop", colour=discord.Colour(0x00FFFF))
        embed.add_field(name="**Syntax**", value="rpg buy [item id]")
        embed.set_footer(text="Dungeon Crawler")
        await ctx.send(embed=embed)
    
    @help.command()
    async def room(self, ctx):
        embed = discord.Embed(title="Room",
                              description="if you want to upgrade your attack, defense or mana capacity you can go to your room", colour=discord.Colour(0x00FFFF))
        embed.add_field(name="**Syntax**", value="rpg room")
        embed.set_footer(text="Dungeon Crawler")
        await ctx.send(embed=embed)
    
    @help.command()
    async def dungeon(self, ctx):
        embed = discord.Embed(title="Dungeon",
                              description="you can say this is the 'main game' in Dungeon Crawler, in dungeon you will fight 10 monster until the final boss and you will get rewards if you can beat them", colour=discord.Colour(0x00FFFF))
        embed.add_field(name="**Syntax**", value="rpg dungeon")
        embed.set_footer(text="Dungeon Crawler")
        await ctx.send(embed=embed)