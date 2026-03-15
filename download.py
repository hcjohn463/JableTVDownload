
import requests
import os
import re
import urllib.request
import m3u8
from config import headers
from crawler import prepareCrawl
from merge import mergeMp4
from encode import ffmpegEncode
from delete import deleteM3u8, deleteMp4
from cover import getCover
from args import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def download(url):

  print('正在下載影片: ' + url)
  # 建立番號資料夾
  urlSplit = url.split('/')
  dirName = urlSplit[-2]
  if os.path.exists(f'{dirName}/{dirName}.mp4'):
    print('番號資料夾已存在, 跳過...')
    return
  if not os.path.exists(dirName):
      os.makedirs(dirName)
  folderPath = os.path.join(os.getcwd(), dirName)
  
  #配置Selenium參數
  options = Options()
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  options.add_argument('--disable-extensions')
  options.add_argument('--headless')
  options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
  dr = webdriver.Chrome(options=options)
  dr.get(url)
  result = re.search("https://.+m3u8", dr.page_source)
  print(f'result: {result}')
  m3u8url = result[0]
  print(f'm3u8url: {m3u8url}')

  # 得到 m3u8 網址
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
      m3u8keyurl = downloadurl + '/' + m3u8uri
      response = requests.get(m3u8keyurl, headers=headers, timeout=10)
      contentKey = response.content
      vt = m3u8iv.replace("0x", "")[:16].encode()  # IV 取前 16 位
      # ✅ 改存 dict，讓每個執行緒自行建立 AES cipher（避免 Race Condition）
      ci_params = {'key': contentKey, 'iv': vt}
  else:
      ci_params = None

  # 刪除m3u8 file
  deleteM3u8(folderPath)

  # 開始爬蟲並下載mp4片段至資料夾
  prepareCrawl(ci_params, folderPath, tsList)

  # 合成 mp4（Python 二進位串接）
  mergeMp4(folderPath, tsList)

  # 轉檔：-c copy + faststart，讓播放器可邊下載邊播
  ffmpegEncode(folderPath, dirName, 1)

  # 刪除子mp4
  deleteMp4(folderPath)

  # 取得封面
  getCover(html_file=dr.page_source, folder_path=folderPath)
