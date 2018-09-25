# -*- coding: utf-8 -*-
import os
import shutil

from app_utils.alarm_utils import get_alarm_bot
from app_utils.db_utils import create_dbsession
from app_utils.json_utils import json
from app_utils.redis_utils import get_current_redis


class BaseManagementCommand(object):

    def __init__(self, db_session=None, redis=None, *args, **kwargs):
        if db_session is None:
            self.need_close_db_session = True
        else:
            self.need_close_db_session = False

        self.db_session = db_session or create_dbsession()
        self.redis = redis or get_current_redis()
        self.alarm_bot = get_alarm_bot()

    def __del__(self):
        if self.db_session is not None and \
                self.need_close_db_session:
            try:
                self.db_session.close()
            except:
                self.alarm_bot.error()
                raise
            self.db_session = None

    @staticmethod
    def _check_or_create_path(path):
        dirs = path.split('/')[:-1]
        for i in range(1, len(dirs)):
            current_path = '/'.join(dirs[:i + 1])
            if not os.path.isdir(current_path):
                os.mkdir(current_path)

    @staticmethod
    def rmfile(path):
        try:
            if os.path.isfile(path):
                os.remove(path)
        except Exception as error:
            print("can't delete file: {}".format(path))
            print(error)
            return None
        return True

    @staticmethod
    def rmdir(path):
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
        except Exception as error:
            print("can't delete dir: {}".format(path))
            print(error)
            return None
        return True

    def _set_options(self, *args, **options):
        pass
