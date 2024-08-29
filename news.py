import requests
import time
from PIL import Image
from io import BytesIO

from config import GNEWS_KEY

def grab_articles(image_files):
    url = f'https://gnews.io/api/v4/top-headlines?lang=en&category=general&apikey={GNEWS_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json()['articles']
        urls = []
        for i, article in enumerate(articles):
            image_url = article['image']
            if image_url:
                filename = f'image_{i}.jpg'
                if download_image(image_url, filename):
                    urls.append(article['url'])
                    image_files.append(filename)
                if len(urls) == 10:
                    break
        time.sleep(1)
        return urls
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response text: {response.text}")
        raise Exception("Failed to fetch articles. Stopping execution.")

def download_image(url, filename):
    response = requests.get(url)
    try:
        img = Image.open(BytesIO(response.content))  # try to open the image
        img.verify()  # verify that it is, in fact, an image
    except (IOError, SyntaxError) as e:
        print('Bad file:', filename)  # print out the names of corrupt files
        return False
    if len(img.getbands()) in (3, 4):
        with open(filename, 'wb') as f:
            f.write(response.content)
        return True
    else:
        print('Image is not 3D:', filename)
        return False
