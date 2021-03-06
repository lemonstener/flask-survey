from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


app = Flask(__name__)
app.config['SECRET_KEY'] = 'chickenz'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def start_session():
    title = satisfaction_survey.title
    info = satisfaction_survey.instructions
    return render_template('home.html', title=title, description=info)


@app.route('/begin', methods=['POST'])
def home_page():
    session['responses'] = []
    print(session['responses'])
    return redirect('/hub')


@app.route('/hub')
def redirect_to_page():
    if len(session['responses']) < len(satisfaction_survey.questions):
        return redirect(f'/questions/{len(session["responses"])}')
    else:
        return redirect('/thankyou')


@app.route('/questions/<int:id>')
def show_question(id):
    if id != len(session['responses']):
        flash('Invalid page', 'error')
        return render_template('question.html', error=True)
    else:
        question = satisfaction_survey.questions[id].question
        return render_template('question.html', question=question)


@app.route('/answer', methods=['POST'])
def update_responses():
    answer = request.form['option']
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses
    return redirect('/hub')


@app.route('/thankyou')
def reset_survey():
    responses = []
    return render_template('thankyou.html')
