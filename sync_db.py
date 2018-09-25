# -*- coding: utf-8 -*-

from app_utils.db_utils import (
    get_dbengine, create_dbsession,
)

from app.models import AppDecBase


class SyncDB(object):

    def __init__(self, db_engine=None, db_session=None):
        self.db_engine = db_engine or get_dbengine()
        self.db_session = db_session or create_dbsession()

    def handler(self):
        self.create_all_models()

    def create_all_models(self):
        AppDecBase.metadata.create_all(self.db_engine)
        # ...

        self.db_session.commit()


if __name__ == '__main__':
    SyncDB().handler()
