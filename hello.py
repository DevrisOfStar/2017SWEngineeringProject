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
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from board_table LIMIT 5")
    data = cursor.fetchall()
    cursor.execute("SELECT * FROM item_table LIMIT 6")
    item = cursor.fetchall()

    if 'username' in session :
        username = session['username']
    else :
        username = None
    return render_template('index.html',username = username, data=data, item=item)
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
         return redirect(url_for('home'))

# Search 부분
@app.route('/search', methods=['GET', 'POST']) #완료
def search():
    search_key=request.values.get('searchBar')
    if search_key == "" or search_key == None : # 애완용품 탭 + 검색어 입력을 하지 않았을 때,
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("select * from item_table")
            data = cursor.fetchall()
            return render_template('search_result.html', data=data)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM item_table WHERE item_name like %s" , ("%" + search_key + "%",))
    #cursor.execute("select * from item_table")
    data = cursor.fetchall()
    if data is None :
        return "<script>alert('검색결과가 없습니다.'); history.back();</script>"
    else :
        return render_template('search_result.html', search_key=search_key, data=data)

# 베스트 상품
@app.route('/search/best_product/',methods=['GET','POST']) # 완료
def bestproduct():
    if 'username' in session :
        username = session['username']
    else :
        return render_template('login.html')
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("Select * from item_table limit 6")
    data = cursor.fetchall()
    return render_template('search_result.html', username = username, data = data)

# 카테고리별 데이터 보여주기
@app.route('/search/category/<number>',methods=['GET','POST']) # 완료
def category(number = None) :
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM item_table WHERE item_id like %s" , (number + "%"))
    data = cursor.fetchall()
    if data is None :
        return "<script>alert('검색결과가 없습니다.'); history.back();</script>"
    else :
        return render_template('search_result.html', data = data)

# 상품 검색 결과 선택 부분
@app.route('/item_select/', methods=['Get','POST']) # 완료
def item_select() :
    button = request.values.get("button")
    number = request.values.get("number")

    if 'username' in session :
        username = session['username']
    else :
        username = None
    if button == "order" : # 장바구니 추가
        cost = request.values.get("cost")
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("insert into cart_table values (%s, %s, 1, %s)",(username,number,cost))
        conn.commit()
        return "<script>alert('장바구니에 추가하였습니다.'); history.back();</script>"
    elif button == "detail" :
        return item_detail(number = number)

# item detail 부분
@app.route('/item_detail/', methods=['GET','POST']) # 완료
def item_detail(number = None) :
    number = request.values.get("number")
    if number is None :
        return render_template('404.html')
    else : # 아이템 정보를 DB에서 가져옴
        cursor = mysql.connect().cursor()
        cursor.execute("Select * from item_table Where item_id = %s",number)
        data = cursor.fetchall()
        return render_template('item_detail.html',data = data)

@app.route('/item_order/', methods=['GET','POST']) # 완료
def order() : # 주문 - 결제 부분
    button = request.values.get('button')
    amount = request.values.get('amount') # 총계
    counts = request.values.get('counts') # 주문 개수
    item = request.values.get('item')
    if 'username' in session :
        username = session['username']
    else :
        return render_template('login.html')

    if button == "card" :
        return render_template('payment_card.html',amount=amount,username = username)
    if button == "bank" :
        return render_template('payment_bank.html',amount=amount,username = username)
    if button == "insert" :
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("update cart_table set amount = %s where item_id=%s and mem_id = %s",(counts,item,username))
        conn.commit()
        return "<script>alert('물품을 수정하였습니다.'); history.back();</script>"
    if button == "delete" :
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("delete from cart_table where item_id = %s and mem_id = %s",(item,username))
        conn.commit()
        return "<script>alert('물품을 삭제하였습니다.'); history.back();</script>"
    if button == "cancel" :
        return render_template('search_result.html')
    if button == "order" :
        return "<script>alert('취소를 누르고, 장바구니담기 버튼을 눌러주세요.'); history.back();</script>"


@app.route('/payment_card/', methods=['GET','POST']) # 구현 부족
def paymentcard() : # 결제 부분 - 카드결제 or 무통장입금
    cardnum_1 = request.values.get('cardnum_1')
    cardnum_2 = request.values.get('cardnum_2')
    cardnum_3 = request.values.get('cardnum_3')
    cardnum_4 = request.values.get('cardnum_4')
    cardcvc = request.values.get('cardcvc')
    cardmonth = request.values.get('cardmonth')

    button = request.values.get('button')
    if button == "cancel" :
        return render_template('mypage.html')

    if not (cardnum_1 and cardnum_2 and cardnum_3 and cardnum_4 and cardcvc and cardmonth) :
        return "<script>alert('빈공간이 존재합니다.'); history.back();</script>"
    else :
        return render_template('index.html')

@app.route('/payment_bank/',methods=['GET','POST']) # 구현 부족
def paymentbank() :
    name = request.values.get('name')
    button = request.values.get('button')
    if button == "cancel" :
        return render_template('mypage.html')

    if not (name) :
        return "<script>alert('빈공간이 존재합니다.'); history.back();</script>"
    else :
        return "<script>alert('계좌번호 : 123-456-7890 (국민)으로 입금부탁드립니다.'); history.back();</script>"
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
    if 'username' in session :
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

    else :
        return """
        <script>alert('로그인이 필요합니다.'); history.back();</script>
        """

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
        data = cursor.fetchall()
        if data is None :
            return "<script>alert('수정권한이 없습니다.'); history.back();</script>"
        return render_template('modify.html',username = username, number = number, data = data)

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
@app.route('/comunity/delete/') # 완료
def delete(number = None) :
    return render_template("delete.html",number=number)

# community - delete : 게시글 삭제
@app.route('/delete/') # 완료
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
@app.route('/admin/',methods=['GET','POST']) # 완료
def admin() :
    if 'username' in session :
        username = session['username']
        return render_template('admin.html',username = username)
    else :
        return """
        <script>alert('로그인이 필요합니다.'); history.back();</script>
        """

# item admin data db에서 가져와 페이지에 로드
@app.route('/admin_item/', methods=['GET','POST']) # 완료
def adminitem():
    if 'username' in session :
        username = session['username']
        cursor = mysql.connect().cursor()
        cursor.execute("Select * from item_table")
        data = cursor.fetchall()
        return render_template('admin_item.html',username = username, data = data)
    else :
        return """
        <script>alert('로그인이 필요합니다.'); history.back();</script>
        """

# admin item - 정보수정창으로 이동
@app.route('/admin_item/modify/',methods=['GET','POST']) # 완료
def modifyItem() :
    if 'username' in session :
        username = session['username']
        button = request.values.get('button')
        if button == 'itemDelete' :
            number = request.values.get('number')
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("delete from item_table where item_id = %s", number)
            conn.commit()
            return redirect('admin_item')


        elif button == 'itemDetail':
            number = request.values.get('number')
            cursor = mysql.connect().cursor()
            cursor.execute("Select * from item_table where item_id = %s", number)
            data = cursor.fetchall()
            return render_template('admin_item_detail.html',username = username, data=data)
        else:
            return render_template('admin_item.html',username = username)

# admin item - 등록창으로 이동
@app.route('/admin_item/register/',methods=['GET','POST']) # 완료
def registerItem() :
    if 'username' in session :
        username = session['username']
        return render_template('admin_item_register.html',username = username)
    else :
        return redirect('home')

# admin item - Item DB에 등록
@app.route('/admin_item/register_item/',methods=['GET','POST']) # 완료
def InsertItem() :
    button = request.values.get('button')
    if button == 'cancel' :
        return redirect('admin')
    # button  == 'save'

    ID = request.values.get('prodID')
    Name = request.values.get('prodName')
    Price = request.values.get('prodP')
    Counts = request.values.get('prodQ')
    Detail = request.values.get('prodD')
    # 유효성 확인 - 빈공간 및 Prmiary 중복 확인
    if not(ID and Name and Price and Counts and Detail) :
        return "<script>alert('빈공간이 존재합니다.'); history.back();</script>"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select * from item_table where item_id = %s", ID)
    data = cursor.fetchone()

    if data is None :
        # insert문
        conn2 = mysql.connect()
        cursor2 = conn2.cursor()
        cursor2.execute("""insert item_table values (%s, %s, %s, %s, %s)"""
         ,(ID, Name, Price, Detail, Counts))
        conn2.commit()
        return "<script>alert('등록이 완료되었습니다.'); history.back();</script>"
    else :
        return "<script>alert('상품번호가 이미 존재합니다.'); history.back();</script>"

# admin item - Item DB를 업데이트
@app.route('/admin_item/update/',methods=['GET','POST']) # 완료
def updateItem() :
    button = request.values.get('button')
    if button == 'cancel' :
        return redirect('/admin_item/')
    # button  == 'save'

    ID = request.values.get('prodID')
    Name = request.values.get('prodName')
    Price = request.values.get('prodP')
    Counts = request.values.get('prodQ')
    Detail = request.values.get('prodD')

    # 유효성 확인
    if not(ID and Name and Price and Counts and Detail) :
        return "<script>alert('빈공간이 존재합니다.'); history.back();</script>"

    # update문
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("""update item_table set item_name = %s,
     item_price = %s, item_info = %s, stock = %s where item_id = %s"""
     ,(Name, Price, Detail, Counts, ID))
    conn.commit()
    return redirect('admin_item')

# member admin data db에서 가져와 페이지에 로드
@app.route('/admin_member/', methods=['GET','POST']) # 완료
def adminmember():
    if 'username' in session :
        username = session['username']
        cursor = mysql.connect().cursor()
        cursor.execute("Select * from member")
        data = cursor.fetchall()
        return render_template('admin_member.html',username = username, data = data)
    else:
        return """
        <script>alert('로그인이 필요합니다.'); history.back();</script>
        """
# admin member - 주문정보 list 가져오기
@app.route('/admin_member/orderdetail',methods =['GET','POST']) # 완료
def adminorderdetail():
    if 'username' in session :
        username = session['username']
        Name = request.values.get('ID')
        cursor = mysql.connect().cursor()
        cursor.execute("Select * from orderlist_table where order_name = %s",(Name))
        data = cursor.fetchall()
        return render_template('member_orderDetail.html',username = username, data = data)
    else:
        return """
        <script>alert('로그인이 필요합니다.'); history.back();</script>
        """
# admin member - 주문 상태 업데이트
@app.route('/admin_member/update/',methods=['GET','POST']) # 완료
def updateOrder() :
    state = request.values.get("state")
    number = request.values.get("number")
    # 유효성 확인
    if not (state and number) :
        return "<script>alert('빈공간이 존재합니다.'); history.back();</script>"

    # update문
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("""update orderlist_table set state = %s
    where order_num = %s"""
     ,(state, number))
    conn.commit()
    return "<script>alert('수정이 완료되었습니다.'); history.back();</script>"

# board admin data db에서 가져와 페이지에 로드
@app.route('/admin_board/', methods=['GET','POST']) # 완료
def adminboard():
    if 'username' in session :
        username = session['username']
        cursor = mysql.connect().cursor()
        cursor.execute("Select * from board_table")
        data = cursor.fetchall()
        return render_template('admin_board.html',username = username,data = data)
    else:
        return """
        <script>alert('로그인이 필요합니다.'); history.back();</script>
        """

@app.route('/admin_board/modify/', methods=['GET','POST'])
def modifyadminboard() :
    if 'username' in session :
        username = session['username']
        number = request.values.get('number')
        conn=mysql.connect()
        cursor = conn.cursor()
        cursor.execute("delete from board_table where bd_num=%s",number)
        conn.commit()
        return redirect('admin_board')
    else:
        return """
        <script>alert('로그인이 필요합니다.'); history.back();</script>
        """

@app.route('/admin_board/process/', methods=['GET','POST'])
def processadminboard() :
    button = request.values.get('button')
    number = request.values.get('number')

    if button == "delete" :
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("delete from board_table where bd_num = %s",(number))
        conn.commit()
        return "<script>alert('삭제완료되었습니다.'); history.back();</script>"

    elif button == "modify" :
        title = request.values.get('subject')
        content = request.values.get('content')
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("update board_table set title = %s, content = %s where bd_num = %s",(title, content, number))
        conn.commit()
        return "<script>alert('수정완료되었습니다.'); history.back();</script>"


    elif button == "cancel" :
        return redirect(url_for('admin_board'))

# mypage 부분 - 완료
@app.route('/mypage/',methods=['GET','POST'])
@app.route('/mypage/<username>',methods=['GET','POST'])
def mypage() :
    if 'username' in session :
        username = session['username']
        amount = 0
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select * from cart_table, item_table where cart_table.item_id = item_table.item_id and cart_table.mem_id = %s",username)
        data = cursor.fetchall()
        data2 = data
        if data2 is not None :
            for row in data2 :
                amount = amount + row[2] * row[3]

        return render_template('mypage.html',username = username, data = data, amount = amount)
    else:
        return """
        <script>alert('로그인이 필요합니다.'); history.back();</script>
        """

# 주문번호별 리스트 보여주기
@app.route('/my_order/',methods=['GET','POST'])
@app.route('/my_order/<username>',methods=['GET','POST'])
def myorder(username = None) :
    if 'username' in session :
        username = session['username']
        cursor = mysql.connect().cursor()
        cursor.execute("Select * from orderlist_table where order_name = %s",(username))
        data = cursor.fetchall()
        return render_template('my_order.html',username = username, data = data)
    else:
        return """
        <script>alert('로그인이 필요합니다.'); history.back();</script>
        """

@app.route('/my_revise/',methods=['GET','POST']) # 완료
@app.route('/my_revise/<username>',methods=['GET','POST'])
def myrevise(username = None) :
    if 'username' in session :
        username = session['username']
        cursor = mysql.connect().cursor()
        cursor.execute("select * from member where mem_id = %s",username)
        data = cursor.fetchall()
        return render_template('my_revise.html',username = username, data=data)
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
    elif function == '3' :
        username = session['username']
        session.pop('username',None)

        # delete문
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("delete from member where mem_id = %s",(username))
        conn.commit()
        return "<script>alert('탈퇴가 완료되었습니다.'); history.back() </script> "
    else :
        return errorhandler(404)

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(debug=True)
