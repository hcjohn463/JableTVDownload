import requests
from config import headers
from functools import partial
import concurrent.futures
import time
import copy

def scrape(ci,folderPath,downloadList,urls):
    response = requests.get(urls, headers=headers, timeout=10)
    content_ts = response.content
    
    fileName = urls.split('/')[-1][0:-3]
    with open(folderPath + "\\" + fileName + ".mp4", 'ab') as f:
        if ci:
            f.write(ci.decrypt(content_ts))  # 解碼
        else:
            f.write(content_ts)
        #輸出進度
        print('已下載: {0} , 剩餘 {1} 個'.format(urls.split('/')[-1],len(downloadList)))
		
        downloadList.remove(urls)
        f.close()

def prepareCrawl(ci,folderPath,tsList):
    downloadList = copy.deepcopy(tsList)
    #開始時間
    start_time = time.time()
    print('開始下載 ' + str(len(downloadList)) + ' 個檔案..',end = '')
    print('預計等待時間: {0:.2f} 分鐘 視影片長度與網路速度而定)'.format(len(downloadList) / 150))

    #開始爬取
    startCrawl(ci,folderPath,downloadList)

    end_time = time.time()
    print('花費 {0:.2f} 分鐘 爬取完成 !'.format((end_time - start_time) / 60))

def startCrawl(ci,folderPath,downloadList):
    #同時建立及啟用 20個執行緒
    while(downloadList != []):
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(partial(scrape,ci,folderPath,downloadList), downloadList)
