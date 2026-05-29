# author: hcjohn463
#!/usr/bin/env python
# coding: utf-8
from args import *
from download import download
from movies import movieLinks

parser = get_parser()
args = parser.parse_args()

proxy_url = args.proxy if hasattr(args, 'proxy') else None

if(len(args.url) != 0):
    url = args.url
    download(url, proxy_url)
elif(args.random == True):
    url = av_recommand(proxy_url)
    download(url, proxy_url)
elif(args.all_urls != ""):
    all_urls = args.all_urls
    urls = movieLinks(all_urls, proxy_url)
    for url in urls:
        download(url, proxy_url)
else:
    # 使用者輸入Jable網址
    url = input('輸入jable網址:')
    download(url, proxy_url)
