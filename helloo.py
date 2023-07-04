import requests
from bs4 import BeautifulSoup

def get_images(topic:str):
    word = topic
    url = 'https://www.google.com/search?q={0}&tbm=isch&tbs=isz:l'.format(word)
    content = requests.get(url).content
    soup = BeautifulSoup(content,'lxml')
    images = soup.findAll('img')
    urls = []
    for image in images:
        print(image.get("width"))
        name = image.get('src')
        if name.endswith(".gif"):
            continue
        urls.append(name)
    return urls