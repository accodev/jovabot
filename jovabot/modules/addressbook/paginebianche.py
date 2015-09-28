import requests
import re
import sys
import logging

from bs4 import BeautifulSoup

#White pages url
WHITE_PAGES_URL="http://www.paginebianche.it/execute.cgi"

class wp_response(object):
    def __init__(self, name, tel, addr):
        self.name = name
        self.tel = tel
        self.addr = addr

def search_wp(name, location):
    payload = {'btt': '1', 'qs': name, 'dv': location}

    try:
        r = requests.get(WHITE_PAGES_URL, params=payload)
        logging.debug('requesting', r.url)
        return parse_response(r.text)
    except Exception as e:
        logging.debug('search failed', e)
        return None

def parse_response(text):
    name = ''
    address = ''
    phone = ''

    #with open('wp_dump.html', 'wt', encoding='utf-8') as fp:
    #    fp.write(text)

    soup = BeautifulSoup(text, 'html.parser')

    for d in soup.find_all("div", "vcard"):
        name = d.find('h2', 'rgs').a['title']
        phone = d.find("div", "tel").find("span", "value").text
        address = d.find("div", "address").div.text
        #address = address[: address.index('|')].strip()

        yield wp_response(name, phone, address)

def test():
    name = sys.argv[1]
    loc = sys.argv[2]

    for o in search_wp(name, loc):
        logging.debug(o.__dict__)

if __name__ == "__main__":
    test()