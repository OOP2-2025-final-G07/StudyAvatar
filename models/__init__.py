from .db import db
from .avatar_history import AvatarHistory
from .avatar_threshold_set import AvatarThresholdSet
from .setting import setting
from .study import Study
from seeds.avatar_seed import seed_threshold_sets

MODELS = [
    setting,
    AvatarHistory,
    Study,
    AvatarThresholdSet,
]


def initialize_database():
    db.connect(reuse_if_open=True)
    db.create_tables(MODELS, safe=True)
    seed_threshold_sets()
    db.close()