import requests
from config import headers
from functools import partial
import concurrent.futures
import time

def scrape(ci,folderPath,urls):
    response = requests.get(urls, headers=headers, timeout=10)
    content_ts = response.content
    
    
    fileName = urls.split('/')[-1][0:-3]
    with open(folderPath + "\\" + fileName + ".mp4", 'ab') as f:
        if ci:
            f.write(ci.decrypt(content_ts))  # 解碼
        else:
            f.write(content_ts)
        f.close()

def startCrawl(ci,folderPath,tsList):
    #開始時間
    start_time = time.time()
    print('正在下載 ' + str(len(tsList)) + ' 個檔案.. (預計等待時間: 10 ~ 15 分 視影片長度與網路速度而定)')
 
    #同時建立及啟用 50個執行緒
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(partial(scrape,ci,folderPath), tsList)
 
    end_time = time.time()
    print(f"花費 {end_time - start_time} 秒爬取 {len(tsList)} 段 ts")