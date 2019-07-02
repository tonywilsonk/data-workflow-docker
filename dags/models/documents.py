# encoding: utf-8

import mongoengine
import datetime


class Image(mongoengine.Document):
    md5 = mongoengine.StringField(unique=True)
    gray = mongoengine.ImageField()
    width = mongoengine.IntField()
    height = mongoengine.IntField()
    create_at = mongoengine.DateTimeField(default=datetime.datetime.now)


class Task(mongoengine.Document):
    url = mongoengine.StringField(max_length=250)
    state = mongoengine.StringField(choices=('success', 'error'))
    create_at = mongoengine.DateTimeField(default=datetime.datetime.now)


