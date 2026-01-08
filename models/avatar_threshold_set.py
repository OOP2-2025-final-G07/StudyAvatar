from peewee import Model, CharField, IntegerField, BooleanField
from .db import db


class AvatarThresholdSet(Model):
    name = CharField()
    min_1 = IntegerField()
    min_2 = IntegerField()
    min_3 = IntegerField()
    is_active = BooleanField(default=False)

    class Meta:
        database = db
        table_name = 'avatar_threshold_sets'
