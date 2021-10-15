# Konmaek Bot

## **Create Discord Bot**

### **Install Pypl**
```bash
py -3 -m pip install -U discord.py
```
### **Install Virtual Enviroments**
* Go to `your project's working directory`
```bash
cd [YOUR-WORKING-DIRECTORY]
```
* Install all command
```bash
py -3 -m venv bot-env
bot-env\Scripts\activate.bat
pip install -U discord.py
```
### Create File **`discord.py`** in Directory: **`/bot-env`**
```py
import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = MyClient()
client.run('[YOUR-TOKEN-DISCORD-BOT]')
```
Congratulations. You now have all set up.

## Quickstart
### A Minimal Bot
Test a bot by create **`[YOUR-FILE].py`**
and Source Code:
```py
import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('[YOUR-TOKEN-DISCORD-BOT]')
```
Test to run in Terminal:
```bash
py [YOUR-FILE].py
```