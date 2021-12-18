headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
}

''' Running as GUI mode or console mode
    1      : GUI mode
    others : console mode   
    '''
gui_mode = 1

''' Default folder to save the download files
    None   : same as the url's last stem,  ie:  "ghi" for url = "https://abc/def/ghi/"
    others : relative to the current folder, or an absolute path  
    '''
save_folder = "download"
