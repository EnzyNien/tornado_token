# -*- encoding: utf-8 -*-
import datetime
from sqlalchemy import (
    Table, Column, Integer, DateTime, String, ForeignKey
)
from sqlalchemy.sql import func
from app.models.mixins import AppDecBase
from app_utils.db_utils.models import BaseModel


__all__ = (
    'User',
    'Tokens',
    'History'
)


class User(BaseModel, AppDecBase):
    '''Пользователи'''

    __tablename__ = "users"

    id = Column(
        Integer, 
        primary_key=True)
    login = Column(
        String(length=150),
        nullable=False)
    password = Column(
        String(length=150),
        nullable=False)

    def __init__(self, login, password):
        self.date = login
        self.open = password


class Tokens(BaseModel, AppDecBase):
    '''Токены'''

    __tablename__ = "tokens"

    id = Column(Integer, 
        primary_key=True)
    user = Column(Integer, 
        ForeignKey("user.id"), 
        nullable=False)
    token = Column(
        DateTime)

    def __init__(self, user, token):
        self.date = name
        self.open = token


class History(BaseModel, AppDecBase):
    '''История'''

    __tablename__ = "history"

    id = Column(
        Integer, 
        primary_key=True)
    user = Column(
        Integer, 
        ForeignKey("user.id"), 
        nullable=False)
    date = Column(
        DateTime, 
        server_default=func.now())

    def __init__(self, user, token):
        self.date = name
        self.open = token
