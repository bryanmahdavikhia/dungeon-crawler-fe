import aiohttp
import discord
from discord import Embed
from discord.ext import commands


class Shop(commands.Cog):

    def __init__(self, bot, api_url):
        self.bot = bot
        self.api_url = api_url

    @commands.Cog.listener()
    async def on_ready(self):
        print('Shop is OK!')

    def get_buy_args(self, arg):
        try:
            item_id = int(arg)
        except ValueError:
            raise ValueError('Please use number for Id')

        return item_id

    @commands.command(name='buy')
    async def buy_shop(self, ctx, arg):
        player_id = ctx.author.id
        try:
            item_id = self.get_buy_args(arg)
        except ValueError as error:
            await ctx.send(error)
            return

        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url+'/shop/buy', json={'accountId': player_id, 'itemId': item_id}) as resp:
                if resp.status == 200:
                    content = await resp.json()
                else:
                    await ctx.send("Something not right, try again later")
                    return

        await ctx.send(content["message"])

    @commands.command(name='shop')
    async def list_shop(self, ctx):
        player_id = ctx.author.id

        async with aiohttp.ClientSession() as session:
            async with session.get(self.api_url+'/shop/list', json={'accountId': player_id}) as resp:
                if resp.status == 200:
                    content = await resp.json()
                else:
                    await ctx.send("Something not right, try again later")
                    return

        embed = Embed(title="SHOP", colour=discord.Colour(0xe9802e), description='Item Shop List, use "rpg buy [item id]"')
        embed.set_footer(text="Dungeon Crawler Beta")

        id_list = content["listItemId"]
        name_list = content["listItemName"]
        price_list = content["listItemPrice"]

        embed.add_field(name="Id", value="\n".join(id_list))
        embed.add_field(name="Name", value="\n".join(name_list))
        embed.add_field(name="Price", value="\n".join(price_list))

        await ctx.send(embed=embed)





