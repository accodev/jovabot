# coding=utf-8

import os
import datetime
import importlib
from . import modules
import logging

import telegram
from flask import Flask, request


# ordered by priority
ENABLED_MODULES = [
    'jovabot.modules.horoscope',
    'jovabot.modules.addressbook',
    'jovabot.modules.learn',
    'jovabot.modules.random',
    'jovabot.modules.lyrics'
]

LOADED_MODULES = []

bot = None

webapp = Flask(__name__)

logging.basicConfig(filename='jovabot.log', level=logging.DEBUG)


def extract_token(filename):
    with open(filename, "r") as f:
        token = f.readline()
    return token


def jova_replace(s):
    return s \
        .replace('s', 'f') \
        .replace('x', 'f') \
        .replace('z', 'f') \
        .replace('S', 'F') \
        .replace('X', 'F') \
        .replace('Z', 'F')


def jova_do_something(message):
    if message.text:
        if 'jova' in message.text.lower():  # invocato il dio supremo
            logging.info(
                "[{0}] [from {1}] [message ['{2}']]".format(datetime.datetime.now().isoformat(), message.from_user,
                                                            message.text))
            chat_id = message.chat.id
            answer = jova_answer(message.text.lower())
            if answer:
                if isinstance(answer, tuple):
                    if answer[1]:
                        answer = jova_replace(answer[0])
                    else:
                        answer = answer[0]
                else:
                    answer = jova_replace(answer)
                bot.sendChatAction(chat_id, telegram.ChatAction.TYPING)
                bot.sendMessage(chat_id, answer, reply_to_message_id=message.message_id)


def jova_answer(message):
    global LOADED_MODULES

    for mod in LOADED_MODULES:
        answer = mod.get_answer(message)
        if answer:
            return answer
    return None


def load_modules():
    global LOADED_MODULES
    global ENABLED_MODULES

    for p in ENABLED_MODULES:
        mod = importlib.import_module(p, 'jovabot.modules')
        if mod:
            LOADED_MODULES.append(mod)
            logging.info('loaded module {0}'.format(mod))


def init_modules():
    global LOADED_MODULES
    for m in LOADED_MODULES:
        m.init()


@webapp.route('/telegram', methods=['POST'])
def telegram_hook():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True))

    # do something, man!
    jova_do_something(update.message)


@webapp.route('/')
def hello():
    return "hello!"


@webapp.route('/init_webhook')
def init_webhook():
    with open('/etc/nginx/ssl/nginx.crt') as c:
        cer = c.read()
    res = bot.setWebhook(webhook_url='https://acco.duckdns.org/telegram', certificate=cer)
    logging.info(res)

    return 'ok'


@webapp.before_first_request
def main():
    pid = str(os.getpid())
    pidfile = "jovabot.pid"

    with open(pidfile, "w") as p:
        p.write(pid)

    load_modules()
    init_modules()

    global bot
    bot = telegram.Bot(token=extract_token("key.token"))


if __name__ == '__main__':
    webapp.run()
