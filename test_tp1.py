# import requests
# from bs4 import BeautifulSoup

# url = "https://www.blogdumoderateur.com/web/"

# def fetch_articles(url):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#     }

#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, 'html.parser')

#         articles_data = []

#         main_tag = soup.find('main')
#         if not main_tag:
#             print("No <main> tag found.")
#             return []

#         articles = main_tag.find_all('article')
#         for article in articles:

#             # # Image url
#             # img_div = article.find('div', class_='post-thumbnail picture rounded-img')
#             # img_tag = img_div.find('img') if img_div else None
#             # img_url = img_tag['src'] if img_tag else None 




#             meta_div = article.find(
#                 'div',
#                 class_='entry-meta ms-md-5 pt-md-0 pt-3'
#             )
#             # tag = (meta_div.find('span', class_='favtag color-b')
#             #            .get_text(strip=True)
#             #        ) if meta_div else None
#             # date = (meta_div.find('span', class_='posted-on t-def px-3')
#             #             .get_text(strip=True)
#             #        ) if meta_div else None

#             header = (meta_div.find('header', class_='entry-header pt-1')
#                       ) if meta_div else None
#             a_tag = header.find('a') if header else None

#             # Title
#             # title = (a_tag.find('h3').get_text(strip=True)
#             #          ) if a_tag and a_tag.find('h3') else None
            
#             article_url = None  # Default null value

#             article_url = a_tag['href'] if a_tag and a_tag.has_attr('href') else None
            
#             # Extract thumbnail
#             # thumbnailImageUrl = soup.select_one('div.meta-picture > img').get('src') #soup.find('div', class_='meta-picture').find('img')['src'] if soup.find('div', class_='meta-picture') else None
#             #img where ?
#             #src /data-lazy-src / srcset
#             # thumbnailImageUrl = img_tag.get('src') if (img_tag := soup.select_one('div.meta-picture > img')) else None
            
#             # Enter inside the url to get the further info    
#             if article_url is not None:  # Explicit check
#                 tmp_article = fetch_articles(article_url)    #fetch un seule article
#         #article (complete article) 'article'
#             #header (header.entry-header)
#                 #title (h1.entry-title)
#                 #summary (div.article-hat p)
#                 #author (span.byline)
#                 #date (span.posted-on time[attrb=datetime])
#                 #thumbnail 
#                     #image (figure.article-hat-img img[attrb=src])
#                     #caption (figcaption.legend text())
#             #body div.entry-content
#         # fetch_articles(page + 1)
            

#             # summary_div = (meta_div.find('div', class_='entry-excerpt t-def t-size-def pt-1')
#             #                ) if meta_div else None
#             # summary = summary_div.get_text(strip=True) if summary_div else None

#             articles_data.append({
#                 # 'image': img_url,
#                 # 'tag': tag,
#                 # 'date': date,
#                 'url': article_url,
#                 # 'title': title,
#                 # 'thumbnail' : thumbnailImageUrl
#                 # 'summary': summary
#             })

#         return articles_data

#     except requests.exceptions.RequestException as e:
#         print(f"Error: {e}")
#         return []

# # def extract_img_url(img_tag):
# #     if not img_tag:
# #         return None
# #     url_attributes = [
# #         'data-lazy-src',
# #         'data-src',
# #         'src'
# #     ]
# #     for attr in url_attributes:
# #         if img_tag.has_attr(attr):
# #             url = img_tag[attr]
# #             if url and url.startswith('https://'):
# #                 return url
# #     return None


# articles = fetch_articles(url)

# for i, article in enumerate(articles, 1):
#     print(f"\nArticle {i}:")
#     for key, value in article.items():
#         print(f"{key.capitalize()}: {value}")
 

# #  1 . All the urls from main page
# #  2 . for loop for all the urls
# #  3 . Enter in each artical and scrap and return one object corresponding to the artical.

import requests
from bs4 import BeautifulSoup

def fetch_articles(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        articles_data = []

        main_tag = soup.find('main')
        if not main_tag:
            print("No <main> tag found.")
            return []
        
        # Extract title
        titles = soup.find('h3', class_='entry-title').get_text(strip=True)
        
        # titles = main_tag.find_all('h3', class_='entry-title').get_text(strip=True)
        for title in titles:
            title_h3 = title.find(
                'div',
                class_='post-thumbnail picture rounded-img'
            )
            # print(img_div)
        return title_h3

        # # Extract thumbnail
        # thumbnail = soup.find('div', class_='post-thumbnail').find('img')['src'] if soup.find('div', class_='post-thumbnail') else None
        
        # # Extract categories
        # categories = [a.get_text(strip=True) for a in soup.find('div', class_='entry-categories').find_all('a')]
        # main_category = categories[0] if categories else None
        # sub_category = categories[1] if len(categories) > 1 else main_category
        
        # # Extract summary
        # summary = soup.find('div', class_='entry-excerpt').get_text(strip=True) if soup.find('div', class_='entry-excerpt') else None
        
        # # Extract date
        # date_str = soup.find('time', class_='entry-date')['datetime']
        # date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
        
        # # Extract author
        # author = soup.find('span', class_='author-name').get_text(strip=True) if soup.find('span', class_='author-name') else None
        
        # # Extract article content
        # content_div = soup.find('div', class_='entry-content')
        # content = ' '.join([clean_text(p.get_text()) for p in content_div.find_all(['p', 'h2', 'h3']) if p.get_text().strip()])
        
        # # Extract images with captions
        # images = []
        # for img in content_div.find_all('img'):
        #     img_data = {
        #         'url': img['src'] if 'src' in img.attrs else None,
        #         'alt': img.get('alt', ''),
        #         'caption': img.find_parent('figure').find('figcaption').get_text(strip=True) if img.find_parent('figure') and img.find_parent('figure').find('figcaption') else None
        #     }
        #     images.append(img_data)
        
        # article_data = {
        #     'title': title,
        #     'thumbnail': thumbnail,
        #     'main_category': main_category,
        #     'sub_category': sub_category,
        #     'summary': summary,
        #     'date': date,
        #     'author': author,
        #     'content': content,
        #     'images': images,
        #     'url': article_url,
        #     'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # }
        
        # return article_data
    
    except Exception as e:
        print(f"Error scraping {article_url}: {str(e)}")
        return None

#         articles = main_tag.find_all('article')
#         for article in articles:
#             img_div = article.find(
#                 'div',
#                 class_='post-thumbnail picture rounded-img'
#             )
#             # print(img_div)
#         return articles_data

#     except requests.exceptions.RequestException as e:
#         print(f"Error: {e}")
#         return []
    
url = "https://www.blogdumoderateur.com/web/"
articles = fetch_articles(url)

for i, title in enumerate(titles, 1):
    print(f"\nTitle {i}:")
    for key, value in title.items():
        print(f"{key.capitalize()}: {value}")