from flask import Blueprint, render_template
from models import User  # Student ではなく User を使う

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/')
def test():
    users = User.select()
    return render_template('test.html', title='遷移', items=users)
