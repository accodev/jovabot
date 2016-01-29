#!/usr/bin/python

import feedparser
import sys
import logging

FEED_URL = 'http://it.horoscopofree.com/rss/horoscopofree-it.rss'


def find_sign(feed, sign):
    try:
        return [x for x in feed.entries if x.title.lower() == sign][0]
    except:
        return None


def strip_href(o):
    s = o.description
    href_start = s.index('<a')
    return s[0:href_start]


class oroscopy(object):
    def __init__(self, sign, text):
        self.sign = sign
        self.text = text


def get(signes):
    f = feedparser.parse(FEED_URL)
    for s in signes:
        try:
            o = oroscopy(s, strip_href(find_sign(f, s)))
            yield o
        except:
            continue


# TEST ONLY
def main():
    try:
        sign = sys.argv[1]
        for o in get([sign]):
            logging.debug('{0}\n{1}\n'.format(o.sign, o.text))
    except Exception as e:
        logging.exception('oroscopo non trovato', e)


if __name__ == '__main__':
    main()
