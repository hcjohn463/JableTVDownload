headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
}

proxy = None

def set_proxy(proxy_url):
    global proxy
    proxy = proxy_url

def get_proxy_dict():
    if proxy:
        return {
            'http': proxy,
            'https': proxy
        }
    return None
