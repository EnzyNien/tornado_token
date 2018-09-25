# -*- coding: utf-8 -*-
from __future__ import print_function

import copy

from sqlalchemy.orm.query import Query

__all__ = ('BaseModel', )


class DjangoQuery(Query):

    def __init__(
            self,
            session,
            model,
            entities=None,
            redis=None,
            base_filters=None
    ):
        super(self.__class__, self).__init__(entities or model, session)
        self.model = model
        self.base_filters = base_filters or {}

    def _query(self, *entities):
        return self.__class__(
            self.session,
            self.model,
            entities=entities,
            base_filters=self.base_filters,
        )

    def get(self, *filters, **filters_by):
        query = self.__use_filters(*filters, **filters_by)
        return query.first()

    def last(self, order_by=None, *filters, **filters_by):
        query = self.__use_filters(*filters, **filters_by)
        if order_by is None:
            order_by = self.model.id.desc()
        return query.order_by(None).order_by(order_by).first()

    def all(self, *filters, **filters_by):
        query = self.__use_filters(*filters, **filters_by)
        return super(query.__class__, query).all()

    def exists(self, *filters, **filters_by):
        return bool(
            self._query(self.model.id).get(*filters, **filters_by)
        )

    def __use_filters(self, *filters, **filters_by):
        query = self
        if filters:
            query = query.filter(*filters)
        filters_by = self.__update_filters(filters_by)
        if filters_by:
            query = query.filter_by(**filters_by)
        return query

    def __update_filters(self, filters):
        updated_filters = copy.deepcopy(self.base_filters)
        updated_filters.update(filters or {})
        return updated_filters


class BaseModel:

    id = None
    BASE_MODEL_FILTERS = None

    @classmethod
    def query(cls, db_session, redis=None, entities=None, base_filters=None):
        if base_filters is None:
            base_filters = cls.BASE_MODEL_FILTERS

        query = DjangoQuery(
            db_session,
            cls,
            entities=entities,
            base_filters=base_filters
        )
        return query

    def save(self, db_session, commit=True):
        if self.id is None:
            db_session.add(self)
        commit and db_session.commit()
        return self
