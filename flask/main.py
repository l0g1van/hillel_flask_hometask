import sqlite3

from flask import Flask, request, render_template, flash
from faker import Faker
import csv
import requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from db import get_db, init_db
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
fake = Faker()
list_1 = list()
height_list = list()
weight_list = list()

# init_db()


class GenreForm(FlaskForm):
    genre = StringField('What Genre Of Tracks Do You Want?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def hello_func():
    return render_template('hello.html', hello_word='Hello')


@app.route("/requirements/")
def requirements():
    with open('../requirements.txt') as f:
        return f.read()


@app.route("/generate-users/", methods=['GET'])
def generate_users():
    for el in range(int(request.args.get("count", 100))):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.ascii_email()
        list_1.append((first_name, last_name, email))
    return [el for el in list_1]


@app.route("/mean/")
def mean_func():
    with open("hw.csv", "r") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            height = row['Index, "Height(Inches)", "Weight(Pounds)"']
            height = height.split(', ')[1]
            weight = row['Index, "Height(Inches)", "Weight(Pounds)"']
            weight = weight.split(', ')[2]
            if height is not None and height != '--':
                height_list.append(float(height))
            if weight is not None and weight != '--':
                weight_list.append(float(weight))
    avg_height = sum(height_list) / len(height_list)
    avg_weight = sum(weight_list) / len(weight_list)
    return f"Average height in cm is {avg_height * 2.54}, Average weight in kg is {avg_weight * 0.45}"


@app.route("/space/")
def space_func():
    r = requests.get('http://api.open-notify.org/astros.json')
    return f'number of astronauts in space: {r.json()["number"]}'


@app.route('/names/')
def get_unique_names():
    db = get_db()
    unique_names = db.execute('''SELECT DISTINCT artist FROM tracks''').fetchall()
    return render_template('names.html', len_unique_names=len(unique_names))


@app.route('/tracks/')
def tracks():
    db = get_db()
    track_number = db.execute('''SELECT * FROM tracks''').fetchall()
    return render_template('track_amount.html', track_number=len(track_number))


@app.route('/tracks_by_genre/', methods=['GET', 'POST'])
def tracks_by_genre():
    db = get_db()
    genre = None
    form = GenreForm()
    if form.validate_on_submit():
        genre = form.genre.data
        form.genre.data = ''
    genre_quantity = len(db.execute('''SELECT * FROM tracks WHERE genre LIKE(?)''', (genre, )).fetchall())
    return render_template('genres.html', genre=genre, form=form, genre_quantity=genre_quantity)


@app.route('/tracks-sec/')
def titles_and_seconds():
    db = get_db()
    result = db.execute('''SELECT title, track_length FROM tracks''').fetchall()
    return render_template('titles_and_seconds.html', result=result)


@app.route('/tracks-sec/statistics/')
def stat_func():
    db = get_db()
    result = 0
    par_1 = db.execute('''SELECT SUM(track_length) FROM tracks''').fetchall()
    track_number = len(db.execute('''SELECT * FROM tracks''').fetchall())
    for el in par_1:
        result = el[0]
    average_value = result / track_number
    return render_template('stats.html', average_value=average_value, result=result)


if __name__ == '__main__':
    app.run()
