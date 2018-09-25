# -*- coding: utf-8 -*-

import copy
import threading
import traceback

from tornado import web, ioloop
from tornado.escape import utf8

from app.models import User, Tokens, History
from app_utils.db_utils import create_dbsession
from app_utils.json_utils import json
from app_utils.logger_utils import get_logger

from settings import (
    SERVER_SCHEMA, SERVER_HOST, DEBUG,
)
from app_utils.tornado_utils.wrappers import (
    memorizing, app_level_memorizing,
)


import sys
if (sys.version_info > (3, 0)):
    unicode = str


__all__ = (
    'AbsHandler',
)


class AbsHandler(web.RequestHandler):

    @property
    def db_session(self):
        return self.application.db_session

    @property
    @app_level_memorizing
    def redis(self):
        return get_current_redis()

    @property
    @app_level_memorizing
    def pipeline(self):
        return self.redis.pipeline()

    @property
    @app_level_memorizing
    def alarm(self):
        return get_alarm_bot()

    @property
    @app_level_memorizing
    def logger(self):
        return get_logger('app')

    # ---

    @memorizing
    def get_json(self):
        try:
            return json.loads(self.request.body)
        except:
            return {}

    # ---

    @classmethod
    def run_in_thread(cls, worker):
        def target():
            alarm = get_alarm_bot()
            try:
                db_session = create_dbsession()
                redis = get_current_redis()
                worker(db_session)
            except Exception as e:
                alarm.error()
            finally:
                try:
                    db_session.commit()
                except:
                    alarm.error()
                try:
                    db_session.close()
                except:
                    alarm.error()

        threading.Thread(target=target).start()

    def worker(self, db_session):
        raise NotImplementedError()

    def start_worker(self, callback=None):
        def worker(db_session):
            self.worker(db_session)
            if callback is not None:
                self.add_callback(callback)
        self.run_in_thread(worker)

    @property
    def current_ioloop(self):
        return ioloop.IOLoop.current()

    def add_callback(self, callback):
        self.current_ioloop.add_callback(callback)

    def info(self, *texts):
        text = ''
        try:
            for _text in texts:
                text += _text + '\n'
        except Exception as e:
            self.error('send info', error=e)

        if text:
            self.alarm.info(text)
            self.logger.info(text)

    def debug(self, *texts):
        text = ''
        try:
            for _text in texts:
                text += _text + '\n'
        except Exception as e:
            self.error('send debug', error=e)

        if text:
            self.alarm.debug(text)
            self.logger.debug(text)

    def error(self, texts, error=None, traceback_text='', trace=True):
        if not hasattr(texts, '__iter__'):
            texts = [texts, ]

        text = ''
        try:
            try:
                for _text in texts:
                    text += _text + u'\n'
            except:
                pass

            try:
                traceback_text = (
                    traceback_text or
                    trace and unicode(
                        traceback.format_exc(), errors='ignore'
                    ) or ''
                )
            except:
                traceback_text = u'Can\'t get traceback_text'

            try:
                error_text = (
                    'error' if error is None else unicode(error)
                )
            except:
                error_text = u'Can\'t get error_text'

            text += u'\n{}: {}'.format(error_text, traceback_text)
        except Exception as e:
            self.error('send error', error=e)

        if text:
            self.alarm.error(text, trace=False)
            self.logger.error(text)

    def log_exception(self, typ, value, tb):
        super(AbsHandler, self).log_exception(typ, value, tb)
        isinstance(value, web.HTTPError) or self.error(
            u'Uncaught exception',
            traceback_text=unicode('\n'.join(
                traceback.format_exception(typ, value, tb)
            ), errors='ignore'),
        )

    def redirect(self, url, permanent=False, status=None):
        """Sends a redirect to the given (optionally relative) URL.

        If the ``status`` argument is specified, that value is used as the
        HTTP status code; otherwise either 301 (permanent) or 302
        (temporary) is chosen based on the ``permanent`` argument.
        The default is 302 (temporary).
        """
        if self._headers_written:
            raise Exception("Cannot redirect after headers have been written")
        if status is None:
            status = 301 if permanent else 302
        else:
            assert isinstance(status, int) and 300 <= status <= 399
        self.set_status(status)
        self.set_header("Location", utf8(url))
        self.finish()
