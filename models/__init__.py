from .db import db
from .user import User

MODELS = [
    User
]

def initialize_database():
    db.connect()
    db.create_tables(MODELS, safe=True)
    db.close()
