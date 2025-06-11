#  1 . All the urls from main pages (first five)
#  2 . For loop for all the urls
#  3 . Enter in each artical, scrap and return one object corresponding to the artical.
#  4 . Save the data in MongoDB

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# Connexion MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["blog_scraper"]
collection = db["articles"]

base_url = "https://www.blogdumoderateur.com/web/page/"

articles_url_data = []
articles_data = []

# To get the urls of articles of the page
def fetch_articles(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        main_tag = soup.find('main')
        if not main_tag:
            print("No <main> tag found.")
            return []

        articles = main_tag.find_all('article')
        for article in articles:

            meta_div = article.find(
                'div',
                class_='entry-meta ms-md-5 pt-md-0 pt-3'
            )

            header = (meta_div.find('header', class_='entry-header pt-1')
                      ) if meta_div else None
            a_tag = header.find('a') if header else None

            article_url = a_tag['href'] if a_tag and a_tag.has_attr('href') else None           

            articles_url_data.append({
                'url': article_url,
            })
        return articles_url_data

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

# To get urls of the articles of the first five pages
for page in range(1, 6):  # Scrape first 5 pages
    url = f"{base_url}{page}/"
    all_articles = fetch_articles(url)

for i, article in enumerate(all_articles, 1):
    print(f"\nArticle {i}:")
    for key, value in article.items():
        print(f"{key.capitalize()}: {value}")


# To get the data of specific article
def fetch_article(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        main_tag = soup.find('main')
        if not main_tag:
            print("No <main> tag found.")
            return []
        
        # header
        header = (main_tag.find('header', class_='entry-header')
                      ) if main_tag else None
        # title
        h1_title = header.find('h1').get_text(strip=True) if header else None
        title = h1_title.replace('&nbsp;', ' ') if header else None
        # summary
        div_summary = header.find('div', class_='article-hat') if header else None
        summary = div_summary.find('p').get_text(strip=True) if div_summary else None
        # author
        span_author = header.find('span', class_='byline') if header else None
        a_tag = span_author.find('a') if span_author else None
        author = a_tag.get('title') if a_tag else None 
        # date
        span_date = header.find('span', class_='posted-on') if header else None
        time_tag = span_date.find('time', class_='entry-date') if span_date else None
        date = time_tag.get('datetime') if time_tag else None
        # thumbnail_img
        thumbnail_img = None
        figure_img = header.find('figure', class_='article-hat-img') if header else None 
        a_img = figure_img.find('a') if figure_img else None
        img_tag_ = a_img.find('img', class_='mx-auto') if a_img else None 
        thumbnail_img = img_tag_['src'] if img_tag_ else None

        # Find the main content container
        content_div = main_tag.find('div', class_='entry-content')

        # Initialize lists to store the extracted content
        headings = []
        paragraphs = []

        if content_div:
        # Extract all h2, h3, and p elements
            for element in content_div.find_all(['h2', 'p']):
                if element.name in ['h2']:
                    headings.append({
                 'level': element.name,
                    'text': element.get_text(strip=True)
                })
                elif element.name == 'p':
                    paragraphs.append(element.get_text(strip=True))
                 

        articles_data.append({
                'url': url,
                'title': title,
                'summary': summary,
                'author' : author,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                'date' : date,
                'thumbnail_img' : thumbnail_img,                
                'headings' : headings,
                'paragraphs' : paragraphs
            })
        return articles_data

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

 
for i, article in enumerate(all_articles, 1):
        for key, value in article.items():
            url_ = f"{value}"
            dataofarticals = fetch_article(url_)

    
for i, article in enumerate(dataofarticals, 1):
        print(f"\nArticle {i}:")
        collection.insert_one(article)
        for key, value in article.items():            
            print(f"{key.capitalize()}: {value}")
    # "C:\Users\Kalyan\Desktop\MscBigDataAI\IPSSI\9th W React\tp_beautiful_soup.py"