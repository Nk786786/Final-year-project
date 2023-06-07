from flask import Flask, request, render_template, flash, redirect, url_for, session, Response, render_template_string
from subjective import SubjectiveTest
import nltk

app = Flask(__name__)

app.secret_key = 'aica2'

nltk.download('punkt')  # Download the punkt tokenizer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test_generate', methods=["POST"])
def test_generate():
    if request.method == "POST":
        inputText = request.form["itext"]
        testType = request.form["test_type"]
        noOfQues = request.form["noq"]
        
        # Tokenize the input text
        inputTokens = nltk.word_tokenize(inputText)
        inputText = " ".join(inputTokens)
        
        if testType == "objective":
            objective_generator = ObjectiveTest(inputText, noOfQues)
            question_list, answer_list = objective_generator.generate_test()
            testgenerate = zip(question_list, answer_list)
            return render_template('generatedtestdata.html', cresults=testgenerate)
        elif testType == "subjective":
            subjective_generator = SubjectiveTest(inputText, noOfQues)
            question_list, answer_list = subjective_generator.generate_test()
            testgenerate = zip(question_list, answer_list)
            return render_template('generatedtestdata.html', cresults=testgenerate)
        else:
            flash('Error Occurred!')
            return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
