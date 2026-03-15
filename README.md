# JableTVDownload

## 下載JableTV好幫手

每次看正要爽的時候就給我卡住轉圈圈  

直接下載到電腦看沒煩惱

---

## 🐳 Docker 一鍵啟動（推薦）

不需要手動安裝 ChromeDriver、FFmpeg、Python 環境，全部封裝在容器內。

### 前置需求
- 安裝 [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### 使用方法

```bash
# 1. 建立 image
docker build -t jable-downloader .

# 2. 執行（互動模式，下載影片存至本機 downloads 資料夾）
docker run -it -v D:\downloads:/downloads jable-downloader
```

---

## 💻 傳統安裝（Windows）

1. 請自行安裝 ffmpeg，裝完之後執行 INIT.bat 將會自動建置其餘環境。
2. 若收到可以執行 RUN.bat 之訊息，執行 RUN.bat 即可使用此神器。

### 1. 搭建並啟用虛擬環境

```
python -m venv jable
jable/Scripts/activate
```
![image](https://github.com/hcjohn463/JableDownload/blob/main/img/createVenv.PNG)

### 2. 下載所需套件

```
pip install -r requirements.txt
```

安裝 [FFmpeg] 用於轉檔

### 3. 執行程式

```
python main.py
```

### 4. 輸入影片網址
`https://jable.tv/videos/ipx-486/`  
![image](https://github.com/hcjohn463/JableDownload/blob/main/img/download2.PNG)

### 5. 等待下載與合成

下載和合成影片皆有即時進度條顯示：

```
⬇ 下載進度:  73%|██████████████░░░░░  | 1334/1827 [01:12<00:27, 18.2片段/s]
🎬 合成影片:  45%|█████████░░░░░░░░░░░ |  821/1827 [01:23<01:40]
```

### 6. 完成

![image](https://github.com/hcjohn463/JableDownload/blob/main/img/demo2.png)

### 如果覺得好用 再麻煩給個星星好評 謝謝!!

---

[FFmpeg]:<https://www.ffmpeg.org/>

---

## Argument Parser

```bash
python main.py -h
python main.py --random True       # 下載隨機熱門影片
python main.py --url <網址>         # 直接指定 URL
python main.py --all_urls <演員頁>  # 下載演員所有影片
```

---

## ☸️ Kubernetes 支援

`k8s/` 資料夾內含完整 Kubernetes 配置，可將下載任務部署為 K8s Job：

```bash
kubectl apply -f k8s/pvc.yaml        # 建立持久化儲存
kubectl apply -f k8s/configmap.yaml  # 套用設定
kubectl apply -f k8s/job.yaml        # 執行下載任務
kubectl get jobs                      # 查看任務狀態
```

---

## 📜 更新日誌 (Update Log)

| 版本 | 日期 | 內容 |
| :--- | :--- | :--- |
| **v2.0** | 2026/03/15 | 🐳 支援 Docker 容器化部署、☸️ K8s (Job/PVC/ConfigMap) 支援 |
| | | 📊 下載與合成加入 `tqdm` 即時進度條、🚀 優化合成與轉檔速度 |
| **v1.11**| 2023/04/19 | 🦕 新增 ffmpeg 自動轉檔 |
| **v1.10**| 2023/04/19 | 🏹 兼容 Ubuntu Server |
| **v1.9** | 2023/04/15 | 🦅 下載演員所有相關影片 |
| **v1.8** | 2022/01/25 | 🚗 下載結束後自動抓取封面 |
| **v1.7** | 2021/06/04 | 🐶 更改 m3u8 獲取方法 (正則表達式) |
| **v1.6** | 2021/05/28 | 🌏 支援 Unix 系統 (Mac, Linux 等) |
| **v1.5** | 2021/05/27 | 🍎 更新爬蟲網頁方法 |
| **v1.4** | 2021/05/20 | 🌳 修改編碼問題 |
| **v1.3** | 2021/05/06 | 🌈 增加下載進度提示、修改 Crypto 問題 |
| **v1.2** | 2021/05/05 | ⭐ 更新穩定版本 |
