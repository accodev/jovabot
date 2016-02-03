# coding=utf-8

import os
import importlib
from . import modules
import logging
import socket
import sys
import codecs
import telegram
from flask import Flask, request, abort
from botanio import botan
import atexit


# ordered by priority
ENABLED_MODULES = [
    'jovabot.modules.slash',
    'jovabot.modules.horoscope',
    'jovabot.modules.addressbook',
    'jovabot.modules.random',
    'jovabot.modules.learn',
    'jovabot.modules.lyrics'
]

LOADED_MODULES = []

bot = None
webapp = Flask(__name__)

if os.name != 'nt':
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout)],
                    level=logging.DEBUG,
                    format='%(asctime)-15s|%(levelname)-8s|'
                           '%(process)d|%(name)s|%(module)s|%(message)s')


def extract_token(filename):
    with open(filename, "r") as f:
        token = f.readline()
    return token.rstrip()


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
        # jova, I choose you!
        if 'jova' in message.text.lower() or '/' in message.text[0]:
            logging.info("[from {0}] [message ['{1}']]"
                         .format(str(message.from_user).encode('utf-8'),
                                 message.text.encode('utf-8')))
            chat_id = message.chat_id
            answer = jova_answer(message.text.lower())
            md = False
            if answer:
                if isinstance(answer, tuple):
                    if answer[1]:
                        if answer[1] == 'markdown':
                            md = True
                        answer = answer[0]
                else:
                    answer = jova_replace(answer)
                bot.sendChatAction(chat_id=chat_id,
                                   action=telegram.ChatAction.TYPING)
                if md:
                    parse_mode = telegram.ParseMode.MARKDOWN
                else:
                    parse_mode = None
                bot.sendMessage(chat_id=chat_id, text=answer,
                                reply_to_message_id=message.message_id,
                                parse_mode=parse_mode)
                # botanio stats tracking
                if webapp.config['BOTANIO_TOKEN']:
                    bt = botan.track(webapp.config['BOTANIO_TOKEN'],
                                     message.from_user, message.to_dict(),
                                     message.text)
                    if bt:
                        logging.info('botan.io track result: {0}'.format(bt))


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


@webapp.route('/telegram/<token>', methods=['POST'])
def telegram_hook(token):
    # why webapp.config['TOKEN'] doesn't work? fucking god
    if token == extract_token('key.token'):
        # retrieve the message in JSON and then transform it to Telegram object
        update = telegram.Update.de_json(request.get_json(force=True))

        # do something, man!
        try:
            jova_do_something(update.message)
        except:
            logging.exception('Something broke')
            # since telegram keeps on sending me the same request
            # I give them 200.
            return "ok", 200

        # jova return something ffs!
        return "ok", 200
    else:
        logging.critical('Token not accepted => token={0}'.format(token))
        abort(404)  # stop spamming my ass fucking telegram


@webapp.route('/')
def hello():
    return "jovabot was here!"


@webapp.route('/webhook/<command>')
def webhook(command):
    if command == 'set':
        res = webhook_set()
    elif command == 'delete':
        res = webhook_delete()
    else:
        res = 'unsupported command {0}'.format(command)
        abort(403)

    logging.info(res)

    return 'ok', 200


def webhook_set():
    webhook_url = socket.gethostname() + '/jovabot/telegram/' + \
                  extract_token('key.token')
    logging.debug(webhook_url)
    res = bot.setWebhook(webhook_url=webhook_url)
    return res


def webhook_delete():
    res = bot.setWebhook('')
    return res


def gtfo():
    logging.info('stopping')


def config():
    # fallback api token path - only used if JOVABOT_API_TOKEN is not found
    try:
        webapp.config['TOKEN_PATH'] = os.environ['JOVABOT_TELEGRAM_TOKEN_PATH']
    except OSError:
        logging.exception('failed to get JOVABOT_TELEGRAM_TOKEN_PATH')
        webapp.config['TOKEN_PATH'] = 0

    # telegram bot api token
    try:
        webapp.config['TOKEN'] = os.environ['JOVABOT_API_TOKEN']
    except OSError:
        logging.exception('failed to get JOVABOT_API_TOKEN')
        webapp.config['TOKEN'] = extract_token(webapp.config['TOKEN_PATH'])

    # creator chat id
    try:
        webapp.config['CREATOR_CHAT_ID'] = \
                                         os.environ['JOVABOT_CREATOR_CHAT_ID']
    except OSError:
        logging.exception('failed to get JOVABOT_CREATOR_CHAT_ID')
        webapp.config['CREATOR_CHAT_ID'] = 0

    # botan.io api token
    try:
        webapp.config['BOTANIO_TOKEN'] = os.environ['BOTANIO_API_TOKEN']
    except OSError:
        logging.exception('failed to get BOTANIO_API_TOKEN')
        webapp.config['BOTANIO_TOKEN'] = 0


@webapp.before_first_request
def main():
    logging.info("starting up")

    # load jovabot modules - crazy stuff
    load_modules()
    init_modules()

    # load configuration from env variables
    config()

    global bot
    bot = telegram.Bot(token=webapp.config['TOKEN'])

    if not bot:
        logging.error('bot is not valid')
        sys.exit(-1)

    logging.debug(webapp.config)

    atexit.register(gtfo)


if __name__ == '__main__':
    webapp.run()
