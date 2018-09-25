# -*- encoding: utf-8 -*-

from app.handlers.abs import BaseHandler


__all__ = (
    'AppHandler',
)


class AppHandler(BaseHandler):

    def get(self):
        self.write('Hello world')
        self.finish()
