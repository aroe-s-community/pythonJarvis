from bs4 import BeautifulSoup
from datetime import date, datetime
from string import Formatter
import requests

class News:
    # Sometimes requests doesn't work unless we have some specific headers *shrug*
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}

    # Website Scraping Functions

    @staticmethod
    def getSoup(url):
        site = requests.get(url, headers=News.headers)
        coverpage = site.content
        soup = BeautifulSoup(coverpage, 'lxml')

        return soup

    @staticmethod
    def darkReading():
        articles_list = []

        url = "https://darkreading.com/"

        soup = News.getSoup(url)

        # Get list of articles
        articles = soup.find('div', id='left-column-inner')

        today = date.today()

        for article in articles.find_all('header', class_='strong medium'):
            data = article.findNextSibling('div', style='overflow: hidden;')

            date_str = str(data.find('span', class_='allcaps smaller').next_sibling).split(',')[-1].strip()
            article_date = datetime.strptime(date_str, '%m/%d/%Y').date()
            if article_date < today:
                # We have hit the end of today's articles
                break

            info = {}

            info['date'] = str(article_date)

            link = article.find('a')['href']
            info['link'] = 'https://darkreading.com' + link

            info['title'] = article.find('a')['title']

            description = data.find('span', class_='black smaller')
            info['description'] = description.text

            author = data.find('a', class_='color-link')
            info['author'] = author.text

            articles_list.append(info)

        return articles_list


    # Get today's news from bleepingcomputer.com
    @staticmethod
    def bleeping_computer():
        # This will hold the data points from each article
        articles_list = []

        url = "https://www.bleepingcomputer.com/"

        soup = News.getSoup(url)

        # Extract every article on the page
        articles = soup.find_all('div', class_='bc_latest_news_text')

        today = date.today()

        # This is a little janky, but I'm still trying to figure out bs4
        # Add data to
        for article in articles:
            date_str = article.find('li', class_='bc_news_date').text
            article_date = datetime.strptime(date_str, '%b %d, %Y').date()
            if article_date < today:
                continue

            info = {}

            info['date'] = str(article_date)

            title = article.contents[3].a
            link = title['href']
            info['link'] = link

            title = title.text
            info['title'] = title

            description = article.contents[5].text
            info['description'] = description

            author = article.contents[7].a.text
            info['author'] = author

            articles_list.append(info)

        return articles_list

    @staticmethod
    def getNewsList(site):
        if site == "bleepingcomputer":
            return News.bleeping_computer()
        elif site == "darkreading":
            return News.darkReading()
        else:
            raise UnknownSiteError(site)

    @staticmethod
    def getNews(message):
        # format is "$news site number", where number is the number
        # of articles to return, because discord has a character limit
        # of 2000. You could make it send multiple messages but whatever.
        split_message = message.content.split(' ')

        if len(split_message) < 3:
            return 'Format is ```$news [website] [number of articles]```'

        site = split_message[1]
        n = int(split_message[2])

        try:
            articles = News.getNewsList(site)[:n]

        except (UnknownSiteError, IndexError):
            result = '**Valid sites are:** \n\nbleepingcomputer\ndarkreading'
            return result

        except ValueError:
            result = '**Pick a valid number of results to return**'
            return result

        formatter = Formatter()
        responses = []
        for i, article in enumerate(articles):
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
