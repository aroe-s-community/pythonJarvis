# Dependencies
import discord
import os

# Local dependencies
from modules.cve import CVE
from modules.csv import CSV
from modules.news import News
from modules.discordhelp import DiscordHelp

client = discord.Client()

# set your bot token as an environment variable, e.g.,
# `export JARVIS_TOKEN="<token>"`
token = os.environ['JARVIS_TOKEN']

helpFile = 'docs/bot.md'

def helpMessage():
    with open(helpFile, 'r') as fp:
        return fp.read()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('$help'):
        await message.channel.send(helpMessage())

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$news'):
        result = News.getNews(message)

        if not DiscordHelp.isValidLength(result):
            result = "**Too many articles to list**"

        await message.channel.send(result)

    if message.content.startswith('$cve'):
        result = CVE.cveSearch(message)
        await message.channel.send(result)

client.run(token)
