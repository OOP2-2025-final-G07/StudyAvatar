from flask import Blueprint, redirect, url_for
from datetime import date
from peewee import IntegrityError
from models import Study, AvatarHistory # modelsからインポート

# 集計専用のBlueprint
aggregator_bp = Blueprint('aggregator', __name__, url_prefix='/aggregate')

@aggregator_bp.route('/update', methods=['POST'])
def update_level():
    today = date.today()
    # 今日の勉強データを取得
    studies = Study.select().where(Study.date == today)

    # 教科カテゴリの定義（study.html の値 に準拠）
    sci_list = ['数学', '物理', '化学', '生物', '情報', '理系その他']
    art_list = ['国語', '日本史', '世界史', '地理', '文系その他']

    sci_score = 0.0
    art_score = 0.0
    total_minutes = 0

    print(f"\n--- 集計デバッグ開始 ({today}) ---")

    # 指定された配分ルールで集計
    for s in studies:
        total_minutes += s.minutes # minutesフィールドを加算
        subject = s.subject # subjectフィールドを確認
        
        current_sci = 0
        current_art = 0

        if subject == '英語':
            # 英語は50%ずつ分配
            current_sci = s.minutes * 0.5
            current_art = s.minutes * 0.5
        elif subject in sci_list:
            # 数学・理系その他などは100%理系
            current_sci = s.minutes
        elif subject in art_list:
            # 社会・文系その他などは100%文系
            current_art = s.minutes
        
        sci_score += current_sci
        art_score += current_art
        print(f"教科: {subject:.<6} | 時間: {s.minutes:>3}分 | 理系加算: {current_sci:>5} | 文系加算: {current_art:>5}")

    # --- 3段階のレベル判定ロジック ---
    def determine_level(s_val, a_val):
        # 1. 両方のスコアが60を超えている場合（バランス型）
        if s_val > 60 and a_val > 60:
            return 3
        # 2. 理系スコアの方が大きい場合（理系特化）
        elif s_val > a_val:
            return 2
        # 3. 文系スコアの方が大きい、または同点の場合（文系特化/デフォルト）
        else:
            return 1

    level = determine_level(sci_score, art_score)

    print(f"【最終結果】 理系スコア: {sci_score} | 文系スコア: {art_score} | レベル: {level}")
    print("--- 集計デバッグ終了 ---\n")

    # DB保存（AvatarHistoryのdateはユニーク制約あり）
    try:
        AvatarHistory.create(date=today, level=level)
    except IntegrityError:
        # すでにレコードがある場合は更新
        record = AvatarHistory.get(AvatarHistory.date == today)
        record.level = level
        record.save()

    return redirect(url_for('index'))