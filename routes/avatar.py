from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime, date, timedelta
from peewee import DoesNotExist, IntegrityError

from models.avatar_history import AvatarHistory
from models.avatar_config import AVATAR_SKINS

avatar_bp = Blueprint('avatar', __name__, url_prefix='/avatar')


# ------------------------------------------------
# 今日のアバター（デフォルト用）
# ------------------------------------------------
@avatar_bp.app_context_processor
def inject_today_avatar():
    """今日のアバターを skin としてテンプレに配る"""
    try:
        record = AvatarHistory.get(AvatarHistory.date == date.today())
        level = record.level
    except DoesNotExist:
        level = 1  # デフォルト

    skin = AVATAR_SKINS.get(level)
    return dict(skin=skin)


# ------------------------------------------------
# n日前のアバターをテンプレから呼び出せる関数
# ------------------------------------------------
@avatar_bp.app_context_processor
def inject_avatar_helpers():
    """avatar_skin_days_ago(n) をテンプレで使えるようにする"""
    def avatar_skin_days_ago(n):
        target = date.today() - timedelta(days=n)
        try:
            record = AvatarHistory.get(AvatarHistory.date == target)
            return AVATAR_SKINS.get(record.level)
        except DoesNotExist:
            return AVATAR_SKINS.get(1)

    return dict(avatar_skin_days_ago=avatar_skin_days_ago)


# ------------------------------------------------
# 日付＋レベルを保存（POST）
# ------------------------------------------------
@avatar_bp.route('/set', methods=['GET', 'POST'])
def set_avatar():
    if request.method == 'POST':
        # 日付とレベルを取得（空なら今日・デフォルト1）
        date_str = request.form.get('date', '')
        level = int(request.form.get('level', 1))

        if not date_str:
            target_date = date.today()
        else:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        try:
            # 新規登録
            AvatarHistory.create(date=target_date, level=level)
        except IntegrityError:
            # 既存なら更新
            record = AvatarHistory.get(AvatarHistory.date == target_date)
            record.level = level
            record.save()

        return redirect(url_for('index'))

    # GET の場合は入力フォームを表示
    return render_template('avatar_set.html')
