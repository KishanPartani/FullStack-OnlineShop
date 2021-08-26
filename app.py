from flask import Flask, render_template, url_for, request, flash, redirect, jsonify, send_file, session
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
from pymongo import MongoClient

app = Flask(__name__)
bcrypt = Bcrypt(app)
client = MongoClient('localhost', 27017)

cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = '14ec258c169f5c19f78385bcc83a51df7444624b2ff90449b4a9832e6fe706a1'

db = client.products
cooking_essentials = db.cooking_essentials
db1 = client.users
info = db1.info

@app.route('/')
def index():
    names = []
    weights = []
    rate = []
    for i in cooking_essentials.find():
        print(i['pname'])
        names.append(i['pname'])
        weights.append(i['pwt'])
        rate.append(i['prate'])
    products = []
    for i in range(cooking_essentials.count()):
        products.append([names[i], weights[i], rate[i]])
    print(products)
    return render_template('index.html', products=products, msg='Login', urllink='login_signup')

@app.route('/login_signup')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signingin', methods=['GET', 'POST'])
def loginsignup():
    name = request.form['name']
    password_hash = bcrypt.generate_password_hash(request.form['password'], 10)
    user_details = {"name": name,
                    "mobn": request.form['num'],
                    "address": request.form['address'],
                    "password": password_hash}
    cust_id = db1.info.insert_one(user_details).inserted_id
    print(cust_id)
    return render_template('login.html')

@app.route('/loggingin', methods=['GET', 'POST'])
def loginsuc():
    number = request.form['num']
    pwd = request.form['password']
    user_cred = info.find_one({'mobn': number}, {
        'name': 1, 'address': 1, 'password': 1})
    names = []
    weights = []
    rate = []
    for i in cooking_essentials.find():
        print(i['pname'])
        names.append(i['pname'])
        weights.append(i['pwt'])
        rate.append(i['prate'])
    products = []
    for i in range(cooking_essentials.count()):
        products.append([names[i], weights[i], rate[i]])
    if(not bool(user_cred)):
        return render_template('signup.html')
    if(bcrypt.check_password_hash(user_cred['password'], pwd)):
        return render_template('index.html', name=user_cred['name'], products=products, msg='Logout', urllink='logoutl')
    else:
        return render_template('signup.html')

@app.route('/logoutl')
def logout():
    names = []
    weights = []
    rate = []
    for i in cooking_essentials.find():
        print(i['pname'])
        names.append(i['pname'])
        weights.append(i['pwt'])
        rate.append(i['prate'])
    products = []
    for i in range(cooking_essentials.count()):
        products.append([names[i], weights[i], rate[i]])
    print(products)
    return render_template('index.html', products=products, msg='Login', urllink='login_signup')

if __name__ == "__main__":
    print('started')
    app.run(debug=True)