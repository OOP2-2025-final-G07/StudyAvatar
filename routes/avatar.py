from flask import Blueprint, render_template, request, redirect, url_for
from datetime import date, timedelta
from peewee import DoesNotExist, IntegrityError
from collections import defaultdict
from models.avatar_history import AvatarHistory
from models.avatar_config import AVATAR_SKINS
from models.avatar_threshold_set import AvatarThresholdSet

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
# 今日のAvatarレベル更新
# ------------------------------------------------
@avatar_bp.route('/update', methods=['POST'])
def update_today_avatar():
    today = date.today()

    from models import Study
    today_studies = Study.select().where(Study.date == today)

    # 区分定義
    categories = {
        '理系': ['数学', '物理', '化学', '生物', '情報', '理系その他'],
        '文系': ['国語', '日本史', '世界史', '地理', '英語', '文系その他']
    }

    # 集計
    category_minutes = {'理系': 0, '文系': 0}
    total_minutes = 0

    for study in today_studies:
        total_minutes += study.minutes

        if study.subject in categories['理系']:
            category_minutes['理系'] += study.minutes

        if study.subject in categories['文系']:
            category_minutes['文系'] += study.minutes

    # 判定関数
    def determine_level(cat_minutes, total_minutes, threshold):
        combined = cat_minutes['理系'] + cat_minutes['文系']
        if threshold is None:
            return 1
        if total_minutes >= threshold.min_3:
            return 8
        elif cat_minutes['理系'] >= threshold.min_2 and cat_minutes['理系'] > cat_minutes['文系']:
            return 7
        elif cat_minutes['文系'] >= threshold.min_2:
            return 6
        elif combined >= threshold.min_2:
            return 5
        elif cat_minutes['理系'] >= threshold.min_1 and cat_minutes['理系'] > cat_minutes['文系']:
            return 4
        elif cat_minutes['文系'] >= threshold.min_1:
            return 3
        elif combined >= threshold.min_1:
            return 2
        else:
            return 1

    level = determine_level(category_minutes, total_minutes)

    # DB保存
    try:
        AvatarHistory.create(date=today, level=level)
    except IntegrityError:
        record = AvatarHistory.get(AvatarHistory.date == today)
        record.level = level
        record.save()

    return redirect(url_for('index'))

@avatar_bp.route('/threshold', methods=['POST'])
def change_threshold():
    threshold_id = request.form['threshold_id']

    AvatarThresholdSet.update(is_active=False).execute()
    AvatarThresholdSet.update(is_active=True)\
        .where(AvatarThresholdSet.id == threshold_id)\
        .execute()

    return redirect(url_for('index'))

# ------------------------------------------------
# 進化基準セットをテンプレに渡す
# ------------------------------------------------
@avatar_bp.app_context_processor
def inject_threshold_sets():
    return dict(
        threshold_sets=AvatarThresholdSet.select()
    )
