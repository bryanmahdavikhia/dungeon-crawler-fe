import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

from cogs.info import Info
from cogs.town import Town
from cogs.dungeon import Dungeon
from cogs.room import Room
from cogs.admin import Admin
from cogs.help import Help
from cogs.shop import Shop

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
API_URL = os.getenv('API_URL')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='rpg ', case_insensitive = True, intents = intents)

bot.remove_command('help')
bot.add_cog(Info(bot))
bot.add_cog(Town(bot, API_URL))
bot.add_cog(Dungeon(bot, API_URL))
bot.add_cog(Shop(bot, API_URL))
bot.add_cog(Room(bot, API_URL))
bot.add_cog(Admin(bot, API_URL))
bot.add_cog(Help(bot))

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

bot.run(TOKEN)