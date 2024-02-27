import requests
from bs4 import BeautifulSoup
import zipfile
import shutil
import os

def get_chromedriver_version():
    url = 'https://googlechromelabs.github.io/chrome-for-testing/'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        formatted_html = soup.prettify()
        
        # print(formatted_html)

        tr_tags = soup.find_all('tr', class_='status-ok')
        for tr in tr_tags:
            if tr.find('a', string="Stable"):
                version_code = tr.find('code').text.strip()
                print(version_code)
                break
        return version_code
    else:
        print("Fail, Code:", response.status_code)

def download_chromedriver(download_link):
    url = download_link
    response = requests.get(url)

    if response.status_code == 200:
        with open('chromedriver.zip', 'wb') as file:
            file.write(response.content)
        print("success!")
    else:
        print("Fail, Code:", response.status_code)

def unzip_chromedriver():
    with zipfile.ZipFile('chromedriver.zip', 'r') as zip_ref:
        zip_ref.extractall('./')

chromedriver_version = get_chromedriver_version()
download_link = f"https://storage.googleapis.com/chrome-for-testing-public/{chromedriver_version}/win64/chromedriver-win64.zip"
download_chromedriver(download_link)
unzip_chromedriver()

# move chromedriver to the root directory
file_source = "chromedriver-win64/chromedriver.exe"
file_destination = "./"
shutil.move(file_source, file_destination)

# clean up
shutil.rmtree('chromedriver-win64')
os.remove("chromedriver.zip")