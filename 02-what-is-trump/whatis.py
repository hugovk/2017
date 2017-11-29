#!/usr/bin/env python
# encoding: utf-8
"""
What is Trump? A variation on last year's Dear Santa, a chapter
crowdsourced from each US state, populated from a Twitter search.

An entry for NaNoGemMo ("write code that writes a novel") 2017.

https://github.com/hugovk/NaNogenMo/2017
https://github.com/NaNoGenMo/2017/issues/79

Notes:
https://github.com/sixohsix/twitter/blob/master/twitter/stream_example.py
https://dev.twitter.com/streaming/reference/post/statuses/filter
"""
from __future__ import print_function

import argparse
import sys

import yaml
from twitter.oauth import OAuth
from twitter.stream import TwitterStream  # , Timeout, HeartbeatTimeout, Hangup
from twitter.util import printNicely

from six.moves.html_parser import HTMLParser  # pip install six

from continental_usa_states_bb import STATES


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


def split_from(target, text):
    """Split text from the target to the end
    """
    pos = text.lower().find(target.lower())
    if pos > 0:
        return text[pos:]
    else:
        return None


def process_tweet(text, target):
    """Check it's ok and remove some stuff"""
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


def do_state(state, auth, query_args, stream_args, htmlparser):

    word_count = 0

    if state:
        name = state['display_name']
        print()
        print(name)
        print("-" * len(name))

        word_count = len(name.split())

        bbox = state['boundingbox']
        bbox = ",".join([bbox[2], bbox[0], bbox[3], bbox[1]])  # SW first
        query_args['locations'] = bbox

    stream = TwitterStream(auth=auth, **stream_args)
    tweet_iter = stream.statuses.filter(**query_args)

    # Iterate over the sample stream.
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
        elif tweet.get('text'):
            processed = process_tweet(tweet['text'], query_args['track'])
            if processed:
                # &amp; -> & etc.
                processed = htmlparser.unescape(processed)
                printNicely(processed)
                word_count += len(processed.split())

        if state:
            if word_count > 1100:
                break
        else:
            if word_count > 51000:
                break

    print()


def parse_arguments():

    parser = argparse.ArgumentParser(description=__doc__ or "")

    parser.add_argument(
        '-y', '--yaml', default='whatis.yaml',
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
                        default='trump is',
                        help='Search the stream for specific text.')
    parser.add_argument('-ns', '--no-states', action='store_true',
                        help="Don't do states.")
    return parser.parse_args()


def main():
    args = parse_arguments()
    htmlparser = HTMLParser()

    credentials = load_yaml(args.yaml)

    # When using Twitter stream you must authorize
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

    if args.no_states:
        do_state(None, auth, query_args, stream_args, htmlparser)
    else:
        for state in STATES:
            do_state(state, auth, query_args, stream_args, htmlparser)


if __name__ == '__main__':
    main()

# End of file
