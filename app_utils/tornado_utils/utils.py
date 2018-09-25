# -*- coding: utf-8 -*-
from tornado import httpserver, ioloop, options, web
from app_utils.db_utils import create_dbsession


def create_server(
        port,
        app_handlers,
        app_settings=None,
        db_settings=None,
        debug=False,
        process=None,
):
    if get_current_redis() is None:
        raise Exception('Need to start Redis Server!')

    app_settings = app_settings or {}
    db_settings = db_settings or {}

    app_settings.update(dict(
        debug=debug,
    ))

    options.parse_command_line()

    app = web.Application(app_handlers, **app_settings)

    app.db_session = create_dbsession(**db_settings)
    app.port = port

    http_server = httpserver.HTTPServer(app, xheaders=True)
    if process is not None:
        http_server.bind(port)
        http_server.start(process)
    else:
        http_server.listen(port)

    ioloop_instance = ioloop.IOLoop.instance()
    ioloop_instance.start()
