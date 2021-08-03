#!/usr/bin/env python
# coding: utf-8

import requests
import os
from lxml import etree

def downloadCover(htmlfile,folderPath,fileName):
    print('开始下载封面')

    html = etree.HTML(htmlfile.text)
    imageUrl = html.xpath('//meta[@property="og:image"]/@content')[0]
    respone = requests.get(imageUrl)
    with open(os.path.join(folderPath,fileName + '.jpg'),"wb")as f:
        f.write(respone.content)
        
    print('下载封面完成')