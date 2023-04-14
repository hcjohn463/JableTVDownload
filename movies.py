# In[0]:
import requests
from config import headers
from bs4 import BeautifulSoup
from selenium import webdriver


def movieLinks(url):
  links = []
  dr = webdriver.Chrome()
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
