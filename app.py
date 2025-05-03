from flask import Flask, render_template, request, redirect, url_for, session
from model import generate_learning_path
from database import init_db, save_plan, load_plan, mark_done, load_progress, get_tables
from datetime import date

app = Flask(__name__)
app.secret_key = 'replace-with-your-secret-key'

@app.before_first_request
def setup():
    init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    tables = get_tables()
    if request.method == 'POST':
        goal = request.form['goal']
        level = request.form['level']
        timeframe = int(request.form['timeframe'])
        session['goal'] = goal
        session['level'] = level
        session['timeframe'] = timeframe
        plan = generate_learning_path(goal, level, timeframe)
        save_plan(plan)
        return redirect(url_for('loading'))
    return render_template('index.html', tables=tables)

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/plan')
def plan():
    plan = load_plan()
    if not plan:
        return redirect(url_for('index'))
    timeframe = session.get('timeframe', 0)
    today = date.today().strftime('%d.%m.%Y')
    return render_template('plan.html', plan=plan, timeframe=timeframe, today=today)

@app.route('/progress', methods=['GET', 'POST'])
def progress():
    if request.method == 'POST':
        day = int(request.form['day'])
        mark_done(day)
    percent, items = load_progress()
    if percent == 100:
        return redirect(url_for('complete'))
    return render_template('progress.html', percent=percent, items=items)

@app.route('/complete')
def complete():
    goal = session.get('goal', 'Курс').replace('topics_', '').capitalize()
    return render_template('complete.html', goal=goal)

@app.route('/new_plan')
def new_plan():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

