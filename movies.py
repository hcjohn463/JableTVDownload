# In[0]:
import requests
from config import headers
from bs4 import BeautifulSoup

def movieLinks(url):
  res = requests.get(url, headers=headers, timeout=10)
  links = []
  if res.status_code == 200:
    content = res.content
    soup = BeautifulSoup(content, 'html.parser')
    a_tags = soup.select('div.img-box>a')
    for a_tag in a_tags:
        links.append(a_tag['href'])
  print('获取到 {0} 個影片'.format(len(links)))
  return links
