from bs4 import BeautifulSoup
import requests
import csv

def pl():
    print('\n')

def bleeping_computer():
    articles = []

    url = "https://www.bleepingcomputer.com/"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}

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
def write_to_csv(contents):
    # Open csv file
    with open('tmp/articles.csv', mode='w') as headline_file:
        headline_writer = csv.writer(headline_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Write each article to csv
        for c in contents:
            headline_writer.writerow(c)

