# -*- coding: utf8 -*-
import re

from transliterate import translit


__all__ = (
    'WORDS_EXP',
    'rreplace',
    'get_translit_from_rus_text',
    'get_url_path_from_rus_text',
)


WORDS_EXP = re.compile(ur'[\dA-Za-zА-ЯЁа-яё]+', re.I)


def rreplace(text, old, new, count=None):
    if count is None:
        items = text.rsplit(old)
    else:
        items = text.rsplit(old, count)
    return new.join(items)


def get_translit_from_rus_text(rus_text):
    return translit(rus_text, 'ru', reversed=True)


def get_url_path_from_rus_text(rus_text):
    words = WORDS_EXP.findall(rus_text)
    rus_text = u'_'.join(words).lower()
    url_path = get_translit_from_rus_text(rus_text)
    url_path = url_path.replace("'", '')
    return url_path
