from flask import Flask, request
from faker import Faker
import pandas
import csv
import requests


app = Flask(__name__)
fake = Faker()
list_1 = list()
height_list = list()
weight_list = list()


@app.route("/")
def hello_func():
    return "Hello"


@app.route("/requirements/")
def requirements():
    with open('requirements.txt') as f:
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


if __name__ == '__main__':
    app.run()
