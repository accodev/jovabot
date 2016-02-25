# coding=utf-8

import atexit
import codecs
# noinspection PyUnresolvedReferences
import modules  # this import is for uwsgi
import importlib
import io
import logging
import os
import socket
import sys

import telegram
from flask import Flask, request

from botanio import botan

# ordered by priority
ENABLED_MODULES = [
    'modules.slash',
    'modules.horoscope',
    'modules.addressbook',
    'modules.lyrics',
    'modules.learn'
]

LOADED_MODULES = []

bot = None
webapp = Flask(__name__)

try:
    if os.name != 'nt':
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout)],
                        level=logging.DEBUG,
                        format='%(asctime)-15s|%(levelname)-8s|'
                               '%(process)d|%(name)s|%(module)s|%(funcName)s::%(lineno)d|%(message)s')
except (io.UnsupportedOperation, AttributeError) as e:
    print(e)


def extract_token(filename):
    with open(filename, "r") as f:
        token = f.readline()
    return token.rstrip()


def jovaize(s):
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
            logging.info('answer => [{}]'.format(answer))
            if answer and isinstance(answer, tuple) and answer[0]:
                formatting = answer[1]
                if 'jovaize' in formatting:
                    answer = jovaize(answer[0])
                else:
                    answer = answer[0]  # don't jovaize!
                bot.sendChatAction(chat_id=chat_id,
                                   action=telegram.ChatAction.TYPING)
                # markdown-formatted message?
                parse_mode = None
                if 'markdown' in formatting:
                    parse_mode = telegram.ParseMode.MARKDOWN
                # are we handling a sticker?
                if 'sticker' in formatting:
                    bot.sendSticker(chat_id=chat_id, reply_to_message_id=message.message_id, sticker=answer)
                else:
                    # otherwise, send a normal message
                    bot.sendMessage(chat_id=chat_id, text=answer,
                                    reply_to_message_id=message.message_id,
                                    parse_mode=parse_mode)
                # botan.io stats tracking
                if webapp.config['BOTANIO_TOKEN']:
                    bt = botan.track(webapp.config['BOTANIO_TOKEN'],
                                     message.from_user, message.to_dict(),
                                     message.text.lower())
                    if bt:
                        logging.info('botan.io track result: [{0}]'.format(bt))


def jova_answer(message):
    for mod in LOADED_MODULES:
        module_name = mod.__name__
        logging.info('querying {}...'.format(module_name))
        answer = mod.get_answer(message)
        if answer and isinstance(answer, tuple) and answer[0]:
            logging.info('answer from {}...'.format(module_name))
            return answer
        else:
            logging.info('no answer from {}...'.format(module_name))
    return None


def load_modules():
    for p in ENABLED_MODULES:
        mod = importlib.import_module(p, 'modules')
        if mod:
            LOADED_MODULES.append(mod)
            logging.info('loaded module {0}'.format(mod))


def init_modules():
    for m in LOADED_MODULES:
        m.init()


@webapp.route('/telegram/<token>', methods=['POST'])
def telegram_hook(token):
    my_token = str(webapp.config['TOKEN'])
    if token == my_token:
        update = telegram.Update.de_json(request.get_json(force=True))

        try:
            jova_do_something(update.message)
        except:
            logging.exception('Something broke')

        return "ok", 200
    else:
        logging.critical('Token not accepted => token={0} is not my_token={1}'.format(token, my_token))
        return "ko", 404


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
        return res, 403

    logging.info(res)

    return 'ok', 200


def webhook_set():
    webhook_url = '{0}/telegram/{1}'.format(str(webapp.config['BASE_ADDRESS']), str(webapp.config['TOKEN']))
    logging.debug(webhook_url)
    res = bot.setWebhook(webhook_url=webhook_url)
    return res


def webhook_delete():
    res = bot.setWebhook('')
    return res


@webapp.route('/channel-update/<secret>', methods=['POST'])
def channel_update(secret):
    logging.info('secret received is [{}]'.format(secret == webapp.config['CHANNEL_UPDATE_TOKEN']))
    if secret == webapp.config['CHANNEL_UPDATE_TOKEN']:
        logging.debug(request.data)
        update = request.get_json()
        logging.debug(update)
        if update:
            update_text = ''
            for c in update.get('commits'):
                update_text = c.get('message') + '\n'
            bot.sendMessage(chat_id='@jovanottibot_updates', text=update_text)
        return 'ok', 200    
    return 'ko', 403


def gtfo():
    logging.info('stopping')


def config():
    # fallback api token path - only used if JOVABOT_API_TOKEN is not found
    try:
        webapp.config['TOKEN_PATH'] = os.environ['JOVABOT_TELEGRAM_TOKEN_PATH']
    except (OSError, KeyError):
        logging.exception('failed to get JOVABOT_TELEGRAM_TOKEN_PATH')
        webapp.config['TOKEN_PATH'] = 0

    # telegram bot api token
    try:
        webapp.config['TOKEN'] = os.environ['JOVABOT_API_TOKEN']
    except (OSError, KeyError):
        logging.exception('failed to get JOVABOT_API_TOKEN')
        webapp.config['TOKEN'] = extract_token(webapp.config['TOKEN_PATH'])

    # creator chat id
    try:
        webapp.config['CREATOR_CHAT_ID'] = os.environ['JOVABOT_CREATOR_CHAT_ID']
    except (OSError, KeyError):
        logging.exception('failed to get JOVABOT_CREATOR_CHAT_ID')
        webapp.config['CREATOR_CHAT_ID'] = 0

    # botan.io api token
    try:
        webapp.config['BOTANIO_TOKEN'] = os.environ['BOTANIO_API_TOKEN']
    except (OSError, KeyError):
        logging.exception('failed to get BOTANIO_API_TOKEN')
        webapp.config['BOTANIO_TOKEN'] = 0

    # jovabot base address
    try:
        webapp.config['BASE_ADDRESS'] = 'https://' + socket.gethostname() + '/' + os.environ['JOVABOT_WEBAPP_NAME']
    except (OSError, KeyError):  # socket.gethostname() could possibly return an exception whose base class is OSError
        logging.exception('failed to set BASE_ADDRESS')
        webapp.config['BASE_ADDRESS'] = 0

    # channel update secret token
    try:
        webapp.config['CHANNEL_UPDATE_TOKEN'] = os.environ['CHANNEL_UPDATE_TOKEN']
    except (OSError, KeyError):
        logging.exception('failed to get CHANNEL_UPDATE_TOKEN')
        webapp.config['CHANNEL_UPDATE_TOKEN'] = 0


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
