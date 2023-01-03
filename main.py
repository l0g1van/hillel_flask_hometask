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
    pass


@app.route("/requirements/")
def requirements():
    pass


@app.route("/generate-users/", methods=['GET'])
def generate_users():
    pass


@app.route("/mean/")
def mean_func():
    pass


@app.route("/space/")
def space_func():
    pass


if __name__ == '__main__':
    app.run()
