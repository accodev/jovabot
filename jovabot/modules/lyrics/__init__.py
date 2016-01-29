# coding=utf-8

import logging
import random
import re
from os import listdir, mkdir
from os.path import isfile, join, dirname, exists

from whoosh.fields import Schema, TEXT
from whoosh.index import create_in
from whoosh.qparser import QueryParser

ix = None


def init():
    schema = Schema(title=TEXT(stored=True), path=TEXT(stored=True), content=TEXT)

    rel = dirname(__file__)
    index_dir = join(rel, 'index')

    global ix

    if not exists(index_dir):
        mkdir(index_dir)
    logging.debug('create lyrics index')
    ix = create_in(index_dir, schema)

    writer = ix.writer()

    lyrics_dir = join(rel, 'items')

    onlyfiles = [f for f in listdir(lyrics_dir) if isfile(join(lyrics_dir, f))]
    for file in onlyfiles:
        with open(join(lyrics_dir, file), encoding="utf-8") as f:
            cnt = f.read()
            link = cnt.splitlines()[0]

            writer.add_document(
                    title=file,
                    content=cnt,
                    path=link)

    writer.commit()


def get_answer(message):
    if '/' in message[0]:
        return None

    rx = r'jova,?\s(.+)$'
    m = re.match(rx, message)
    if not m or len(m.groups(1)) < 1:
        return None

    global ix

    search_terms = m.groups(1)[0]
    parser = QueryParser("content", ix.schema)
    qry = parser.parse(search_terms)

    with ix.searcher() as searcher:
        results = searcher.search(qry)
        result = None
        if len(results) == 0:
            return None
        if len(results) == 1:
            result = results[0]
        else:
            result = random.choice(results)

        if result is None or 'path' not in result:
            return None

        return result['path'], 'plain-text'

    return None
