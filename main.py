# coding: utf-8

import argparse
import model_crawler
from executor import process_subscription

parser = argparse.ArgumentParser(description="Jable TV Downloader")

sub_parser = parser.add_subparsers()

video_parser = sub_parser.add_parser("videos", help="download video by urls")
video_parser.add_argument("urls", metavar='N', type=int, nargs='+',
                          help="Jable TV URLs to download")

models_parser = sub_parser.add_parser("subscription",
                                      help="subscribe some topic(models or tags)/sync videos from subscriptions")

models_parser.add_argument("--add", type=str, default="",
                           help="add subscription by single url, support models/tags")
models_parser.add_argument("--get", action='store_true',
                           help="get current subscription")
models_parser.add_argument("--sync-videos", action='store_true',
                           help="download all subscription related videos")

models_parser.set_defaults(func=process_subscription)

# TODO:add retry.

if __name__ == '__main__':
    args = parser.parse_args()

    args.func(args)

