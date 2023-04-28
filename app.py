from flask import Flask, request, redirect, render_template, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Amadeus'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES = []

@app.route('/')
def start_survey():
    # RESPONSES.clear()
    title = survey.title
    instruct= survey.instructions
    return render_template('begin.html', title=title, instruct=instruct)

@app.route('/questions/<int:num>')
def next_question(num):
    try:
        if num > len(RESPONSES):
            num = len(RESPONSES)
            flash('Cannot skip questions!')
            return redirect(f'/questions/{num}')
        elif len(RESPONSES) == len(survey.questions):
            return redirect('/questions/thank_you')
        else:
            question = survey.questions[num]
            return render_template('survey_question.html', question=question, num=num) 
    except:
        return "Something went wrong"

@app.route('/questions/thank_you')
def thank_you():
    if len(RESPONSES) == len(survey.questions):
        return render_template('thank_you.html')
    else:
        num = len(RESPONSES)
        flash('Cannot skip questions!')
        return redirect(f'/questions/{num}')


@app.route('/answers/<num>', methods=['POST'])
def save_answers(num):
    val = request.form[num]

    RESPONSES.append({int(num): val})
    num = int(num) + 1 
    return redirect(f'/questions/{num}')
