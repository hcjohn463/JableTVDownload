import argparse
import requests
from bs4 import BeautifulSoup
import cloudscraper
import random


def get_parser():
    parser = argparse.ArgumentParser(description="Jable TV Downloader")
    parser.add_argument("--random", type=bool, default=False,
                        help="Enter True for download random ")
    parser.add_argument("--url", type=str, default="",
                        help="Jable TV URL to download")

    return parser


def av_recommand():
    url = 'https://jable.tv/'
    r = requests.get(url)
    # 這邊用 cloudscraper 取代 requests，這套件幫我們
    new_response = cloudscraper.create_scraper().get(url)
    # 得到繞過轉址後的 html
    soup = BeautifulSoup(new_response.text, 'html.parser')
    # print(soup.prettify())
    h6_tags = soup.find_all('h6', class_='title')
    # print(h6_tags)
    av_list = []
    for tag in h6_tags:
        # print(tag)
        # print(tag.text.split(' ')[0][0])
        if((tag.text.split(' ')[0][0] >= 'a' and tag.text.split(' ')[0][0] <= 'z') or (tag.text.split(' ')[0][0] >= 'A' and tag.text.split(' ')[0][0] <= 'Z')):
            # print(tag.a.get('href'))
            av_list.append(tag.a.get('href'))
    # print(av_list)
    return random.choice(av_list)


# print(av_recommand())
