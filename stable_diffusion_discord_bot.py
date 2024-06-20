from discord.ext import commands
import discord
import os
from dotenv import load_dotenv
import io
import websockets
import uuid
import base64
import json

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_USERID = int(os.getenv("OWNER_USERID"))
TEST_CHANNEL_ID = int(os.getenv("TEST_CHANNEL_ID"))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=False)

#get websocket response
async def await_response(websocket):
    response = await websocket.recv()
    print(f'response: {response}')

def decode_images(output):
    images = []
    for image in output['data'][0]:
        images.append(base64.b64decode(image[23:-1]))

    return images

#create websocket connection, send prompt, recieve generated images
async def get_images(prompt, negative_prompt, guidance_scale):
    uri = 'wss://stabilityai-stable-diffusion.hf.space/queue/join'
    session_hash = str(uuid.uuid4())
    session_message = f'{{"session_hash":"{session_hash}","fn_index":3}}'
    prompt_message = f'{{"fn_index":3,"data":["{prompt}","{negative_prompt}",{guidance_scale}], "session_hash": "{session_hash}"}}'

    async with websockets.connect(uri) as websocket:
        print(f'connected to websocket at {uri}...')
        await await_response(websocket)
        await websocket.send(session_message)
        print(f'request: {session_message}')

        await await_response(websocket)
        await await_response(websocket)
        await websocket.send(prompt_message)
        print(f'request: {prompt_message}')

        await await_response(websocket)

        output = json.loads(await websocket.recv())['output']
        try:
            return decode_images(output)
        except:
            return output

#message test channel on launch
@bot.event
async def on_ready():
    print('running...')
    channel = bot.get_channel(TEST_CHANNEL_ID)
    await channel.send('running...')

#slash command for image generation from user prompt
@bot.tree.command(name='generate')
async def generate(interaction, prompt: str):
    await interaction.response.defer()
    print(f'prompt: {prompt}')
    negative_prompt = '' #will add functionality to utilise the negative prompt later
    guidance_scale = '9' #default value = 9, will add functionality for user input later
    response = await get_images(prompt, negative_prompt, guidance_scale)
    
    if isinstance(response, list):
        files: list[discord.File] = []
        for image in response:
            data = io.BytesIO(image)
            files.append(discord.File(data, 'sd.jpg'))
            message = f'Prompt: {prompt}'
        await interaction.followup.send(message, files=files)
    else:
        error_message = f'Prompt: {prompt}\nStable Diffusion error: {response['error']}'
        await interaction.followup.send(error_message)
        print(response['error'])

#regular command (uses defined prefix)
#syncs all defined slash commands
@bot.command()
async def sync(ctx): 
    if ctx.author.id == OWNER_USERID:
        await bot.tree.sync()
        await ctx.send('command tree sync complete')
        print('command tree sync complete')
    else:
        await ctx.send('Error: you must be the owner to use this command')

bot.run(BOT_TOKEN)