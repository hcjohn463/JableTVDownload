# author: hcjohn463 ** Modify by Alfredo 26/Dec/2021
#!/usr/bin/env python
# coding: utf-8

import sys
import os
from args import *
from JableTVJob import JableTVJob
from gui import JableTVDownloadWindow
from config import *
""" global variable, Refer config.py for more detail 
    gui_mode    = 1
    save_folder = "download"
"""


def main(urls, dest=None):
    # 使用者輸入Jable網址
    if not urls or urls == '' : urls = input('輸入jable網址:')
    jjob = JableTVJob(urls, dest)
    if jjob.is_url_vaildate():
        jjob.start_download()
        print('下載完成!')


def gui_main(urls, dest):
    mainWnd = JableTVDownloadWindow(dest=dest, urls=urls)
    mainWnd.mainloop()
    mainWnd.cancel_download()


if __name__ == "__main__":
    url = ""
    parser = get_parser()
    args = parser.parse_args()
    if len(args.url) != 0:
        url = args.url
    elif args.random is True:
        url = av_recommand()

    if gui_mode == 1:
        gui_main(url, save_folder)
    else:
        main(url, save_folder)

    sys.exit(0)