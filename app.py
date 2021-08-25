from flask import Flask, render_template, url_for, request, flash, redirect, jsonify, send_file, session
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.products
cooking_essentials = db.cooking_essentials


@app.route('/')
def index():
    names = []
    weights = []
    rate = []
    for i in cooking_essentials.find():
        print(i['pname'])
        names.append(i['pname'])
        #weights.append[i['pwt']]
        #rate.append[i['prate']]
    return render_template('index.html', names=names, weights=weights, rate=rate)

if __name__ == "__main__":
    print('started')
    app.run(debug=True)