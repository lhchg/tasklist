"""
WSGI config for analyze project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys


from django.core.wsgi import get_wsgi_application
import pickle
import multiprocessing
import daemon
import gunicorn.app.base
import logging
from logging.handlers import RotatingFileHandler


sys.path.append("../")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "analyze.settings")

application = get_wsgi_application()


class GunicornApp(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

#def run_gunicorn():
#    ip = os.getenv('DL_SYSTEM_IP')
#    port = os.getenv('DL_SYSTEM_PORT')
#
#    options = {
#        'bind': ['%s:%s' % (ip, port)],
#        'workers': multiprocessing.cpu_count(),
#        'daemon': False,
#    }
#    GunicornApp(application, options).run()

def run_gunicorn():
    ip = os.getenv('DL_SYSTEM_IP')
    port = os.getenv('DL_SYSTEM_PORT')

    log_file = "/tmp/web.log"
    error_file = open(log_file, "w")
    context = daemon.DaemonContext(stdout=error_file, stderr=error_file)

    with context:
        options = {
            'bind': ['%s:%s' % (ip, port)],
            'workers': multiprocessing.cpu_count(),
            'daemon': False,
        }
        GunicornApp(application, options).run()

if __name__ == '__main__':
    with daemon.DaemonContext():
        run_gunicorn()
