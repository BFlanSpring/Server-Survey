from flask import Flask, render_template, request, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY']="secret"
debug = DebugToolbarExtension(app)

responses = []

@app.route("/")
def start_survey():
    """render the survey page"""
    return render_template('start_survey.html', title=satisfaction_survey.title, instructions=satisfaction_survey.instructions)

@app.route("/questions/<int:question_index>", methods=['GET', 'POST'])
def show_question(question_index):
    """Render the question form and handle form submission"""
    if request.method == 'POST':
        # Save answer
        response = request.form['answer']
        responses.append(response)

        """ Checking for more questions """
        if question_index + 1 < len(satisfaction_survey.questions):
            return redirect(url_for('show_question', question_index=question_index + 1))
        else:
            """Redirect to complete page """
            return redirect(url_for('complete_survey'))

    question = satisfaction_survey.questions[question_index]

    return render_template('question.html', question=question, question_index=question_index)

@app.route("/complete")
def complete_survey():
    """render complete page"""
    return render_template ('complete.html')