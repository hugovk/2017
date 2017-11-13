#!/usr/bin/env python
# encoding: utf-8
"""
One 140 tweet about 280
One 280 tweet about 280
Repeat!

An entry for NaNoGemMo ("write code that writes a novel") 2017.

Thanks to  🎄xmas 🎅prumpky 🎄 for the idea!
https://twitter.com/survivorevan/status/928041592207818752

https://github.com/hugovk/NaNoGenMo/2017
https://github.com/NaNoGenMo/2017/issues/79

Notes:
https://github.com/sixohsix/twitter/blob/master/twitter/stream_example.py
https://dev.twitter.com/streaming/reference/post/statuses/filter
"""
from __future__ import print_function

import argparse
import random
import sys

import yaml
from twitter.oauth import OAuth
from twitter.stream import TwitterStream
from twitter.util import printNicely

# from pprint import pprint


TOGGLE_TYPES = ['toggle', 'short', 'long', 'random']


def load_yaml(filename):
    """
    File should contain:
    consumer_key: TODO_ENTER_YOURS
    consumer_secret: TODO_ENTER_YOURS
    access_token: TODO_ENTER_YOURS
    access_token_secret: TODO_ENTER_YOURS
    """
    with open(filename) as f:
        data = yaml.safe_load(f)
    if not set(data) >= {
            'access_token', 'access_token_secret',
            'consumer_key', 'consumer_secret'}:
        sys.exit("Twitter credentials missing from YAML: " + filename)
    return data


def intro():
    printNicely('<html><head><title>280</title>')
    printNicely('<link rel="stylesheet" href="280.css"></head><body>')
    printNicely('<h1>280</h1>')


def outro():
    printNicely("</body></html>")


def split_from(target, text):
    """Split text from the target to the end
    """
    pos = text.lower().find(target.lower())
    if pos > 0:
        return text[pos:]
    else:
        return None


def process_tweet(text, target, do_short):
    """Check it's ok and remove some stuff"""
    # print(len(text) > 140, len(text))

    if not text:
        return None

    if do_short and len(text) > 141:
        return None
    elif not do_short and len(text) <= 140:
        return None

    if (text.startswith("RT ") or
            "@" in text or
            "#" in text or
            "http" in text):
        return None

    text_lower = text.lower()
    if target.lower() not in text_lower:
        return None

    exclude = []
    if any(substr in text_lower for substr in exclude):
        return None
    # return split_from(target, text)

    return text


def do_html_things(text):
    text = text.replace("\n", "<br>")
    text = text.replace("  ", "&nbsp;&nbsp;")
    return text


def do_stuff(auth, query_args, stream_args, toggle):

    if toggle == "toggle":
        # We'll do a short tweet than a long one then a short...
        do_short = True
    else:
        # Only one size
        do_short = toggle == "short"

    word_count = 0
    tweet_count = 0

    stream = TwitterStream(auth=auth, **stream_args)
    tweet_iter = stream.statuses.filter(**query_args)

    # Iterate over the sample stream
    for tweet in tweet_iter:
        # You must test that your tweet has text. It might be a delete
        # or data message.
        if tweet is None:
            pass
            #             printNicely("-- None --")
            #         elif tweet is Timeout:
            #             printNicely("-- Timeout --")
            #         elif tweet is HeartbeatTimeout:
            #             printNicely("-- Heartbeat Timeout --")
            #         elif tweet is Hangup:
            #             printNicely("-- Hangup --")
        else:
            if "extended_tweet" in tweet:
                text = tweet["extended_tweet"]["full_text"]
            else:
                text = tweet.get("text")

            # pprint(tweet)
            processed = process_tweet(text, query_args['track'], do_short)
            if processed:
                tweet_count += 1
                word_count += len(processed.split())

                processed = do_html_things(processed)

                printNicely('<div id={0} class={1}><a href=#{0}>{2}</a></div>'.
                            format(tweet_count,
                                   "s" if do_short else "l",
                                   processed))
                # print(do_short)
                if toggle == "toggle":
                    do_short = not do_short  # toggle
                # print(do_short)

        if word_count > 56000:  # 280 * 200
            break

    printNicely("")


def parse_arguments():

    parser = argparse.ArgumentParser(description=__doc__ or "")

    parser.add_argument(
        '-y', '--yaml',
        # default='/Users/hugo/Dropbox/bin/data/citybikebot.yaml',
        default='citybikebot.yaml',
        help="YAML file location containing Twitter keys and secrets")
    parser.add_argument('-us', '--user-stream', action='store_true',
                        help='Connect to the user stream endpoint.')
    parser.add_argument('-ss', '--site-stream', action='store_true',
                        help='Connect to the site stream endpoint.')
    parser.add_argument('-to', '--timeout',
                        help='Timeout for the stream (seconds).')
    parser.add_argument('-ht', '--heartbeat-timeout',
                        help='Set heartbeat timeout.', default=90)
    parser.add_argument('-nb', '--no-block', action='store_true',
                        help='Set stream to non-blocking.')
    parser.add_argument('-tt', '--track-keywords',
                        default='280',
                        help='Search the stream for specific text.')
    parser.add_argument(
        '-t', '--toggle', choices=TOGGLE_TYPES, default='toggle',
        help='Whether to toggle short/long, show only short or long, '
             'or pick toggle/short/long at random')
    return parser.parse_args()


def main():
    args = parse_arguments()
    credentials = load_yaml(args.yaml)

    # When using Twitter stream you must authorise
    auth = OAuth(credentials['access_token'],
                 credentials['access_token_secret'],
                 credentials['consumer_key'],
                 credentials['consumer_secret'])

    # These arguments are optional:
    stream_args = dict(
        timeout=args.timeout,
        block=not args.no_block,
        heartbeat_timeout=args.heartbeat_timeout)

    query_args = dict()
    query_args['track'] = args.track_keywords

    if args.toggle == "random":
        # Any but 'random'
        args.toggle = random.choice(TOGGLE_TYPES[:-1])

    do_stuff(auth, query_args, stream_args, args.toggle)


if __name__ == '__main__':
    intro()
    main()
    outro()

# End of file
