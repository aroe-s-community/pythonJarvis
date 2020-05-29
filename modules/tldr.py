import requests
import discord

class TLDR:
    BASE_URL = "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/"

    PLATFORMS = ['linux', 'common', 'osx', 'windows']

    COMMANDS = requests.get("https://tldr.sh/assets/index.json").json()['commands']

    helpFile = 'docs/tldr.md'

    def notFound(command):
        return '`' + command + "` documentation is not available. Consider contributing Pull Request to <https://github.com/tldr-pages/tldr>"

    def getHelp():
        with open(TLDR.helpFile, 'r') as fp:
            return fp.read()

    # Given a command str and list of platforms for that command,
    # loop through general list of platforms in specific order
    def getPageURL(command, platforms):
        page = None
        # This loop allows us to search for commands in a specific platform order
        for platform in TLDR.PLATFORMS:
            if platform in platforms:
                page = TLDR.BASE_URL + platform + '/' + command + '.md'
                break

        return page

    # Loop through list of all commands. If the command exists,
    # return the json information of the command.
    # Else, return None
    def getPlatform(command):
        for cmd in TLDR.COMMANDS:
            if cmd['name'] == command:
                return cmd['platform']

        return None

    def getPage(command):
        platforms = TLDR.getPlatform(command)
        # Command doesn't exist
        if platforms == None:
            return None

        url = TLDR.getPageURL(command, platforms)

        page = requests.get(url)
        return page

    def tldr(message):
        splitMessage = message.content.split(' ')

        if len(splitMessage) != 2 or splitMessage[1] == "-h":
            return TLDR.getHelp()

        # Get the command we are searching for
        command = splitMessage[-1]

        # Get request
        page = TLDR.getPage(command)
        if page is None:
            return TLDR.notFound(command)

        # page.content is class bytes so we need to decode it
        content = "```markdown\n" + page.content.decode("utf-8") + "\n```"

        # Create the embed
        embed = discord.Embed(description=content)

        return embed
