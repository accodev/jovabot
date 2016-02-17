# coding=utf-8
from . import paginebianche
import re


def init():
    pass


def get_answer(message):
    if 'cerca' in message and '/' not in message[0]:
        return jova_paginebianche(message), 'jovaize'
    return None


def jova_paginebianche(message):
    rx = r'jova,?\s(?:cercami|trovami|cerca|trova|paginebianche)' \
          '\s([\w\s]+)\s(?:a|ad|in)\s([\w\s]+)'
    m = re.match(rx, message)

    if not m:
        return None

    tokens = m.groups(1)
    if len(tokens) == 2:

        found = False
        out = 'ho trovato:\n'
        for o in paginebianche.search_wp(tokens[0], tokens[1]):
            out += "{0} tel: {1}\n{2}\n\n".format(o.name, o.tel, o.addr)
            found = True

        if not found:
            return "non ho trovato nessuno"

        return out

    return None
