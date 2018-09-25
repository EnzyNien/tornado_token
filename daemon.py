# -*- coding: utf-8 -*-
import fcntl
import os
import signal
import sys
import traceback
import time

from subprocess import Popen

from application_settings import APP_HANDLERS, APP_SETTINGS
from settings import (
    DEBUG, CURRENT_PATH,
    SERVER_PORT, DB_PATH,
)
from app_utils.tornado_utils import create_server


LOCK_FNAME = CURRENT_PATH + '/lock_file'
COMMANDS = ['start', 'stop', 'restart', 'test_mode']


def kill_process(pid):
    os.kill(pid, signal.SIGKILL)


def start(port):
    started = isstarted(port)
    if not started:
        pid = Popen([
            'python', os.path.abspath(__file__),
            'daemon', str(port),
        ]).pid
        print('Server started (pid: %i) (port: %i)...' % (pid, port))
        fname = '%s_%d' % (LOCK_FNAME, port)
        with open(fname, "w") as f:
            f.write(str(pid))
    else:
        print('Server alegry started (pid: %i)' % started)


def stop(port):
    started = isstarted(port)
    if started:
        try:
            kill_process(started)
            print('Server stoped (pid %i)' % started)
        except:
            print('Server not started')
        fname = '%s_%d' % (LOCK_FNAME, port)
        os.remove(fname)
    else:
        print('Server not started')


def restart(port):
    stop(port)
    time.sleep(1)
    start(port)
    time.sleep(1)


def isstarted(port):
    '''
    if tornado is on return pid else 0
    '''
    pid = 0
    fname = '%s_%d' % (LOCK_FNAME, port)
    if os.path.exists(fname):
        with open(fname, "r") as f:
            try:
                pid = int(f.read().strip())
            except:
                pass
    return pid


def daemon(port):
    try:
        create_server(
            SERVER_PORT, APP_HANDLERS, APP_SETTINGS,
            db_settings=dict(db_path=DB_PATH),
            debug=DEBUG
        )
    except Exception as e:
        traceback.print_exc()


if __name__ == "__main__":
    num = len(sys.argv)
    if num >= 2 and sys.argv[1] in (COMMANDS + ['daemon']):
        cmd = sys.argv[1]
        port = int(sys.argv[2]) if num >= 3 else SERVER_PORT
        globals()[cmd](port)
    else:
        print('Error: invalid command')
        print('Usage: python daemon.py {%s}.' % '|'.join(COMMANDS))
