from peewee import Model, CharField, IntegerField, DateField
from .db import db

class Study(Model):
    """
    勉強を表すテーブル用モデルクラス
    """

    # 勉強のタイトル
    title = CharField()

    # 勉強時間
    minutes = IntegerField()

    # 備考
    note = CharField()

    # 教科(選択)
    SUBJECT_CHOICES = (
        # 理系
        ('数学', '数学'),
        ('物理', '物理'),
        ('化学', '化学'),
        ('生物', '生物'),
        ('情報', '情報'),
        ('理系その他','理系その他'),

        # 文系
        ('国語', '国語'),
        ('英語', '英語'),
        ('日本史', '日本史'),
        ('世界史', '世界史'),
        ('地理', '地理'),
        ('文系その他','文系その他'),
    )

    subject = CharField(choices=SUBJECT_CHOICES)

    # 日付
    date = DateField()

    class Meta:
        # このモデルが使用するデータベースを指定
        # db は db.py で定義された Peewee のデータベース接続
        database = db
