from bs4 import BeautifulSoup
import csv
import requests

# Sometimes requests doesn't work unless you have a User-Agent header *shrug*
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}

# Get today's news from bleepingcomputer.com
def bleeping_computer():
    # This will hold the data points from each article
    articles = []

    url = "https://www.bleepingcomputer.com/"

    # Connect to site
    r1 = requests.get(url, headers=headers)

    # Get content
    coverpage = r1.content

    # Convert to soup-readable format
    soup1 = BeautifulSoup(coverpage, 'lxml')

    # Extract every article on the page
    coverpage_news = soup1.find_all('div', class_='bc_latest_news_text')

    # This is a little janky, but I'm still trying to figure out bs4
    # Add data to
    for news in coverpage_news:
        title = news.contents[3].a
        link = title['href']
        title = title.text
        description = news.contents[5].text
        author = news.contents[7].a.text

        articles.append([title, link, description, author])

    return articles

# Contents requires each article to have: title, link, description, author
# ORDER MATTERS
def append_csv(contents, filename):
    # Open csv file
    with open('tmp/articles.csv', mode='a') as fp:
        headline_writer = csv.writer(fp, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Write each article to csv
        for c in contents:
            headline_writer.writerow(c)

# Clear a csv file
def clear_csv(filename):
    with open(filename, mode='w') as fp:
        fp.close()
