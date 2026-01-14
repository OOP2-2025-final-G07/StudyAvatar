# routes/progress.py
from flask import Blueprint, render_template
from models.study import Study
from models.avatar_threshold_set import AvatarThresholdSet # 追加
from peewee import DoesNotExist

progress_bp = Blueprint('progress', __name__, url_prefix='/progress')

def get_progress_data(minutes, max_min): # max_min を引数で受け取るように変更
    """
    設定された max_min を1周として、周回数と進捗を計算
    """
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

@progress_bp.route('/bars')
def show_bars():
    # 現在有効な進化基準セットを取得
    try:
        threshold = AvatarThresholdSet.get(AvatarThresholdSet.is_active == True)
    except DoesNotExist:
        # 万が一設定がない場合のデフォルト（ふつう）
        threshold = type('obj', (object,), {'min_1': 60, 'min_2': 150, 'min_3': 300})

    max_min = threshold.min_3 # 進化段階3（180, 300, 420）を最大値にする
    
    all_studies = Study.select()
    sci_min = 0
    hum_min = 0
    
    sci_subjects = ['数学', '物理', '化学', '生物', '情報', '理系その他']
    hum_subjects = ['国語', '英語', '日本史', '世界史', '地理', '文系その他']

    for s in all_studies:
        if s.subject in sci_subjects:
            sci_min += s.minutes
        elif s.subject in hum_subjects:
            hum_min += s.minutes

    return render_template(
        'graphs/progress_bars.html',
        science=get_progress_data(sci_min, max_min),
        humanities=get_progress_data(hum_min, max_min),
        total=get_progress_data(sci_min + hum_min, max_min),
        max_min=max_min,
        threshold=threshold # マーカー表示用にthresholdオブジェクトを渡す
    )