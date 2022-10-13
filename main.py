# author: hcjohn463 ** Modify by Alfredo 26/Dec/2021
#!/usr/bin/env python
# coding: utf-8

from args import *
from JableTVJob import *
from gui import *

''' Running as GUI mode or console mode
    1      : GUI mode
    others : consoles mode   
    '''
''' Default folder to save the download files
    "" or None : same as the url's last stem,  ie:  "abc-001" for url = "https://jable.tv/videos/abc-001/"
    others : relative to the current folder, or an absolute path  
    '''
save_folder = "download"


if __name__ == "__main__":
    url = ""
    parser = get_parser()
    args = parser.parse_args()

    if len(args.url) != 0:
        url = args.url
    elif args.random is True:
        url = av_recommand()

    if args.nogui:
        consoles_main(url, save_folder)
    else:
        gui_main(url, save_folder)

    sys.exit(0)