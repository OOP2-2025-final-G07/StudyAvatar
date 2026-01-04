from .db import db
from .avatar_history import AvatarHistory
from .user import User
from .study import Study

MODELS = [
    User,
    AvatarHistory,
    Study,
]

def initialize_database():
    db.connect()
    db.create_tables(MODELS, safe=True)
    db.close()