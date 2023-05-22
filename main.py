# author: hcjohn463
#!/usr/bin/env python
# coding: utf-8
from args import *
from download import download
from encode import ffmpegEncode
from movies import movieLinks
# In[2]:


def process_single_job(args, url):
    """Process single url job including download and convert"""
    (folder_path, file_name) = download(url)
    # 轉檔
    if args.encode != 'none':
        ffmpegEncode(folder_path, file_name, args.encode)


parser = get_parser()
args = parser.parse_args()

if(len(args.url) != 0):
    process_single_job(args, args.url)
elif(args.random == True):
    url = av_recommand()
    process_single_job(args, url)
elif(args.all_urls != ""):
    all_urls = args.all_urls
    urls = movieLinks(all_urls)
    for url in urls:
        process_single_job(args, url)
else:
    # 使用者輸入Jable網址
    url = input('輸入jable網址:')
    process_single_job(args, url)

