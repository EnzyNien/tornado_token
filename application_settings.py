# -*- encoding: utf-8 -*-

from app.handlers import (
    AppHandler
)

from settings import CURRENT_PATH


APP_SETTINGS = {
}


APP_HANDLERS = [
    (r'/', AppHandler),
]
