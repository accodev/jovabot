# coding=utf-8

from os import listdir
from os.path import isfile, join, dirname
import random

phrases_list = {}
conditions_list = {}

def init():
    read_jova_conditions()
    read_jova_phrases()


def get_answer(message):
    if 'help' in message:
        answer = jova_help()
    else:
        answer = jova_answer_conditions(message)
    return answer


def read_jova_phrases():
    global phrases_list

    print("start reading jova phrases...")

    rel = dirname(__file__)
    phrases_path = join(rel, 'phrases')

    onlyfiles = [f for f in listdir(phrases_path) if isfile(join(phrases_path, f))]
    for file in onlyfiles:
        with open(join(phrases_path, file), encoding="utf-8") as f:
            phrases_list[file] = f.read().splitlines()
            print("\t{0} read ->\tlines {1}".format(file, len(phrases_list[file])))


def read_jova_conditions():
    global conditions_list

    print("start reading jova conditions...")

    rel = dirname(__file__)
    cond_path = join(rel, 'conditions')

    onlyfiles = [f for f in listdir(cond_path) if isfile(join(cond_path, f))]
    for file in onlyfiles:
        with open(join(cond_path, file), encoding="utf-8") as f:
            conditions_list[file] = f.read().splitlines()
            print("\t{0} read ->\tlines {1}".format(file, len(conditions_list[file])))


def jova_help():
    plain_message = ""
    print("printing help...")
    for condition_file in conditions_list:
        print("printing conditions for {0} ->".format(condition_file))
        plain_message += condition_file + '\n'
        conditions = conditions_list.get(condition_file)
        for condition in conditions:
            print("\t{0}".format(condition))
            plain_message += '\t' + condition + '\n'
        plain_message += '--------\n'
    return plain_message, 'plain-text'

def jova_answer_conditions(message):
    plain_message = None
    for condition_file in conditions_list:
        cond = conditions_list.get(condition_file)
        if any(condition in message for condition in cond):
            phrase = phrases_list.get(condition_file)
            plain_message = random.choice(phrase)
            break
    return plain_message