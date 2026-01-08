from flask import Blueprint, render_template, request, redirect, url_for
from datetime import date, datetime
from models import Study

# Blueprintの作成
# 'job' はBlueprint名、url_prefix='/job' によりURLは /job/... になる
study_bp = Blueprint('study', __name__, url_prefix='/study')


# 入力、入力したものを確認できるよう表示する
@study_bp.route('/', methods=['GET', 'POST'])
def new_study():
    if request.method == 'POST':

        # 日付が入力されていればその日付。されていなければ今日の日付が入ります
        date_str = request.form.get('date')
        if date_str:
            study_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            study_date = date.today()

        # データの登録
        Study.create(
            title=request.form['title'],
            minutes=int(request.form['minutes']),
            note=request.form['note'],
            subject=request.form['subject'],
            date=study_date
        )
        return redirect(url_for('study.new_study'))

    studys = Study.select()
    return render_template('study.html', items=studys, debug=True)
