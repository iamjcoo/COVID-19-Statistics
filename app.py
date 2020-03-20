from flask import Flask, render_template, redirect, json, jsonify, url_for
from babel.numbers import format_decimal
import requests
import json

app = Flask(__name__)
app.run(debug=False)

@app.route("/")
def index():
    url = 'https://corona.lmao.ninja/countries'
    response = requests.get(url)
    data = response.json()

    confirmed = format_decimal(sum(d['cases'] for d in data if d), locale="en_US")
    deaths = format_decimal(sum(d['deaths'] for d in data if d), locale="en_US")
    active = format_decimal(sum(d['active'] for d in data if d), locale="en_US")
    recovered = format_decimal(sum(d['recovered'] for d in data if d), locale="en_US")
    return render_template('base.html', confirmed=confirmed, deaths=deaths, recovered=recovered, active=active, data=data)

@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/<country>")
def country(country):
    url = 'https://corona.lmao.ninja/countries/' + country
    response = requests.get(url)
    check = response.content

    url1 = 'https://pomber.github.io/covid19/timeseries.json'
    response1 = requests.get(url1)
    data1 = response1.json()

    if check!="Country not found":
        data = response.json()
        return render_template('country.html', data=data, data1=data1[country])
    else:
        return redirect(url_for('index'))
