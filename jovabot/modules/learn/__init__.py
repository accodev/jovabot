# coding=utf-8
import json
import logging
import random
import re
from fuzzywuzzy import process

try:
    import pymongo

    HAVE_MONGO_DB = True
except:
    HAVE_MONGO_DB = False

try:
    import redis

    HAVE_REDIS = True
except:
    HAVE_REDIS = False

try:
    from uwsgi import sharedarea_read, sharedarea_write, \
                      sharedarea_write32, sharedarea_read32

    HAVE_SHARED_AREA = True
except:
    HAVE_SHARED_AREA = False


class JovaLearnNone(object):
    def __init__(self):
        pass

    def jova_learn(self, tit, tat):
        return False

    def jova_keys(self):
        return None

    def jova_answer_for_key(self, key):
        return None

    def clear(self):
        pass


class JovaLearnSharedMemory(object):
    def __init__(self):
        self.data = {}
        self.id = random.randint(10, 20)

    def jova_learn(self, tit, tat):
        if tit in self.data:
            self.data[tit].append(tat)
        else:
            self.data[tit] = [tat]
        return self.write_shared_area()

    def jova_keys(self):
        self.read_shared_area()
        return self.data

    def jova_answer_for_key(self, key):
        self.read_shared_area()
        if key in self.data:
            return random.choice(self.data[key])
        return None

    def write_shared_area(self):
        payload = json.dumps(self.data)

        # write payload len
        sharedarea_write32(self.id, 0, len(payload))

        # write payload
        sharedarea_write(self.id, 4, payload)

    def read_shared_area(self):
        # read payload len
        len_ = sharedarea_read32(self.id, 0)

        # read payload
        if len_ > 0:
            json_ = sharedarea_read(self.id, 4, len_)
            self.data = json.loads(json_)
        else:
            self.data = {}

    def clear(self):
        # write zero len
        sharedarea_write32(self.id, 0, 0)

    def get_all(self, key):
        self.read_shared_area()
        if key in self.data:
            return self.data[key]
        return []


class JovaLearnMongoDb(object):
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db = self.client.jovabot
        self.tit_for_tat = self.db.tit_for_tat

    def jova_learn(self, tit, tat):
        tit_tat = {"key": tit, "text": tat}
        self.tit_for_tat.insert_one(tit_tat)

    def jova_keys(self):
        return self.tit_for_tat.distinct("key")

    def jova_answer_for_key(self, key):
        all_ = self.get_all(key)
        if len(all_):
            return random.choice(self.get_all(key))
        return None

    def clear(self):
        self.tit_for_tat.drop()

    def get_all(self, key):
        return [x['text'] for x in self.tit_for_tat.find({"key": key})]


class JovaLearnRedis(object):
    def __init__(self):
        self.client = redis.Redis('localhost')

    def jova_learn(self, tit, tat):
        self.client.sadd(tit, tat)

    def jova_keys(self):
        pass

    def jova_answer_for_key(self, key):
        return self.client.srandmember(key)

    def clear(self):
        self.client.flushdb()

    def get_all(self, key):
        return self.client.smembers(key)


impl = None


def init():
    global impl

    if HAVE_MONGO_DB:
        impl = JovaLearnMongoDb()
        logging.debug('learn module uses mongo-db backend')
    elif HAVE_REDIS:
        impl = JovaLearnRedis()
        logging.debug('learn module uses redis backend')
    elif HAVE_SHARED_AREA:
        impl = JovaLearnSharedMemory()
        logging.debug('learn module uses uwsgi shared area backend')
    else:
        impl = JovaLearnNone()
        logging.debug('learn module not available')


def get_answer(message):
    if message.startswith('/'):
        return None

    if 'se ti dico' in message and '/':
        return jova_learn(message)
    else:
        return jova_answer_learned(message), 'jovaize'


def jova_answer_learned(message):
    rx = r'jova,?\s(.+)$'
    m = re.match(rx, message)
    if not m:
        return None
    try:
        k = m.groups(1)[0]
        return jova_fuzzy_answer(k)
    except:
        logging.exception('jova_answer_learned error')

    return None


def jova_learn(message):
    rx = r'jova,?\sse ti (?:dico|dicono)\s([\w\s\?\!\']+)\stu rispondi\s([\w\s\?\!\']+)'
    m = re.match(rx, message)

    if not m:
        return None

    tokens = m.groups(1)
    if len(tokens) == 2 and len(tokens[0]) > 3:
        try:
            logging.info('learning to answer {0} to the trigger {1}'
                         .format(tokens[1], tokens[0]))
            impl.jova_learn(tokens[0], tokens[1])
            # file_id = BQADBAADkgADwThpBr2dKDwqptsXAg - SAITAMA_OK
            return 'BQADBAADkgADwThpBr2dKDwqptsXAg', 'sticker'
        except:
            logging.exception('jova_learn error')
    return None


def jova_fuzzy_answer(key):
    keys = impl.jova_keys()
    choosen_key = process.extractOne(key, keys)
    if choosen_key:
        if choosen_key[1] < 80:
            logging.warning('found a key which is **almost** the requested[{0}] - found[{1}]'
                            .format(key, choosen_key[0]))
        return impl.jova_answer_for_key(choosen_key[0])
    return None


def clear():
    impl.clear()


def get_all(key):
    return impl.get_all(key)
