from flask import Flask, render_template, request
from giorgisshubi import lgconvert, glconvert, noun_breaker, noun_maker
import json

app = Flask(__name__)
with app.open_resource('static/dictionary02.json','r') as f:
    x = f.read()
    all_words = json.loads(x)

@app.route('/', methods=['GET', 'POST'])
def dictionary():
    if request.method == 'POST':
        result = request.form
        word = result['word']
        gmorph = lgconvert(word)
        lmorph = glconvert(word)
        noun = noun_breaker(lmorph)

        if type(noun) == dict:         
            return render_template('index.html', word=word, noun=noun)
               
        else:
            return render_template('index.html', word=None, noun=noun)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)




