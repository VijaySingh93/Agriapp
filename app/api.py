from flask import Flask, render_template, flash, redirect, url_for, request
from search import searchAnswers
import Inference

app = Flask(__name__)
app.config['SECRET_KEY'] = '1b14bba67856caa6d514033678de'


@app.route("/")
def home():
    return render_template('main.html')


@app.route('/search', methods=['GET', 'POST'])
def search_page():
    form = searchAnswers()
    if request.method == 'POST':
        if form.validate_on_submit():
            input = request.form.get('searchtext')
            if not input == '':
                results = Inference.callfunc(input)
                return render_template('ITSMresult.html',
                                        input=input,
                                        results=results)
            else:
                results = "Please enter a question!!"
                return render_template('ITSMresult.html',
                                       input=input,
                                       results=results)

    if request.method == 'GET':
        return render_template('ITSMmain.html', form=form)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
