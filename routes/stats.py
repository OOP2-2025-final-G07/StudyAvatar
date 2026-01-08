# routes/stats.py

from flask import Blueprint, render_template
from datetime import date, timedelta
from collections import defaultdict
from models.study import Study  # 勉強データのモデル
from peewee import fn

# Blueprintの定義
stats_bp = Blueprint('stats', __name__, url_prefix='/stats')

# ------------------------------------------------
# ① 教科別バランス（円グラフ用データ）
# ------------------------------------------------
@stats_bp.route('/graph/subject')
def subject_balance():
    # データベースからすべての勉強データを取得
    all_study = Study.select()
    
    # ターミナルでのデバッグ表示
    print(f"--- DEBUG: 教科別グラフ集計開始 ---")
    print(f"取得レコード数: {len(all_study)}件")

    # 教科ごとに分数を加算
    counts = defaultdict(int)
    for item in all_study:
        counts[item.subject] += item.minutes
    
    # 集計結果の確認
    print(f"集計結果(辞書): {dict(counts)}")
    print(f"--------------------------------")

    # グラフ表示用テンプレートにラベルと値を渡す
    return render_template(
        'graphs/chart_subject.html',
        labels=list(counts.keys()),
        values=list(counts.values())
    )


# ------------------------------------------------
# ② 学習時間の推移（過去7日間・棒グラフ用データ）
# ------------------------------------------------
@stats_bp.route('/graph/transition')
def study_transition():
    today = date.today()
    labels = []
    values = []

    print(f"--- DEBUG: 学習推移グラフ集計開始 ---")

    # 過去7日間分をループ（6日前から今日まで）
    for i in range(6, -1, -1):
        target_date = today - timedelta(days=i)
        
        # グラフのX軸ラベル（月/日）
        date_str = target_date.strftime('%m/%d')
        labels.append(date_str)
        
        # その日の合計学習時間をSQLのSUM関数で計算
        # scalar() は単一の値を返す
        day_total = (Study.select(fn.SUM(Study.minutes))
                     .where(Study.date == target_date)
                     .scalar()) or 0
        
        values.append(day_total)
        print(f"日付: {date_str}, 合計分数: {day_total}分")

    print(f"最終ラベルリスト: {labels}")
    print(f"最終データリスト: {values}")
    print(f"----------------------------------")

    return render_template(
        'graphs/chart_transition.html',
        labels=labels,
        values=values
    )