# encoding: utf-8

from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('workflow')
app.config_from_object('workflow.celeryconfig')

if __name__ == '__main__':
    app.start()

