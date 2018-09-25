# -*- coding: utf-8 -*-
from __future__ import print_function

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


__all__ = (
    'get_dbengine',
    'get_dbsession',
    'create_dbsession',
)


ENGINES = {}
DBSESSIONS = {}


def get_dbengine(db_path, **kwargs):
    if db_path not in ENGINES:
        ENGINES[db_path] = create_engine(
            db_path,
            pool_size=20,
            max_overflow=100,
        )
    return ENGINES[db_path]


def create_dbsession(db_path, **kwargs):
    engine = get_dbengine(db_path=db_path, **kwargs)
    SessionClass = sessionmaker(bind=engine)
    return SessionClass()


def get_dbsession(db_path, **kwargs):
    if db_path not in DBSESSIONS:
        DBSESSIONS[db_path] = create_dbsession(db_path, **kwargs)
    return DBSESSIONS[db_path]
