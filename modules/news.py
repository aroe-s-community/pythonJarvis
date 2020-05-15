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
    sites = {
        "bleepingcomputer": "https://bleepingcomputer.com/feed/",
        "darkreading": "https://www.darkreading.com/rss_simple.asp",
        "_3howley": "https://ethanizen.com//feed.xml",
        "plastic": "https://plasticuproject.github.io/blog/index.xml",
        "ycombinator": "https://news.ycombinator.com/rss",
        "nakedsecurity": "https://nakedsecurity.sophos.com/feed/",
        "threatpost": "https://threatpost.com/feed/",
        "krebs": "https://krebsonsecurity.com/feed/"
    }

    # Get list of articles from url
    @staticmethod
    def getEntries(url):
        return feedparser.parse(url)['entries']

    @staticmethod
    def getNewsList(site):
        if site in News.sites:
            return News.getEntries(News.sites[site])
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
            sites = '\n'.join(News.sites.keys())

            result = '**Valid sites are:**\n\n' + sites
            return result

        except ValueError:
            result = '**Pick a valid number of results to return**'
            return result

        if not articles:
            return '**Sorry, there are no articles!**'

        formatter = Formatter()
        responses = []
        for i, article in enumerate(articles):
            title = article['title']

            author = ''
            if 'author' in article.keys():
                author = ' by ' + article['author']

            link = article['link']

            response = formatter.format("{num}. {_title}{_author} (<{link}>)", num=i+1, \
                                        _title=title, _author=author, \
                                        link=link)

            responses.append(response)

        result = '\n'.join(responses)

        return result

class UnknownSiteError(Exception):
    def __init__(self, site):
        self.site = site

    def __str__(self):
        return 'Unkown site "' + self.site + '".'
