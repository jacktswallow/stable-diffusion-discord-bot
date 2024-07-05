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

#constructs message and truncates prompt strings if they are longer than the Discord bot maximum message length
def construct_message(prompt, negative_prompt, guidance_scale, error_message):
    MAX_CHARS = 1967
    neg_heading = '\n**Negative prompt:** '
    prompt_chars = len(prompt)
    neg_prompt_chars = len(negative_prompt)
    curr_chars = prompt_chars + neg_prompt_chars + len(error_message) + len(str(guidance_scale))
    #if message longer than discord max, truncate prompt strings
    if curr_chars > MAX_CHARS:
        overflow = '...'
        prompt_diff = abs(prompt_chars - neg_prompt_chars)
        excess_chars = curr_chars - MAX_CHARS
        if neg_prompt_chars > 0:
            excess_chars += len(neg_heading)
        #if the excess chars are less than difference between prompt string chars, remove excess chars from the longer prompt string
        if excess_chars <= prompt_diff:
            excess_chars += len(overflow)
            if neg_prompt_chars > prompt_chars:
                negative_prompt = negative_prompt[:-excess_chars] + overflow
            else:
                prompt = prompt[:-excess_chars] + overflow
        #else, truncate the longer string to the length of the shorter string, and then remove half the remaining excess from each string
        else:
            if prompt_chars > neg_prompt_chars:
                prompt = prompt[:-prompt_diff]
            elif neg_prompt_chars > prompt_chars:
                negative_prompt = negative_prompt[:-prompt_diff]
            excess_chars -= prompt_diff
            truncate_by = excess_chars // 2 + (excess_chars % 2 > 0) + len(overflow)
            prompt = prompt[:-truncate_by] + overflow
            negative_prompt = negative_prompt[:-truncate_by] + overflow

    #construct message string
    message = f'**Prompt:** {prompt}'
    if neg_prompt_chars > 0:
        message += neg_heading + negative_prompt
    message += f'\n**Guidance scale:** {guidance_scale}'
    message += error_message
    print(len(message))
    return message

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
    MAX_GUIDANCE_SCALE = 50
    await interaction.response.defer()

    if not 0 <= guidance_scale <= MAX_GUIDANCE_SCALE:
        error_message = f'\n**Error:** Guidance scale must be withinin range 0 - {MAX_GUIDANCE_SCALE}'
        message = construct_message(prompt, negative_prompt, guidance_scale, error_message)
        await interaction.followup.send(message)
        return
    
    response = await get_images(prompt, negative_prompt, str(guidance_scale)) 
    
    if isinstance(response, list) and len(response) > 0:
        files: list[discord.File] = []
        for image in response:
            data = io.BytesIO(image)
            files.append(discord.File(data, 'sd.jpg'))
        message = construct_message(prompt, negative_prompt, guidance_scale, '')
        await interaction.followup.send(message, files=files)
    else:
        try:
            error_message = f'\n**Error:** {response['error']}'
            message = construct_message(prompt, negative_prompt, guidance_scale, error_message)
            await interaction.followup.send(message)
        except:
            error_message = '\n**Error:** Unknown error'
            message = construct_message(prompt, negative_prompt, guidance_scale, error_message)
            await interaction.followup.send(message)

#regular command (uses defined prefix)
#syncs all defined slash commands
@bot.command()
async def sync(ctx): 
    if ctx.author.id == OWNER_USERID:
        await bot.tree.sync()
        await ctx.send('command tree sync complete')
    else:
        await ctx.send('**Error:** you must be the owner to use this command')

bot.run(BOT_TOKEN)