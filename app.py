from flask import Flask, render_template, request, redirect, flash
from bson.objectid import ObjectId
from passlib.hash import pbkdf2_sha256
import datetime
import random
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

import pymongo
client = pymongo.MongoClient("mongodb+srv://test_user:55QmLnJdUpl3PcKz@cluster0.9jbfb.mongodb.net/hocoproject?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")

db = client.hocoproject
ent = db.posts
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

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/about', methods=['GET','POST'])
def about():
    return render_template('about.html')

@app.route('/create', methods=['GET','POST'])
def create():
    return render_template('create.html')

@app.route('/dashboard', methods=['GET','POST'])
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

@app.route('/messaging', methods=['GET','POST'])
def messaging():
    return render_template('messaging.html')

@app.route('/register', methods=['GET','POST'])
def register(): 
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        print(request.form)
        l = request.form
        upw = pbkdf2_sha256.hash(l['pw'])
        print(l['name'], upw) 
        use.insert_one({'username': l['name'],'password': upw})
        return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)