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

#decodes base64 images and returns them as a list
def decode_images(output):
    images = []
    for image in output['data'][0]:
        images.append(base64.b64decode(image[23:-1]))
    return images

#create websocket connection, send prompt, recieve generated images
async def get_images(prompt, negative_prompt, guidance_scale):
    prompt = prompt.replace('"', '\\"')
    uri = 'wss://stabilityai-stable-diffusion.hf.space/queue/join'
    session_hash = str(uuid.uuid4())
    session_message = f'{{"session_hash":"{session_hash}","fn_index":3}}'
    prompt_message = f'{{"fn_index":3,"data":["{prompt}","{negative_prompt}",{guidance_scale}], "session_hash": "{session_hash}"}}'

    async with websockets.connect(uri, max_size = 3000000) as websocket:
        try:
            await websocket.recv()
            await websocket.send(session_message)

            await websocket.recv()
            await websocket.recv()
            await websocket.send(prompt_message)

            await websocket.recv()
            output = json.loads(await websocket.recv())['output']
        except:
            output = {'error': 'Websocket connection error, please try again'}
            return output
        
        try:
            return decode_images(output)
        except:
            return output

#message test channel on launch
@bot.event
async def on_ready():
    channel = bot.get_channel(TEST_CHANNEL_ID)
    await channel.send('running...')

#slash command for image generation from user prompt
@bot.tree.command(name='generate')
async def generate(interaction: discord.Interaction, prompt: str, negative_prompt:str = '', guidance_scale:int = 9):
    await interaction.response.defer()

    message = f'Prompt: {prompt}'
    if len(negative_prompt) > 0:
        message += f'\nNegative prompt: {negative_prompt}'
    message += f'\nGuidance scale: {guidance_scale}'

    if not 0 <= guidance_scale <= 50:
        error_message = message + f'\nError: Guidance scale must be withinin range 0 - 50'
        await interaction.followup.send(error_message)
        return
    
    response = await get_images(prompt, negative_prompt, str(guidance_scale)) 
    
    if isinstance(response, list) and len(response) > 0:
        files: list[discord.File] = []
        for image in response:
            data = io.BytesIO(image)
            files.append(discord.File(data, 'sd.jpg'))
        await interaction.followup.send(message, files=files)
    else:
        try:
            error_message = message + f'\nError: {response['error']}'
            await interaction.followup.send(error_message)
        except:
            error_message = message + '\nError: Unknown error'
            await interaction.followup.send(error_message)

#regular command (uses defined prefix)
#syncs all defined slash commands
@bot.command()
async def sync(ctx): 
    if ctx.author.id == OWNER_USERID:
        await bot.tree.sync()
        await ctx.send('command tree sync complete')
    else:
        await ctx.send('Error: you must be the owner to use this command')

bot.run(BOT_TOKEN)