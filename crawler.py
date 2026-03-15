import os
import requests
from config import headers
from functools import partial
import concurrent.futures
import time
import copy
import threading
from tqdm import tqdm
from Crypto.Cipher import AES


def scrape(ci_params, folderPath, pbar, lock, session, urls):
    """
    ci_params: dict 包含 key 和 iv
    session: requests.Session 用於連線複用，加快下載
    """
    fileName = urls.split('/')[-1][0:-3]
    saveName = os.path.join(folderPath, fileName + ".mp4")

    # 如果檔案已存在，進度條不重複更新（因為 startCrawl 已過濾）
    try:
        response = session.get(urls, headers=headers, timeout=30)
        if response.status_code == 200:
            content_ts = response.content
            if ci_params:
                ci = AES.new(ci_params['key'], AES.MODE_CBC, ci_params['iv'])
                content_ts = ci.decrypt(content_ts)
            with open(saveName, 'ab') as f:
                f.write(content_ts)
            
            # ✅ 只有成功下載才更新進度條
            with lock:
                pbar.update(1)
            return True
    except Exception:
        pass
    
    return False


def measureSpeed(tsList, sample_count=3):
    """並行測速，減少啟動延遲"""
    sample = tsList[:sample_count]
    times = []
    sizes = []

    def _fetch(url):
        t0 = time.time()
        try:
            with requests.Session() as s:
                response = s.get(url, headers=headers, timeout=15)
            size_kb = len(response.content) / 1024
            return time.time() - t0, size_kb
        except Exception:
            return 2.0, 0

    print(f'正在測試您的網速（抽樣 {sample_count} 個片段，並行）...', end='', flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=sample_count) as ex:
        results = list(ex.map(_fetch, sample))
    times = [r[0] for r in results]
    sizes = [r[1] for r in results]
    avg_sec = sum(times) / len(times) if times else 2.0
    avg_speed_kb = sum(sizes) / sum(times) if sum(times) > 0 else 0
    print(f' 平均網速: {avg_speed_kb:.0f} KB/s ({avg_sec:.2f} 秒/片段)')
    return avg_sec, avg_speed_kb


def prepareCrawl(ci_params, folderPath, tsList):
    downloadList = copy.deepcopy(tsList)
    total = len(downloadList)

    avg_sec_per_ts, avg_speed_kb = measureSpeed(tsList)
    # 提高並發：上限 32、下限 8，公式放寬以善用頻寬
    workers = min(32, max(8, int(avg_speed_kb / 200)))
    print(f'開始下載 {total} 個片段（使用 {workers} 個執行緒）')

    estimated_sec = (total * avg_sec_per_ts) / workers
    est_m = int(estimated_sec // 60)
    est_s = int(estimated_sec % 60)
    print(f'預計等待時間: {est_m} 分 {est_s} 秒（依據您的實際網速估算）')

    start_time = time.time()
    startCrawl(ci_params, folderPath, downloadList, total, workers)
    end_time = time.time()

    actual_sec = end_time - start_time
    act_m = int(actual_sec // 60)
    act_s = int(actual_sec % 60)
    print(f'\n花費 {act_m} 分 {act_s} 秒 爬取完成！')


def startCrawl(ci_params, folderPath, downloadList, total, workers):
    lock = threading.Lock()
    round_num = 0
    # 連線池：同一 host 複用 TCP，減少握手指數
    with requests.Session() as session:
        _run_crawl(ci_params, folderPath, downloadList, total, workers, lock, session)


def _run_crawl(ci_params, folderPath, downloadList, total, workers, lock, session):
    round_num = 0
    # ✅ 初始化進度條，總數固定為 total
    with tqdm(total=total, unit='片段', desc='⬇ 下載進度',
              bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]',
              dynamic_ncols=True, colour='cyan') as pbar:

        # 先檢查已經下載過的，更新進度條初始值
        existing_count = 0
        initial_list = list(downloadList)
        for url in initial_list:
            file_ts = url.split('/')[-1][0:-3] + '.mp4'
            if os.path.exists(os.path.join(folderPath, file_ts)):
                existing_count += 1
                downloadList.remove(url)
        
        pbar.update(existing_count)

        while downloadList:
            round_num += 1
            batch = list(downloadList)

            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
                # scrape 使用 session 連線複用，加快下載
                executor.map(partial(scrape, ci_params, folderPath, pbar, lock, session), batch)

            # 更新剩餘清單：移除已成功下載的
            new_download_list = []
            for url in downloadList:
                file_ts = url.split('/')[-1][0:-3] + '.mp4'
                if not os.path.exists(os.path.join(folderPath, file_ts)):
                    new_download_list.append(url)
            
            downloadList = new_download_list

            if downloadList:
                tqdm.write(f'⚠ Round {round_num} 結束，還有 {len(downloadList)} 個片段失敗，準備重試...')
                time.sleep(1) # 短暫休息避免被封鎖
