import json
from bs4 import BeautifulSoup
import urllib
import requests
import time
import os
import random
import string

OUT_DIR = "images"
OUT_FILE = "./movies.json"
LARGE_CDN_URL = "https://xl.movieposterdb.com/"
NORMAL_CDN_URL = "https://posters.movieposterdb.com/"
GITHUB_CDN_URL = "https://raw.githubusercontent.com/AEManov20/movie-poster-storage/main/{}"

f = open(OUT_FILE)
movies = json.load(f)
time_start = time.time()
f.close()

def create_dir():
    try:
        os.mkdir(OUT_DIR)
    except:
        pass


def save_image(url: str):
    file_name = url.split("/")[-1]
    path = os.path.join(OUT_DIR, file_name)
    response = requests.get(url)

    if response.status_code >= 400 or len(response.content) == 0:
        print(f"Error when saving image: {url}")
        return

    f = open(path, "wb")
    f.write(response.content)
    f.close()

    return path


def get_image_url(soup: BeautifulSoup, retries = 20):
    if retries < 0:
        raise RuntimeError("Retries exceeded!")

    try:
        image_element = soup.select(".section")[0].select(".vertical-image")[
            abs(-20 + retries)
        ]
        param_components = str(image_element.get("data-src")).split("/")[3:]
        param_components[-1] = param_components[-1].replace("s", "xl", 1)
        return LARGE_CDN_URL + "/".join(param_components)
    except:
        print("Failed! Retrying...")
        return get_image_url(soup, retries - 1)


def do_request(url: str):
    user_agent = "".join(
        random.choices(string.ascii_lowercase + string.ascii_uppercase, k=20)
    )
    response = requests.get(
        url,
        headers={"User-Agent": user_agent},
    )
    print(
        f'Requested "{url}". Status: {response.status_code}. Remaining: {response.headers["x-ratelimit-remaining"]}. UserAgent: {user_agent}'
    )
    return response


def process_request(response: requests.Response):
    global time_start

    if time_start == 0:
        time_start = time.time()

    if int(response.headers["x-ratelimit-remaining"]) == 0:
        sleep_time = 120 - (time.time() - time_start)
        print(f"Requests per minute over. Sleeping for {sleep_time}")
        time.sleep(sleep_time)
        time_start = 0

    soup = BeautifulSoup(response.text, "html.parser")
    url = get_image_url(soup)

    return save_image(url)

url = "https://www.movieposterdb.com/search?q={}&imdb=0"
query = "INSERT INTO public.movies (name, description, genre, release_date, length, imdb_link, is_deleted, poster_image_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?);\n"

def c(x):
    path = process_request(do_request(url.format(x["title"])))
    x['posterUrl'] = path
    return x

create_dir()

movies = list(map(lambda x: c(x), movies))
print(movies)
f = open(OUT_FILE, 'w')
json.dump(movies, f)
f.close()
