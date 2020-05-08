from datetime import date, datetime
from string import Formatter
from time import mktime

import feedparser

class News:
    helpFile = 'docs/news.md'
    # Get help message
    def getHelp():
        with open(News.helpFile, 'r') as fp:
            return fp.read()

    # Feed URLs
    bleepingComputer = "https://bleepingcomputer.com/feed/"
    darkReading = "https://www.darkreading.com/rss_simple.asp"

    # Get list of articles from url
    @staticmethod
    def getEntries(url):
        return feedparser.parse(url)['entries']

    @staticmethod
    def getNewsList(site):
        if site == "bleepingcomputer":
            return News.getEntries(News.bleepingComputer)
        elif site == "darkreading":
            return News.getEntries(News.darkReading)
        else:
            raise UnknownSiteError(site)

    @staticmethod
    def getNews(message):
        # format is "$news site [number]", where number is the number
        # of articles to return, because discord has a character limit
        # of 2000. You could make it send multiple messages but whatever.
        split_message = message.content.split(' ')

        if len(split_message) < 2 or len(split_message) > 3:
            return News.getHelp()

        site = split_message[1]

        try:
            n = 5
            if len(split_message) == 3:
                n = int(split_message[2])

            articles = News.getNewsList(site)[:n]

        except (UnknownSiteError, IndexError):
            result = '**Valid sites are:** \n\nbleepingcomputer\ndarkreading'
            return result

        except ValueError:
            result = '**Pick a valid number of results to return**'
            return result

        if not articles:
            return '**Sorry, there are no articles posted today!**'

        formatter = Formatter()
        responses = []
        today = date.today()
        for i, article in enumerate(articles):
            date_ = date.fromtimestamp(mktime(article['published_parsed']))
            if today > date_:
                break

            response = formatter.format("{num}. {title} by {author} ({link})", num=i+1, \
                                        title=article['title'], author=article['author'], \
                                        link=article['link'])

            responses.append(response)

        result = '\n'.join(responses)

        return result

class UnknownSiteError(Exception):
    def __init__(self, site):
        self.site = site

    def __str__(self):
        return 'Unkown site "' + self.site + '".'
