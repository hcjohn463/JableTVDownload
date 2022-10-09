import requests
from bs4 import BeautifulSoup

from config import headers


def input_url_validator(tag_url):
    if "from=" in tag_url:
        raise Exception("input url is not valid. url cannot contain page number")
    if not ("tags" in tag_url or "models" in tag_url):
        raise Exception("input url is not valid. only support tags and models")


def get_model_names_and_last_page_num(url):
    res = requests.get(url, headers=headers, timeout=10)
    last_page_num = 1
    if res.status_code == 200:
        content = res.content
        soup = BeautifulSoup(content, 'html.parser')

        model_name = soup.select('#list_videos_common_videos_list > section > div > div > div > h2')[0].text
        page_items = soup.select('.pagination>.page-item>.page-link')
        last_item = page_items[-1].get('data-parameters')
        if last_item:
            page_num = last_item.split(":")[-1]
            if page_num.isdigit():
                last_page_num = int(last_item.split(":")[-1])
    return model_name, last_page_num


def get_all_video_links(url):
    tag_name, last_page_num = get_model_names_and_last_page_num(url)
    if not url.endswith('/'):
        url = url + '/'

    video_links = set()
    for page_num in range(1, last_page_num + 1):
        page_url = url + "?from=%s" % page_num
        print("抓取 %s 第 %s 页 共 %s 页" % (tag_name, page_num, last_page_num))
        res = requests.get(page_url, headers=headers, timeout=10)
        if res.status_code == 200:
            content = res.content
            soup = BeautifulSoup(content, 'html.parser')
            a_tags = soup.select('div.img-box>a')
            for a_tag in a_tags:
                video_links.add(a_tag['href'])

    print('%s => 获取到 %s 个影片' % (tag_name, len(video_links)))
    return video_links
