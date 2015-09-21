# coding=utf-8
import re
import os
import json
import random

learned = {}

def init():
    pass


def get_answer(message):
    if 'se ti dico' in message:
        return jova_learn(message)
    else:
        return jova_answer_learned(message)


def jova_answer_learned(message):
    rx = r'jova,?\s(.+)$'
    m = re.match(rx, message)
    if not m:
        return None

    try:
        k = m.groups(1)[0]
        if k in learned:
            v = read_key(k)
            return v
    except:
        pass

    return None

def jova_learn(message):
    global learned

    rx = r'jova,?\sse ti (?:dico|dicono)\s([\w\s\?\!]+)\stu rispondi\s([\w\s\?\!]+)'
    m = re.match(rx, message)

    if not m:
        return None

    tokens = m.groups(1)
    if len(tokens) == 2:
        add_and_save(tokens[0], tokens[1])
        return 'OK'

    return None

def read_memory_file():
    global learned

    rel = os.path.dirname(__file__)
    with open( os.path.join(rel, 'learned.db'), encoding='utf-8' ) as fp:
        learned = json.load(fp)

def add_and_save(key, value):
    global learned

    if key not in learned:
        learned[key] = []
    if not value in learned[key]:
        learned[key].append(value)

    rel = os.path.dirname(__file__)

    with open( os.path.join(rel, 'learned.db'), 'wt', encoding='utf-8' ) as fp:
        json.dump(learned, fp)


def read_key(key):
    global learned
    if key in learned:
        vl = learned[key]
        if len(vl) == 0:
            return None
        if len(vl) == 1:
            return vl[0]

        return random.choice(vl)
    return None