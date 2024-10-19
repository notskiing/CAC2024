from flask import Flask, render_template, request, redirect, flash, session
from bson.objectid import ObjectId
from passlib.hash import pbkdf2_sha256
import datetime
import random
import json
import base64
import os
from dotenv import load_dotenv
import pymongo
import pytz
from pytz import timezone
import tzlocal

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

print(app.config)

client = pymongo.MongoClient(os.getenv("MONGO_URI"))

db = client.hocoproject
ent = db.posts
use = db.users

@app.template_filter()

def datetimefilter(value, format="%x %I:%M %p"):
    tz = pytz.timezone(session["timezone"]) # timezone you want to convert to from UTC
    utc = pytz.timezone('UTC')  
    value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
    local_dt = value.astimezone(tz)
    return local_dt.strftime(format)

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
        timestamp = datetime.datetime.now(datetime.timezone.utc)
        k = request.form
        print(request.form, request.files)
        raw_image = request.files['image']
        image = base64.b64encode(raw_image.read())
        ent.insert_one({'title': k['title'],'post': k['post'],'name': k['name'], 'time': timestamp, 'image': image.decode()})
        return redirect('/dashboard')

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if request.method == 'GET':
        if "username" in session:
            return render_template('dashboard.html')
        else:
            return redirect('/login')

@app.route('/login', methods=['GET','POST'])
def log():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        print(request.form)
        username = request.form['username']
        password = request.form['password']
        user_tz = request.form['timezone']
        session["timezone"] = user_tz
        u = use.find_one({'username': username})
        if u != None:
            print('user exists, now finding password')
            if pbkdf2_sha256.verify(password, u['password']) == True:
                print('login success!')
                session["username"] = username
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
        data = ent.find()
        return render_template('feed.html', data=data)

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