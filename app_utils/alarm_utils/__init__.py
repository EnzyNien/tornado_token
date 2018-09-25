# -*- coding: utf8 -*-

import functools

from telegram_bot import AlarmTgBot

try:
    import settings
    settings.ALARM_TG_ACCESS_TOKEN
    settings.ALARM_TG_CHAT
    settings.ALARM_TG_INFO_CHAT
    settings.ALARM_TG_DEBUG_CHAT
except:
    print('''add settings.py with:

ALARM_TG_ACCESS_TOKEN = "..."
ALARM_TG_CHAT = "..."
ALARM_TG_INFO_CHAT = "..."
ALARM_TG_DEBUG_CHAT = "..."
''')
    import sys
    sys.exit()


__all__ = (
    'get_alarm_bot', 'alarm_exception',
    'debug', 'info', 'error',
)


def get_alarm_bot(
        messenger='tg',
):
    if messenger == 'tg':
        return AlarmTgBot(
            settings.ALARM_TG_ACCESS_TOKEN,
            settings.ALARM_TG_CHAT,
            settings.ALARM_TG_INFO_CHAT,
            settings.ALARM_TG_DEBUG_CHAT,
        )

    return None


ALARM_BOT = get_alarm_bot()


def alarm_exception(text='Error', raise_exc=False):
    def actual(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                ALARM_BOT.error(text)
                if raise_exc:
                    raise
            return None
        return wrapper
    return actual


def debug(*args, **kwargs):
    ALARM_BOT.debug(*args, **kwargs)


def info(*args, **kwargs):
    ALARM_BOT.info(*args, **kwargs)


def error(*args, **kwargs):
    ALARM_BOT.error(*args, **kwargs)


if __name__ == '__main__':
    for update in get_alarm_bot().get_updates():
        print('\n{}'.format(update.message))
