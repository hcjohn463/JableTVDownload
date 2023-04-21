import requests
import os
from bs4 import BeautifulSoup


def getCover(html_file, folder_path):
  # get cover
  soup = BeautifulSoup(html_file, "html.parser")
  cover_name = f"{os.path.basename(folder_path)}.jpg"
  cover_path = os.path.join(folder_path, cover_name)
  for meta in soup.find_all("meta"):
      meta_content = meta.get("content")
      if not meta_content:
          continue
      if "preview.jpg" not in meta_content:
          continue
      try:
          r = requests.get(meta_content)
          with open(cover_path, "wb") as cover_fh:
              r.raw.decode_content = True
              for chunk in r.iter_content(chunk_size=1024):
                  if chunk:
                      cover_fh.write(chunk)
      except Exception as e:
          print(f"unable to download cover: {e}")

  print(f"cover downloaded as {cover_name}")
