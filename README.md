<a id="readme-top"></a>
# Stable Diffusion Discord Intergration Bot
A Discord bot that integrates Stable Diffusion 2.1 image generation from text prompts into Discord.

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
* [Discord](https://discord.com/)
* [Python and pip](https://packaging.python.org/en/latest/tutorials/installing-packages/)
* pip packages
  * [discord.py](https://discordpy.readthedocs.io/en/stable/intro.html)
    ```sh
    pip install discord.py
    ```
  * [python-dotenv](https://pypi.org/project/python-dotenv/)
    ```sh
    pip install python-dotenv
    ```
  * [websockets](https://pypi.org/project/websockets/)
    ```sh
    pip install websockets
    ```

### Installation

1. Install all prerequisites listed above
2. Clone the repo
   ```sh
   git clone https://github.com/jacktswallow/stable-diffusion-discord-bot.git
   ```
3. Enable developer mode for your Discord account
    1. Open Discord and click on the cog icon (user settings)
    2. Click the 'Advanced' tab
    3. Toggle 'Developer Mode' to on
4. Create a Discord bot account and get its token
    1. Visit the [Discord applications page](https://discord.com/developers/applications)
    2. Ensure you are logged in to your Discord account
    3. Click 'New Application'
    4. Name the bot and click 'Create'
    5. Go to the 'Bot' tab and click 'Add Bot'
    6. Copy the token. Treat this like a password, do not share it with anyone.
    7. Open the '.env.example' file in the root directory of the project
    8. Paste the token into the 'BOT_TOKEN' field and save the file
5. Enable privileged intents
    1. Navigate back to the 'Bot' tab
    2. Under 'Privileged Gateway Intents', enable all three intents ('Presence', 'Server Members', 'Message Content')
    3. Save changes
6. Invite the bot to join your server
    1. Go to the 'OAuth2' tab.
    2. Under 'scopes', check the 'bot' field
    3. Under 'bot permissions' check the following fields
        * 'View Channels' (General permissions)
        * 'Send Messages' (Text permissions)
        * 'Send Messages in Threads' (Text permissions)
        * 'Embed Links' (Text permissions)
        * 'Attach Files' (Text permissions)
        * 'Use Slash Commands' (Text permissions)
    4. Click 'copy'
    5. Paste the URL in a new browser window or tab
    6. Choose a server to invite the bot to and click 'Authorize'
7. Get your personal user ID
    1. Open Discord and navigate to any server
    2. Right click on the your profile in the panel on the right
    3. Click 'Copy User ID'
    4. Open the '.env.example' file in the root directory of the project
    5. Paste the ID into the OWNER_USER_ID field and save the file 
8. Get the test channel ID
    1. Choose a channel to be your 'test channel'. This channel will recieve a 'running' message from the bot on startup
    2. Open Discord, right click on the desired channel and click 'Copy Channel ID'
    3. Open the '.env.example' file in the root directory of the project
    4. Paste the ID into the TEST_CHANNEL_ID field and save the file 
9. Change the '.env.example' file name to '.env'
   
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### Running the bot
1. Open a new terminal window in the root directory of the project
2. Run the following command 
```sh
python stable_diffusion_discord_bot.py
```
### Syncronising slash commands 
1. Open discord and navigate to the server the bot was invited to
2. In any text channel type '!sync' (without the quotations) and send the message
3. The bot should respond with 'command tree sync complete'
4. Press ctrl + R (or cmd + R on mac) to refresh discord and ensure the slash commands have been synchronised
5. These steps only need to be carried out once for each server the bot is in
### Slash command usage
The only command the bot uses is '/generate'. The generate slash command requires one compulsary user field which is 'prompt'. 
The other two optional fields are 'negative_prompt' and 'guidance_scale'. Guidance scale must be between 0 and 50.
To use the command, simply type '/generate' (without quotations), and fill in the fields as desired before sending the message.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact
Jack Swallow - jack.t.swallow@gmail.com

Project Link: [https://github.com/jacktswallow/stable-diffusion-discord-bot](https://github.com/jacktswallow/stable-diffusion-discord-bot)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
