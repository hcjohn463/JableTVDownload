import json


def get_config(conf_path='./config.json'):
    with open(conf_path, 'r', encoding='utf8') as f:
        return json.load(f)


def update_config(conf, conf_path='./config.json'):
    with open(conf_path, 'w', encoding='utf8') as f:
        json.dump(conf, f, indent=4, ensure_ascii=False)


CONF = get_config()
headers = CONF["headers"]
