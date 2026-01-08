from peewee import Model, CharField
from .db import db

class setting(Model):
    name = CharField()

    class Meta:
        database = db
