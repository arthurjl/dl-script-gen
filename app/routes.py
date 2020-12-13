from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    data = [
        {
            'author': {'username': 'arthur'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'taylor'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'daniel'},
            'body': 'i watned to play pingpong!'
        }
    ]
    return render_template('index.html', title='Home', data=data)
