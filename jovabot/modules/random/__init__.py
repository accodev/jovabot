# coding=utf-8

from os import listdir
from os.path import isfile, join, dirname
import random
import logging

phrases_list = {}
conditions_list = {}


def init():
    read_jova_conditions()
    read_jova_phrases()


def get_answer(message):
    if '/' not in message[0]:
        if 'a cosa rispondi' in message:
            answer = jova_help()
        else:
            answer = jova_answer_conditions(message)
    else:
        answer = None
    return answer


def read_jova_phrases():
    global phrases_list

    logging.info("reading phrases...")

    rel = dirname(__file__)
    phrases_path = join(rel, 'phrases')

    onlyfiles = \
        [f for f in listdir(phrases_path) if isfile(join(phrases_path, f))]
    for file in onlyfiles:
        with open(join(phrases_path, file), encoding="utf-8") as f:
            phrases_list[file] = f.read().splitlines()


def read_jova_conditions():
    global conditions_list

    logging.info("reading conditions...")

    rel = dirname(__file__)
    cond_path = join(rel, 'conditions')

    onlyfiles = [f for f in listdir(cond_path) if isfile(join(cond_path, f))]
    for file in onlyfiles:
        with open(join(cond_path, file), encoding="utf-8") as f:
            conditions_list[file] = f.read().splitlines()


def jova_help():
    plain_message = ""
    logging.debug("help requested")
    for condition_file in conditions_list:
        logging.debug("printing conditions for {0} ->".format(condition_file))
        plain_message += '*' + condition_file.upper() + '*\n'
        conditions = conditions_list.get(condition_file)
        for condition in conditions:
            plain_message += '\t' + condition + '\n'
        plain_message += '\n'
    return plain_message, 'markdown'


def jova_answer_conditions(message):
    plain_message = None
    for condition_file in conditions_list:
        cond = conditions_list.get(condition_file)
        if any(condition in message for condition in cond):
            phrase = phrases_list.get(condition_file)
            plain_message = random.choice(phrase)
            break
    return plain_message
