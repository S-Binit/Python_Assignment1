import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Target URL
url = 'https://kathmandupost.com/'

# Fetch the page
response = requests.get(url)
# <html>...</html>

soup = BeautifulSoup(response.text, features='html.parser')

# Inside ul having class trending-topics-list, all li elements having a tags, extract their url
trending_topics_section = soup.find('ul', class_='trending-topics-list')
trending_topics = trending_topics_section.find_all('li')

trending_paths = []
for each_topic in trending_topics:
    a_tag = each_topic.find('a')
    if a_tag:
        trending_paths.append(a_tag['href'])

trending_articles_urls = []
for each_path in trending_paths:
    full_url = 'https://kathmandupost.com' + each_path
    trending_articles_urls.append(full_url)

    file_name = "kathmandu_post_trending.txt"


with open(file_name, "a", encoding="utf-8") as f:
    for article_url in trending_articles_urls:
        article_response = requests.get(article_url)
        article_soup = BeautifulSoup(article_response.text,'html.parser')

        tag_mark = article_soup.find('h4', class_='title--line__red')
        tag = tag_mark.find('a').get_text(strip=True) if tag_mark else None
        
        title = tag_mark.find_next('h1').get_text(strip=True)
        
        article_data = {
            'title': title + "\n",
            'tag': tag + "\n",
            'url': article_url  + "\n",
            'scraped_at': datetime.now().isoformat() + "\n"
        }
        
        f.write("Title: " + article_data['title'])
        f.write("Tag: " + str(article_data['tag']))
        f.write("URL: " + article_data['url'])
        f.write("Scraped At: " + article_data['scraped_at'])
        f.write("\n" + "." * 80 + "\n\n")

print("Data saved to txt file")
