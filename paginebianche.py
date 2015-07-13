import requests
import re
import sys

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
        print('requesting', r.url)
        return parse_response(r.text)
    except Exception as e:
        print('search failed', e)
        return None

def parse_response(text):
    name = ''
    address = ''
    phone = ''

    with open('wp_dump.html', 'wt', encoding='utf-8') as fp:
        fp.write(text)

    m = NAME_PATTERN.match(text)
    if m is not None and len(m.groups(1)) > 0:
        name = m.groups(1) [0]

    m = ADDRESS_PATTERN.match(text)
    if m is not None and len(m.groups(1)) > 0:
        address = m.groups(1) [0]

    m = PHONE_PATTERN.match(text)
    if m is not None and len(m.groups(1)) > 0:
        phone = m.groups(1) [0]


    soup = BeautifulSoup(text, 'html.parser')

    for d in soup.find_all("div", "vcard"):
        name = d.find('h2', 'rgs').a['title']
        phone = d.find("div", "tel").find("span", "value").text
        address = d.find("div", "address").text
        address = address[: address.index('|')].strip()

        yield wp_response(name, phone, address)

def test():
    name = sys.argv[1]
    loc = sys.argv[2]

    for o in search_wp(name, loc):
        print(o.__dict__)

if __name__ == "__main__":
    test()