from flask import Flask, render_template, request, redirect, flash
from bson.objectid import ObjectId
from passlib.hash import pbkdf2_sha256
import datetime
import random
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

import pymongo
client = pymongo.MongoClient("mongodb+srv://test_user:TzCC3SjGsiKtP9Mi@cluster0.9jbfb.mongodb.net/jumbledwords?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")

db = client.blog
ent = db.entries
use = db.users

@app.route('/', methods=['GET','POST'])
def add():
    if request.method == 'GET':
        data = ent.find()
        return render_template('user_home.html', data=data)
    if request.method == 'POST':
        print(request.form)
        return redirect('/')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET','POST'])
def log():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        print(request.form)
        user_name = request.form['username']
        user_pass = request.form['password']
        u = use.find_one({'username': user_name})
        if u != None:
            print('user exists, now finding password')
            if pbkdf2_sha256.verify(user_pass, u['password']) == True:
                print('login success!')
                return redirect('/post')
            else:
                print('404, password not found')
                return redirect('/login')
        else:
            print('404, user not found')
            return redirect('/login')
    return redirect('/login')

@app.route('/messaging')
def messaging():
    return render_template('messaging.html')

@app.route('/register')
def register(): 
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        print(request.form)
        l = request.form
        upw = pbkdf2_sha256.hash(l['pw'])
        print(upw) 
        use.insert_one({'username': l['name'],'password': upw})
        return redirect('/login')



if __name__ == '__main__':
    app.run(debug=True)