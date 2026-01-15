from flask import Blueprint, render_template, request, redirect, url_for
from datetime import date, timedelta
from peewee import DoesNotExist, IntegrityError
from collections import defaultdict

# アバター関連モデル・設定
from models.avatar_history import AvatarHistory
from models.avatar_config import AVATAR_SKINS
from models.avatar_threshold_set import AvatarThresholdSet

# Blueprint 定義
avatar_bp = Blueprint('avatar', __name__, url_prefix='/avatar')


# ================================================================
# コンテキストプロセッサ
# ================================================================

# ------------------------------------------------
# 今日のアバターをテンプレに渡す（デフォルト表示用）
# ------------------------------------------------
@avatar_bp.app_context_processor
def inject_today_avatar():
    """
    今日のアバター skin をテンプレート変数 `skin` として配布する
    ・今日の AvatarHistory が存在すればその level
    ・存在しなければ level=1 を使用
    """
    try:
        record = AvatarHistory.get(AvatarHistory.date == date.today())
        level = record.level
    except DoesNotExist:
        level = 1  # 未登録日のデフォルト

    skin = AVATAR_SKINS.get(level)
    return dict(skin=skin)


# ------------------------------------------------
# n日前のアバターを取得するヘルパー関数をテンプレに渡す
# ------------------------------------------------
@avatar_bp.app_context_processor
def inject_avatar_helpers():
    """
    テンプレート内で avatar_skin_days_ago(n) を使えるようにする
    例: avatar_skin_days_ago(1) → 昨日のアバター
    """
    def avatar_skin_days_ago(n):
        target = date.today() - timedelta(days=n)
        try:
            record = AvatarHistory.get(AvatarHistory.date == target)
            return AVATAR_SKINS.get(record.level)
        except DoesNotExist:
            return AVATAR_SKINS.get(1)  # デフォルト

    return dict(avatar_skin_days_ago=avatar_skin_days_ago)


# ================================================================
# アバターレベル更新ロジック（共通処理）
# ================================================================

def update_avatar_for_date(target_date):
    """
    指定した日付（target_date）の Study を集計し、
    条件に応じたアバターレベルを算出して AvatarHistory に保存する
    """
    from models import Study

    # 指定日の学習記録を取得
    studies = Study.select().where(Study.date == target_date)

    # 教科カテゴリ定義
    categories = {
        '理系': ['数学', '物理', '化学', '生物', '情報', '理系その他'],
        '文系': ['国語', '日本史', '世界史', '地理', '英語', '文系その他']
    }

    # 分数集計用
    category_minutes = {'理系': 0, '文系': 0}
    total_minutes = 0

    # 学習時間集計
    for study in studies:
        total_minutes += study.minutes

        if study.subject in categories['理系']:
            category_minutes['理系'] += study.minutes
        if study.subject in categories['文系']:
            category_minutes['文系'] += study.minutes

    # レベル判定ロジック
    def determine_level(cat_minutes, total_minutes, threshold):
        """
        学習時間と進化基準セットからアバターレベルを決定
        """
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

    # 現在有効な進化基準セットを取得
    try:
        threshold = AvatarThresholdSet.get(AvatarThresholdSet.is_active == True)
    except DoesNotExist:
        threshold = None

    # レベル算出
    level = determine_level(category_minutes, total_minutes, threshold)

    # AvatarHistory を upsert（存在すれば更新、なければ作成）
    try:
        AvatarHistory.create(date=target_date, level=level)
    except IntegrityError:
        record = AvatarHistory.get(AvatarHistory.date == target_date)
        record.level = level
        record.save()


# ================================================================
# ルーティング
# ================================================================

# ------------------------------------------------
# 今日＋昨日のアバターレベルを更新
# （日付またぎ学習対策）
# ------------------------------------------------
@avatar_bp.route('/update', methods=['POST'])
def update_today_avatar():
    today = date.today()
    yesterday = today - timedelta(days=1)

    update_avatar_for_date(today)
    update_avatar_for_date(yesterday)

    return redirect(url_for('home'))


# ------------------------------------------------
# 直近7日間のアバターレベルをまとめて再計算
# ------------------------------------------------
@avatar_bp.route('/update_recent', methods=['POST'])
def update_recent_avatars():
    today = date.today()

    # 今日〜6日前までを再計算
    for i in range(7):
        target_date = today - timedelta(days=i)
        update_avatar_for_date(target_date)

    return redirect(url_for('home'))


# ------------------------------------------------
# 進化基準セットの切り替え
# ------------------------------------------------
@avatar_bp.route('/threshold', methods=['POST'])
def change_threshold():
    threshold_id = request.form['threshold_id']

    # すべて無効化
    AvatarThresholdSet.update(is_active=False).execute()

    # 選択されたセットを有効化
    AvatarThresholdSet.update(is_active=True) \
        .where(AvatarThresholdSet.id == threshold_id) \
        .execute()

    return redirect(url_for('home'))


# ------------------------------------------------
# 進化基準セット一覧をテンプレに渡す
# ------------------------------------------------
@avatar_bp.app_context_processor
def inject_threshold_sets():
    """
    テンプレートで進化基準セット一覧を表示するための変数
    """
    return dict(
        threshold_sets=AvatarThresholdSet.select()
    )
