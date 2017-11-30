#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import string

reload(sys)
sys.setdefaultencoding('utf8')

from flask import Flask, request, url_for, redirect, session, flash
from flask import render_template
from flaskext.mysql import MySQL



app = Flask(__name__)
app.secret_key = '#ekd@aA/3g dE~2A!jEdH.,!RA' #Secret key in Session

# mysql 초기설정
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'melting7.5'
app.config['MYSQL_DATABASE_DB'] = 'aboutmydog'
app.config['MYSQL_DATABASE_HOST'] = '210.89.180.38'
mysql.init_app(app)

# error handler
@app.errorhandler(404)
def page_not_found(error) :
    return render_template('404.html'),404
# main 부분
@app.route('/') # 완료
def home(username = None) : # get userName in index
    if 'username' in session :
        username = session['username']
    else :
        username = None
    return render_template('index.html',username = username)
#signup, login 부분
@app.route('/signup/', methods=['GET','POST']) # 완료
def signup() :
        return render_template('member_info.html')

@app.route('/signup_verify/', methods=['GET','POST']) # 완료
def signup_verify() :
    button = request.values.get('button')
    UserID = request.values.get('ID')
    if button == "save" :
        # 정보 가져오기
        Password = request.values.get('password')
        Password2 = request.values.get('password2')
        UserName = request.values.get('name')
        Zipcode = request.values.get('zipcode')
        address1 = request.values.get('address1')
        address2 = request.values.get('address2')
        email = request.values.get('email')
        phoneNum = request.values.get('phoneNum')
        address = address1
        address = address + address2

        # 유효성 확인 : password 유효성 검사만 추가하면됨
        cursor = mysql.connect().cursor()
        cursor.execute('select * from member where mem_id = %s',UserID)
        data = cursor.fetchone()
        if not(UserID and Password and Password2 and UserName and Zipcode and address1 and address2 and email and phoneNum) :
            return "<script>alert('빈공간이 존재합니다.'); history.back();</script>"
        if data is not None :
            return "<script>alert('중복된 ID입니다.'); history.back();</script>"
        if Password != Password2 :
            return "<script>alert('두 비밀번호가 일치하지 않습니다.'); history.back();</script>"

        # insert문
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""Insert into member
        (mem_id,pwd,name,address,tel,email,zip) values
        (%s,%s,%s,%s,%s,%s,%s)""",(UserID,Password,UserName,address,phoneNum,email,Zipcode))
        conn.commit()

        return render_template('index.html')

    elif button == "cancel" :
        return render_template('index.html')

    elif button == "verify" :
        cursor = mysql.connect().cursor()
        cursor.execute('select * from member where mem_id = %s',UserID)
        data = cursor.fetchone()
        if UserID =="":
            return """
                <script>alert('ID를 입력해주세요.'); history.back();</script>
            """

        if data is None :
            return """
            <script>alert('ID를 사용할 수 있습니다.'); history.back();</script>
            """

        else :
            return """
            <script>alert('ID를 이미 사용하고 있습니다.'); history.back();</script>
            """

@app.route('/login/', methods=['GET','POST']) # 완료
def login() :
    return render_template('login.html')

@app.route('/logout/', methods=['GET','POST']) # 완료
def logout() :
    session.pop('username', None)
    return redirect(url_for('home'))

# login DB 검사
@app.route('/Authenticate/',methods=['GET','POST']) # 완료
def Authenticate() :
    userID = request.form.get('ID')
    password = request.form.get('PW')

    cursor = mysql.connect().cursor()
    cursor.execute("Select * from member where mem_id = %s and pwd = %s",(userID,password))
    data = cursor.fetchone()

    if data is None :

         return """
         <script>alert('로그인에 실패했습니다.'); history.back();</script>
         """
    else :
         session['username'] = userID
         return render_template("index.html",username = userID)

# community 부분
@app.route('/community/',methods=['GET','POST']) # 완료
def community():
    if 'username' in session :
        username = session['username']
	cursor = mysql.connect().cursor()
	cursor.execute("Select * from board_table")
	data = cursor.fetchall()
        return render_template('community.html',username = username, data=data)
    else :
        return redirect(url_for('home'))

# community - writer 부분
@app.route('/community/write/', methods=['GET','POST']) # 완료
def writeBoard() :
    return render_template('writer.html')

# community - writer : 게시글 등록
@app.route('/community/write/db/',methods=['GET','POST']) # 완료
def writeDB() :
    button = request.values.get('button')
    if button == 'list' :
        return redirect(url_for('community'))
    elif button == 'cancel' :
        return redirect(url_for('community'))
    elif button =='writeOn' :
        UserID = session['username']
        subject = request.values.get('subject')
        content = request.values.get('content')
        password = request.values.get('password')
        if subject == '':
            return  "<script>alert('제목을 입력해주세요'); history.back();</script>"
        if content == '' :
            return  "<script>alert('내용을 입력해주세요'); history.back();</script>"
        if password == '' :
            return  "<script>alert('비밀번호를 입력해주세요'); history.back();</script>"
        # insert문
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""Insert into board_table
        (title, content, writer_id, password) values
        (%s,%s,%s,%s)""",(subject, content, UserID, password))
        conn.commit()

        return "<script>alert('게시글이 등록되었습니다.'); history.back();</script>"

# community - read 부분
@app.route('/coummunity/board/<number>') # 완료
def readBoard(number = None) :
    if number is None :
        return redirect('board.html')
    else :
        username = session['username']
        cursor = mysql.connect().cursor()
        cursor.execute("Select * from board_table where bd_num = %s",number)
        data = cursor.fetchall()
        if data is None :
            return """
            <script>alert('게시글이 존재하지 않습니다.'); history.back();</script>
            """
        else :
            # 조회수 상승
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("update board_table set hit=hit+1 where bd_num = %s",number)
            conn.commit()
            return render_template('read.html',username = username, data = data)

# button handler
@app.route('/read_btn/') # 완료
def read_btn() :
    # data read
    username = session['username']
    button = request.values.get('button')
    number = request.values.get('number')

    # switch : page redirection
    if button == "list" :
        return redirect(url_for('community'))

    elif button == "modify" :
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select * from board_table where bd_num = %s and writer_id = %s",(number,username))
        data = cursor.fetchone()
        if data is None :
            return "<script>alert('수정권한이 없습니다.'); history.back();</script>"
        return render_template('modify.html',username = username, number = number)

    elif button == "delete" :
        return render_template('delete.html',username = username, number = number)
    else :
        return redirect(url_for('community'))

# community - modify : 게시글 수정
@app.route('/community/modify/db/',methods=['GET','POST']) # 완료
def modifyDB() :
    button = request.values.get('button')

    if button == 'list' :
        return redirect(url_for('community'))
    elif button == 'cancel' :
        return redirect(url_for('community'))
    elif button =='modify' :
        UserID = session['username']
        number = request.values.get('number')
        subject = request.values.get('subject')
        content = request.values.get('content')
        password = request.values.get('password')

        if subject == '':
            return  "<script>alert('제목을 입력해주세요'); history.back();</script>"
        if content == '' :
            return  "<script>alert('내용을 입력해주세요'); history.back();</script>"
        if password == '' :
            return  "<script>alert('비밀번호를 입력해주세요'); history.back();</script>"

        # 비밀번호 확인
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("Select * from board_table where bd_num = %s and password = %s",
        (number,password))
        data = cursor.fetchall()
        if data is None :
            return "<script>alert('비밀번호가 틀립니다.'); history.back();</script>"

        # update문
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""update board_table set
        title = %s, content = %s
        where bd_num = %s
        """,(subject, content, number))
        conn.commit()
        return "<script>alert('게시글이 수정되었습니다.'); history.back();</script>"

# community - delete 부분
@app.route('/comunity/delete/')
def delete(number = None) :
    return render_template("delete.html",number=number)

# community - delete : 게시글 삭제
@app.route('/delete/')
def deleteDB() :
    button = request.values.get('button')
    number = request.values.get('num')
    if button == 'cancel' :
        return redirect(url_for('community'))
    elif button =='delete' :
        UserID = session['username']
        password = request.values.get('password')

        if password == '' :
            return  "<script>alert('비밀번호를 입력해주세요'); history.back();</script>"

        # 비밀번호 확인
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("Select * from board_table where bd_num = %s and password = %s",
        (number,password))
        data = cursor.fetchall()
        if data is None :
            return "<script>alert('비밀번호가 틀리거나 이미 게시글이 존재하지 않습니다.'); history.back();</script>"

        # delete문
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("delete from board_table where bd_num = %s", number)
        conn.commit()
        return "<script>alert('게시글이 삭제되었습니다.'); history.back();</script>"

# admin 부분
@app.route('/admin/',methods=['GET','POST'])
def admin() :
    if 'username' in session :
        username = session['username']
        return render_template('admin.html',username = username)
    else :
        return """
        <script>alert('로그인이 필요합니다.'); history.back();</script>
        """

@app.route('/admin_item/', methods=['GET','POST'])
def adminitem():
    if 'username' in session :
        username = session['username']
        return render_template('admin_item.html',username = username)
    else :
        return """
        <script>alert('로그인이 필요합니다.'); history.back();</script>
        """

@app.route('/admin_member/', methods=['GET','POST'])
def adminmember():
    if 'username' in session :
        username = session['username']
        return render_template('admin_member.html',username = username)
    else:
        return """
        <script>alert('로그인이 필요합니다.'); history.back();</script>
        """

@app.route('/admin_board/', methods=['GET','POST'])
def adminboard():
    if 'username' in session :
        username = session['username']
        return render_template('admin_board.html',username = username)
    else:
        return """
        <script>alert('로그인이 필요합니다.'); history.back();</script>
        """

# mypage 부분
@app.route('/mypage/',methods=['GET','POST'])
@app.route('/mypage/<username>',methods=['GET','POST'])
def mypage() :
    if 'username' in session :
        username = session['username']
        return render_template('mypage.html',username = username)
    else:
        return """
        <script>alert('로그인이 필요합니다.'); history.back();</script>
        """

@app.route('/my_order/',methods=['GET','POST'])
@app.route('/my_order/<username>',methods=['GET','POST'])
def myorder(username = None) :
    if 'username' in session :
        username = session['username']
        return render_template('my_order.html',username = username)
    else:
        return """
        <script>alert('로그인이 필요합니다.'); history.back();</script>
        """
@app.route('/my_revise/',methods=['GET','POST']) # 완료
@app.route('/my_revise/<username>',methods=['GET','POST'])
def myrevise(username = None) :
    if 'username' in session :
        username = session['username']
        return render_template('my_revise.html',username = username)
    else:
        return """
        <script>alert('로그인이 필요합니다.'); history.back();</script>
        """
# my_revise - 유효성 검사 후, 처리
@app.route('/vertify/', methods=['GET','POST']) # 확인 필요
def vertify() : # 1 : cancel, 2 : save, 3 : drop
    function = request.values.get('button')
    if function == '1' : # cancel
        return redirect(url_for('mypage'))
    elif function == '2' : # save
        # 정보 가져오기
        UserID = session['username']
        Password = request.values.get('password')
        Password2 = request.values.get('password2')
        UserName = request.values.get('name')
        Zipcode = request.values.get('zipcode')
        address1 = request.values.get('address1')
        address2 = request.values.get('address2')
        email = request.values.get('email')
        phoneNum = request.values.get('phonenum')
        address = address1
        address = address + " "
        address = address + address2

        # 유효성 확인 : password 유효성 검사만 추가하면됨
        if not(Password and Password2 and UserName and Zipcode and address and email and phoneNum) :
            return "<script>alert('빈공간이 존재합니다.'); history.back();</script>"
        if Password != Password2 :
            return "<script>alert('두 비밀번호가 일치하지 않습니다.'); history.back();</script>"

        # update문
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""update member set pwd = %s,
         name = %s, address = %s, tel = %s, email = %s,
         zip = %s where mem_id = %s""",(Password, UserName, address, phoneNum, email, Zipcode, UserID))
        conn.commit()
        return "<script>alert('수정이 완료되었습니다.'); history.back();</script>"
    elif function == '3' : # drop databases - 구현 필요
        session.pop('username',None)
        return "<script>alert('data 삭제.'); history.back();</script> "
    else :
        return errorhandler(404)

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(debug=True)
