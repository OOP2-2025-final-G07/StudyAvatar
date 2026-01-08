from flask import Blueprint, render_template
from models import setting  # Student ではなく setting を使う

setting_bp = Blueprint('setting', __name__, url_prefix='/settings')

@setting_bp.route('/')
def seed_set():
    settings = setting.select()
    return render_template('seed_set.html', title='遷移', items=settings)
