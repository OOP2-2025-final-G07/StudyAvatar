from peewee import Model, DateField, IntegerField
from .db import db   # いま使ってるやつ

class AvatarHistory(Model):
    date = DateField(unique=True)   # 同じ日付は1件だけ
    level = IntegerField()

    class Meta:
        database = db
