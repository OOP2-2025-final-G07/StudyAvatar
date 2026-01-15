

from flask import Flask, render_template
from models import initialize_database, Study # Studyを追加
from models.avatar_threshold_set import AvatarThresholdSet # 追加
from peewee import DoesNotExist
from datetime import date
from routes import blueprints

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# 設定された max_min を1周として、周回数と進捗を計算 (progress.pyのロジックを流用)
def get_progress_data(minutes, max_min):
    """
    設定された max_min を1周として、周回数と進捗を計算
    """
    if max_min <= 0: return {"val": 0, "lap": 1, "percent": 0} # 0除算防止
    lap = (minutes // max_min) + 1
    display_min = minutes % max_min
    
    if minutes > 0 and display_min == 0:
        lap -= 1
        display_min = max_min
        
    return {
        "val": display_min,
        "lap": lap,
        "percent": (display_min / max_min) * 100
    }

# ホームページのルート
@app.route('/')
def index():
    # 直近の学習ログを取得（最新5件）
    recent_studies = Study.select().order_by(Study.date.desc()).limit(5)

    # 進捗ゲージ用のデータを集計
    try:
        threshold = AvatarThresholdSet.get(AvatarThresholdSet.is_active == True)
    except DoesNotExist:
        # 万が一設定がない場合のデフォルト
        threshold = type('obj', (object,), {'min_1': 60, 'min_2': 150, 'min_3': 300})

    max_min = threshold.min_3
    all_studies = Study.select()
    
    sci_subjects = ['数学', '物理', '化学', '生物', '情報', '理系その他']
    # 理系・文系の集計
    sci_min = sum(s.minutes for s in all_studies if s.subject in sci_subjects)
    hum_min = sum(s.minutes for s in all_studies if s.subject not in sci_subjects)

    return render_template(
        'index.html',
        recent_studies=recent_studies,
        science=get_progress_data(sci_min, max_min),
        humanities=get_progress_data(hum_min, max_min),
        total=get_progress_data(sci_min + hum_min, max_min),
        current_date=date.today().strftime('%Y/%m/%d')
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False) #False