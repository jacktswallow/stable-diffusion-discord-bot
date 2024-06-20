from discord.ext import commands
import discord
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_USERID = int(os.getenv("OWNER_USERID"))
TEST_CHANNEL_ID = int(os.getenv("TEST_CHANNEL_ID"))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=False)

#message test channel on launch
@bot.event
async def on_ready():
    print('running...')
    channel = bot.get_channel(TEST_CHANNEL_ID)
    await channel.send('running...')

#regular command (uses defined prefix)
#syncs all defined slash commands
@bot.command()
async def sync(ctx):
    print('command tree synced...')
    if ctx.author.id == OWNER_USERID:
        await bot.tree.sync()
        await ctx.send('command tree synced...')
    else:
        await ctx.send('you must be the owner to use this command...')

bot.run(BOT_TOKEN)