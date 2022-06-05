import requests
from bs4 import BeautifulSoup

page = requests.get("https://mlwbd.top/")
soup = BeautifulSoup(page.content, "html.parser")
    
all_movies = soup.find(id="dtw_content-6")

titles = [name.find('h3').get_text() for name in all_movies.find_all(class_="w_item_b")]
links = [link['href'] for link in all_movies.find_all('a', href=True) if link.text]

thumbnails = [image['src'] for image in all_movies.find_all('img', src=True)]
images = [thumbnails[i] for i in range(len(thumbnails)) if i % 2 != 0]

movies = [{'title': titles[i], 'link': links[i], 'image': images[i]} for i in range(len(titles))]

print(movies[1].get('title'))



