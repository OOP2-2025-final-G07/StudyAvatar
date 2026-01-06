from flask import Blueprint, render_template, request, redirect, url_for, abort, current_app
from datetime import date, datetime
from models import Study

# Blueprintの作成
# 'job' はBlueprint名、url_prefix='/job' によりURLは /job/... になる
study_bp = Blueprint('study', __name__, url_prefix='/study')


# 入力、入力したものを確認できるよう表示する
@study_bp.route('/', methods=['GET', 'POST'])
def new_study():
    if request.method == 'POST':

        # デバッグ用データがあればタイマーを開始していなくてもデータを記録する
        debug_date = request.form.get("debug_date")
        debug_minutes = request.form.get("debug_minutes")
        if (
            request.form.get("started") != "1"
            and not (current_app.debug and (debug_minutes and debug_date))
        ):
            abort(400, "タイマーを開始してください")

        # 日付の決定（デバッグデータがあればデバッグデータを優先）
        if current_app.debug and debug_date:
            study_date = datetime.strptime(debug_date, "%Y-%m-%d").date()
        else:
            date_str = request.form.get("start_date")
            study_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        # 時間の決定（デバッグデータがあればデバッグデータを優先）
        if current_app.debug and debug_minutes:
            minutes = int(debug_minutes)
        else:
            minutes = int(request.form["minutes"])
            
        # データの登録
        Study.create(
            title=request.form['title'],
            minutes=minutes,
            note=request.form['note'],
            subject=request.form['subject'],
            date=study_date
        )
        return redirect(url_for('study.new_study'))

    studys = Study.select()
    return render_template('study.html', items=studys, debug=current_app.debug)
