import requests
from config import headers
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def movieLinks(url, proxy_url=None):
  links = []
  options = Options()
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  options.add_argument('--disable-extensions')
  options.add_argument('--headless')
  options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
  if proxy_url:
      options.add_argument(f'--proxy-server={proxy_url}')
  dr = webdriver.Chrome(options=options)
  dr.get(url)
  bs = BeautifulSoup(dr.page_source,"html.parser")
  a_tags = bs.select('div.img-box>a')
  print(a_tags)
  for a_tag in a_tags:
    links.append(a_tag['href'])
  print('获取到 {0} 個影片'.format(len(links)))
  print(links)
  return links

# %%
