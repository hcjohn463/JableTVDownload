import config
import model_crawler
from config import CONF


def process_subscription(args):
    if args.add:
        input_url = args.add
        model_crawler.input_url_validator(input_url)
        name, _ = model_crawler.get_model_names_and_last_page_num(input_url)
        subs = {'url': input_url, 'name': name}
        if subs not in CONF['subscriptions']:
            CONF['subscriptions'].append(subs)
            config.update_config(CONF)
            print("add subscription success.")
            print(subs)
        else:
            print("subscription already exists.")
        # print(model_crawler.get_all_video_links(input_url))
    elif args.get:
        print("current subscriptions:\n")
        print(CONF['subscriptions'])
    elif args.sync_videos:
        raise NotImplemented
