# coding=utf-8
import re
from . import oroscopy
import logging


def init():
    pass


def get_answer(message):
    if 'oroscopo' in message and '/' not in message[0]:
        return jova_oroscopo(message)
    return None


def jova_oroscopo(message):
    signes = [
        'ariete', 'toro', 'gemelli',
        'cancro', 'leone', 'vergine',
        'bilancia', 'scorpione', 'sagittario',
        'capricorno', 'acquario', 'pesci']

    found_signes = [x for x in signes if x in message]

    logging.debug("oroscopo richiesto per i segni: ", found_signes)

    if not len(found_signes):
        return None

    found = False
    out = ''
    for o in oroscopy.get(found_signes):
        out += '{0}\n{1}\n'.format(o.sign, o.text)
        found = True

    if not found:
        return None

    return out
