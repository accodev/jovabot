# coding=utf-8
from . import oroscopy
import logging


def init():
    pass


def get_answer(message):
    if 'oroscopo' in message and not message.startswith('/'):
        return jova_oroscopo(message), 'jovaize'
    return None


def jova_oroscopo(message):
    signes = [
        'ariete', 'toro', 'gemelli',
        'cancro', 'leone', 'vergine',
        'bilancia', 'scorpione', 'sagittario',
        'capricorno', 'acquario', 'pesci']

    found_signes = [x for x in signes if x in message]

    logging.debug("oroscopo richiesto per i segni: {0}".format(found_signes))

    if not len(found_signes):
        return None

    found = False
    out = ''
    for o in oroscopy.get(found_signes):
        out += '{0}\n{1}\n'.format(o.sign.upper(), o.text)
        found = True

    if not found:
        return None

    return out
