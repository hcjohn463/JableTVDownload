chcp 65001

@echo off
SET VENV_PATH=.\jable

REM 檢查虛擬環境是否存在
IF EXIST "%VENV_PATH%\Scripts\activate.bat" (
    ECHO 虛擬環境已經存在。
) ELSE (
    ECHO 虛擬環境不存在，正在創建...
    python -m venv jable
    ECHO 虛擬環境創建完成。
)

REM 激活虛擬環境
CALL "%VENV_PATH%\Scripts\activate"

pip3 install -r requirements.txt

REM 檢查chromedriver.exe是否存在
IF EXIST "chromedriver.exe" (
    ECHO chromedriver已存在。
) ELSE (
    ECHO chromedriver不存在，正在下載...
    python getchromedriver.py
)

REM 檢查FFmpeg是否安裝
where ffmpeg >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    ECHO FFmpeg已安裝，你可以執行RUN.bat了
) ELSE (
    ECHO FFmpeg未安裝，請先安裝FFmpeg
)


pause
