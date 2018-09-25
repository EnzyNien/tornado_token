# -*- coding: utf-8 -*-
from functools import wraps


__all__ = (
    'memorizing',
)


def memorizing(func):
    name = '___' + func.__name__

    @wraps(func)
    def decorator(self, *args, **kwargs):
        if not hasattr(self, name):
            setattr(self, name, func(self, *args, **kwargs))
        return getattr(self, name)
    return decorator
