# seed/avatar_seed.py
from models.db import db
from models.avatar_threshold_set import AvatarThresholdSet

def seed_threshold_sets():
    if AvatarThresholdSet.select().count() == 0:
        AvatarThresholdSet.insert_many([
            dict(name='ゆるめ', min_1=30, min_2=90,  min_3=180),
            dict(name='ふつう', min_1=60, min_2=150, min_3=300, is_active=True),
            dict(name='きつめ', min_1=90, min_2=210, min_3=420),
        ]).execute()
