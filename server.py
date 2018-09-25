# -*- encoding: utf-8 -*-

from application_settings import APP_HANDLERS, APP_SETTINGS
from app_utils.tornado_utils import create_server
from settings import DEBUG, SERVER_PORT, DB_PATH, PROCESS_NUM


if __name__ == "__main__":
    #print('server started (port: {})'.format(SERVER_PORT))

    create_server(
        SERVER_PORT, APP_HANDLERS, APP_SETTINGS,
        db_settings=dict(db_path=DB_PATH),
        debug=DEBUG, process=PROCESS_NUM,
    )
