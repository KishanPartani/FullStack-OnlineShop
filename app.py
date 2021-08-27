from re import A
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
orders = db1.orders
global products, cart, totalsum, pcartt
totalsum = 0
cart = []
pcartt = []
products = []
names = []
weights = []
rate = []
for i in cooking_essentials.find():
        #print(i['pname'])
        names.append(i['pname'])
        weights.append(i['pwt'])
        rate.append(i['prate'])
for i in range(cooking_essentials.count()):
    products.append([names[i], weights[i], rate[i]])

@app.route('/')
def index():
    global products
    #print(products)
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
    #print(cust_id)
    return render_template('login.html')

@app.route('/loggingin', methods=['GET', 'POST'])
def loginsuc():
    number = request.form['num']
    pwd = request.form['password']
    user_cred = info.find_one({'mobn': number}, {
        'name': 1, 'address': 1, 'password': 1})
    global products
    if(not bool(user_cred)):
        return render_template('signup.html')
    if(bcrypt.check_password_hash(user_cred['password'], pwd)):
        # create session variable with email
        session['name'] = user_cred['name']
        print(session['name'])
        return render_template('index.html', name=user_cred['name'], products=products, msg='Logout', urllink='logoutl')
    else:
        return render_template('signup.html')

@app.route('/logoutl')
def logout():
    global products
    #print(products)
    pcartt = []
    session.clear()
    return render_template('index.html', products=products, msg='Login', urllink='login_signup')

@app.route('/addtocart', methods=['GET', 'POST'])
def cartadd():
    global products, cart
    if 'name' not in session:
        return render_template('login.html')
    if request.method == 'POST':
        pname = request.form['pname']
        pquant = request.form['quant']
        print(pname, pquant)
        cart.append([pname, pquant])
    #print(cart)
    return render_template('index.html', name=session['name'], products=products, msg='Logout', urllink='logoutl')

@app.route('/mycart')
def mycart():
    global cart, totalsum, pcartt
    if 'name' not in session:
        return render_template('login.html')
    
    pcart = []
    pwtcart = []
    pratecart = []
    pquant = []
    totalsum = 0
    for i in cart:
        prod_cred = cooking_essentials.find_one({'pname': i[0]}, {
        'pwt': 1, 'prate': 1})
        totalsum += int(i[1]) * int(prod_cred['prate'])
        pcart.append(i[0])
        pwtcart.append(prod_cred['pwt'])
        pratecart.append(prod_cred['prate'])
        pquant.append(i[1])
    for i in range(len(pcart)):
        pcartt.append([pcart[i], pwtcart[i], pratecart[i], pquant[i]])
    print(pcartt)
    return render_template('cart.html', name=session['name'], msg='Logout', urllink='logoutl', pcartt=pcartt, sum=totalsum)

@app.route('/placeorder')
def placeorder():
    global pcartt,totalsum
    if 'name' not in session:
        return render_template('login.html')
    user_cred = info.find_one({'name': session['name']}, {'mobn':1, 'address': 1, 'password': 1})
    order_details = {"cust_name": session['name'],
                    "mobn": user_cred['mobn'],
                    "address": user_cred['address'],
                    "order": pcartt,
                    "total": totalsum}
    order_id = db1.orders.insert_one(order_details).inserted_id
    print(order_id)
    return "Order Placed"


if __name__ == "__main__":
    print('started')
    app.run(debug=True)