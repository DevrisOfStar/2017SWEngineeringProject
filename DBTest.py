#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import string
from flask import Flask, request, render_template
from flaskext.mysql import MySQL

# 이거 실행됨!
mysql = MySQL() # 안녕
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '-'
app.config['MYSQL_DATABASE_DB'] = 'aboutmydog'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def hello(username=None):
    return render_template("DBTest.html", username=username)

@app.route("/Authenticate/", methods = ['GET','POST'])
def Authenticate() :
    if request.method == 'POST' :
        username = request.form.get('Username')
        password = request.form.get('Password')

        cursor = mysql.connect().cursor()
        cursor.execute("Select * from user where userName = %s and password = %s",(username,password))
        data = cursor.fetchone()


        if data is None :
             return "hello, world"
        else :
             return "take"

if __name__ == "__main__" :
    app.run(debug=True)
