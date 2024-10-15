from flask import Flask, render_template, request, redirect, flash
from bson.objectid import ObjectId
from passlib.hash import pbkdf2_sha256
import datetime
import random
import json
import base64
app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

import pymongo
client = pymongo.MongoClient("mongodb+srv://test_user:55QmLnJdUpl3PcKz@cluster0.9jbfb.mongodb.net/hocoproject?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")

db = client.hocoproject
ent = db.posts
use = db.users

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def add():
    if request.method == 'GET':
        data = ent.find()
        return render_template('index.html', data=data)
    if request.method == 'POST':
        print(request.form)
        return redirect('/')

@app.route('/about', methods=['GET','POST'])
def about():
    return render_template('about.html')

@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    if request.method == 'POST':
        timestamp = datetime.datetime.now()
        k = request.form
        print(request.form, request.files)
        image = request.files['image']
        print(image, base64.b64encode(image.read()))
        ent.insert_one({'title': k['title'],'post': k['post'],'name': k['name'], 'time': timestamp, 'image': base64.b64encode(image.read())})
        return redirect('/dashboard')

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if request.method == 'GET':
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
                return redirect('/dashboard')
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

@app.route('/feed', methods=['GET','POST'])
def feed():
    if request.method == 'GET':
        return render_template('feed.html')

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
    app.run(debug=True, port=5500)