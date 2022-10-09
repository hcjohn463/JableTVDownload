import concurrent.futures
import copy
import os
import re
import time
import urllib.request
from functools import partial

import cloudscraper
import m3u8
import requests
from Crypto.Cipher import AES
from bs4 import BeautifulSoup

from config import CONF, headers
from utils import deleteM3u8, deleteMp4
from utils import merge_mp4
from video_crawler import prepareCrawl


def get_cover(html_file, folder_path):
    soup = BeautifulSoup(html_file.text, "html.parser")
    cover_name = f"{os.path.basename(folder_path)}.jpg"
    cover_path = os.path.join(folder_path, cover_name)
    for meta in soup.find_all("meta"):
        meta_content = meta.get("content")
        if not meta_content:
            continue
        if "preview.jpg" not in meta_content:
            continue
        try:
            r = requests.get(meta_content)
            with open(cover_path, "wb") as cover_fh:
                r.raw.decode_content = True
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        cover_fh.write(chunk)
        except Exception as e:
            print(f"unable to download cover: {e}")

    print(f"cover downloaded as {cover_name}")


def download_by_video_url(url):
    # 建立番號資料夾
    urlSplit = url.split('/')
    dirName = urlSplit[-2]
    # TODO: 修改为文件名
    if not os.path.exists(dirName):
        os.makedirs(dirName)
    folderPath = os.path.join(os.getcwd(), dirName)

    # 得到 m3u8 網址
    htmlfile = cloudscraper.create_scraper(browser='firefox', delay=10).get(url)
    result = re.search("https://.+m3u8", htmlfile.text)
    m3u8url = result[0]

    m3u8urlList = m3u8url.split('/')
    m3u8urlList.pop(-1)
    downloadurl = '/'.join(m3u8urlList)

    # 儲存 m3u8 file 至資料夾
    m3u8file = os.path.join(folderPath, dirName + '.m3u8')
    urllib.request.urlretrieve(m3u8url, m3u8file)

    # 得到 m3u8 file裡的 URI和 IV
    m3u8obj = m3u8.load(m3u8file)
    m3u8uri = ''
    m3u8iv = ''

    for key in m3u8obj.keys:
        if key:
            m3u8uri = key.uri
            m3u8iv = key.iv

    # 儲存 ts網址 in tsList
    tsList = []
    for seg in m3u8obj.segments:
        tsUrl = downloadurl + '/' + seg.uri
        tsList.append(tsUrl)

    # 有加密
    if m3u8uri:
        m3u8keyurl = downloadurl + '/' + m3u8uri  # 得到 key 的網址

        # 得到 key的內容
        response = requests.get(m3u8keyurl, headers=headers, timeout=10)
        contentKey = response.content

        vt = m3u8iv.replace("0x", "")[:16].encode()  # IV取前16位

        ci = AES.new(contentKey, AES.MODE_CBC, vt)  # 建構解碼器
    else:
        ci = ''

    # 刪除m3u8 file
    deleteM3u8(folderPath)

    # 開始爬蟲並下載mp4片段至資料夾
    prepareCrawl(ci, folderPath, tsList)

    # 合成mp4
    merge_mp4(folderPath, tsList)

    # 刪除子mp4
    deleteMp4(folderPath)

    # get cover
    get_cover(html_file=htmlfile, folder_path=folderPath)


def scrape(ci, folderPath, downloadList, urls):
    os.path.split(urls)
    fileName = urls.split('/')[-1][0:-3]
    saveName = os.path.join(folderPath, fileName + ".mp4")
    if os.path.exists(saveName):
        # 跳過已下載
        print('當前目標: {0} 已下載, 故跳過...剩餘 {1} 個'.format(
            urls.split('/')[-1], len(downloadList)))
        downloadList.remove(urls)
    else:
        response = requests.get(urls, headers=CONF['headers'], timeout=10)
        if response.status_code == 200:
            content_ts = response.content
            if ci:
                content_ts = ci.decrypt(content_ts)  # 解碼
            with open(saveName, 'ab') as f:
                f.write(content_ts)
                # 輸出進度
            downloadList.remove(urls)
        print('\r當前下載: {0} , 剩餘 {1} 個, status code: {2}'.format(
            urls.split('/')[-1], len(downloadList), response.status_code), end='', flush=True)


def prepareCrawl(ci, folderPath, tsList):
    downloadList = copy.deepcopy(tsList)
    # 開始時間
    start_time = time.time()
    print('開始下載 ' + str(len(downloadList)) + ' 個檔案..', end='')
    print('預計等待時間: {0:.2f} 分鐘 視影片長度與網路速度而定)'.format(len(downloadList) / 150))

    # 開始爬取
    startCrawl(ci, folderPath, downloadList)

    end_time = time.time()
    print('\n花費 {0:.2f} 分鐘 爬取完成 !'.format((end_time - start_time) / 60))


def startCrawl(ci, folderPath, downloadList):
    # 同時建立及啟用 20 個執行緒
    round = 0
    while (downloadList != []):
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            executor.map(partial(scrape, ci, folderPath,
                                 downloadList), downloadList)
        round += 1
        print(f', round {round}')
