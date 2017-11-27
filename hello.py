#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from flask import Flask, request,url_for, redirect
from flask import render_template

app = Flask(__name__)
app.secret_key = '#ekd@aA/3g dE~2A!jEdH.,!RA' #Secret key in Session

@app.errorhandler(404) # error handler
def page_not_found(error) :
    return render_template('404.html'),404

@app.route('/')
@app.route('/<username>')
def home(username = None) : # get userName in index
    return render_template('index.html',username=username)

@app.route('/signup', methods=['GET','POST'])
def signup() :
    if request.method == 'POST' :
        return redirect(url_for('index'))
    return render_template('member_info.html')

@app.route('/login', methods=['GET','POST'])
def login() :
    if request.method == 'POST' :

        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/community/',methods=['GET','POST'])
def community():
    if request.method == 'POST' :
        return redirect(url_for('index'))
    return render_template('community.html')

@app.route('/admin/',methods=['GET','POST'])
def admin() :
    if request.method == 'POST' :
        return redirect(url_for('index'))
    return render_template('admin.html')

@app.route('/admin_item/', methods=['GET','POST'])
def adminitem():
    if request.method == 'POST' :
        return redirect(url_for('index'))
    return render_template('admin_item.html')

@app.route('/admin_member/', methods=['GET','POST'])
def adminmember():
    if request.method == 'POST' :
        return redirect(url_for('index'))
    return render_template('admin_member.html')

@app.route('/admin_board/', methods=['GET','POST'])
def adminboard():
    if request.method == 'POST' :
        return redirect(url_for('index'))
    return render_template('admin_board.html')

@app.route('/mypage/',methods=['GET','POST'])
@app.route('/mypage/<username>',methods=['GET','POST'])
def mypage(username = None) :
    if request.method == 'POST' :
        return redirect(url_for('index'))
    if username == None :
        return render_template('mypage.html',username = None) #'''로그인이 필요합니다'''
    return render_template('mypage.html', username=username)

@app.route('/my_order/',methods=['GET','POST'])
@app.route('/my_order/<username>',methods=['GET','POST'])
def myorder(username = None) :
    if request.method == 'POST' :
        return redirect(url_for('index'))
    if username == None :
        return render_template('my_order.html',username = None) #'''로그인이 필요합니다'''
    return render_template('my_order.html',username=username)

@app.route('/my_revise/',methods=['GET','POST'])
@app.route('/my_revise/<username>',methods=['GET','POST'])
def myrevise(username = None) :
    if request.method == 'POST' :
        return redirect(url_for('index'))
    if username == None :
        return render_template('my_revise.html',username = None) #'''로그인이 필요합니다'''
    return render_template('my_revise.html',username=username)


if __name__ == '__main__':
    app.run()
    #app.run(debug=True)
