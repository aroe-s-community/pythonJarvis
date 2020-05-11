# Jarvis

Jarvis is a bot for Discord, mainly for [aRoe's Cyber Palace](https://discord.gg/DH8x6CT). Some bot functions include:

* Fetching News from Cyber Security Resources
* Fetch CVE details
* Print out a TL;DR Page for a command-line program
* ... and many more to come!

## Installation

To run this bot on your own server, you can clone this repo. You also need to set your Bot Token as an environment variable:

```bash
# Clone this repo
$ git clone https://github.com/aroe-s-community/new_jarvis_discord_bot.git
$ cd new_jarvis_discord_bot
$ pip install -r requirements.txt

# Set environment variable (Linux)
$ export JARVIS=[Bot Token Here]
```

## Contributing

Have an idea on how to make this bot better? We would love to have your contributions. You can fork this repo, and then submit a Pull Request with your changes to the `dev` branch.

To start working, you need to set up a virtualenv. More information can be found [here](https://virtualenvwrapper.readthedocs.io/en/latest/), but an abridged version to get set up quickly is below.

```bash
# Set up virtualenv
$ sudo pip install virtualenv virtualenvwrapper
$ export WORKON_HOME=~/.config/.virtualenvs
# Add the following line to your ~/.bashrc
source /usr/local/bin/virtualenvwrapper.sh

# Now clone the repo
$ git clone https://github.com/YOUR_USERNAME/new_jarvis_discord_bot.git
$ cd new_jarvis_discord_bot
# Make a python3 virtual environment
$ mkvirtualenv new_jarvis -p python3
$ pip install -r requirements.txt
```

## License
This software is distributed under the [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html).
