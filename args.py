import argparse
from bs4 import BeautifulSoup
import random
from urllib.request import Request, urlopen
from config import headers
import re


def get_parser():
    parser = argparse.ArgumentParser(description="Jable TV Downloader")
    parser.add_argument("--random", type=bool, default=False,
                        help="Enter True for download random ")
    parser.add_argument("--url", type=str, default="",
                        help="Jable TV URL to download")
    parser.add_argument("--nogui", type=bool, default=False,
                        help="True for disable gui mode")

    return parser


def av_recommand():
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://jable.tv/'
    request = Request(url, headers=headers)
    web_content = urlopen(request).read()
    # 得到繞過轉址後的 html
    soup = BeautifulSoup(web_content, 'html.parser')
    h6_tags = soup.find_all('h6', class_='title')
    av_list = re.findall(r'https[^"]+', str(h6_tags))
    return random.choice(av_list)


# print(av_recommand())
