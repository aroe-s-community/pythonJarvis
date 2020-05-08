# Dependencies
import discord
import os

# Local dependencies
from modules.csv import CSV
from modules.news import News
from modules.discordhelp import DiscordHelp

client = discord.Client()

# set your bot token as an environment variable, e.g.,
# `export JARVIS_TOKEN="<token>"`
token = os.environ['JARVIS_TOKEN']

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$news'):
        result = News.getNews(message)

        if not DiscordHelp.isValidLength(result):
            result = "**Too many articles to list**"

        await message.channel.send(result)

client.run(token)
