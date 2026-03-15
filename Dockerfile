# ---- Base Image ----
# 使用輕量的 Python 3.11 映像檔
FROM python:3.11-slim

# ---- 系統套件安裝 ----
# 安裝 Chromium (headless browser) + ChromeDriver + FFmpeg
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# ---- 環境變數 ----
# 告知 Selenium 使用系統的 Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# ---- 工作目錄 ----
WORKDIR /app

# ---- 安裝 Python 依賴 ----
# 先複製 requirements.txt，利用 Docker 快取機制加速重建
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- 複製專案程式碼 ----
COPY . .

# ---- 掛載點 ----
# 下載的影片會存放到 /downloads，可透過 -v 掛載到本機
VOLUME ["/downloads"]

# 預設工作目錄切到下載資料夾
WORKDIR /downloads

# ---- 啟動指令 ----
# 執行主程式，透過環境變數 URL 傳入影片網址
# 用法: docker run -e URL="https://jable.tv/..." jable-downloader
CMD ["python", "/app/main.py"]
