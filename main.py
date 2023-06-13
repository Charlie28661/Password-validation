from flask import Flask
from flask import request
from flask import render_template
from flask import render_template_string
import sqlite3

app = Flask(__name__)

#設定網頁路由
@app.route("/create", methods = ['GET', 'POST'])
def create():

    #連線資料庫
    connect = sqlite3.connect('database.db')
    sql = connect.cursor()

    #若傳輸協定為POST(網路概論內容)，則觸發下面判斷式
    if request.method == 'POST':

        #嘗試接收網頁回傳資料
        try:
            username = request.values["username"]
            password = request.values["password"]

        #若沒成功接收回傳"請輸入帳密"
        except:
            return render_template_string("請輸入帳密")
        
        #成功接收執行以下敘述
        else:

            #判斷回傳資料是否為空字串
            if len(username) == 0:
                return render_template_string("帳號請勿留白")
            if len(password) == 0:
                return render_template_string("密碼請勿留白")
            if len(username) and len(password) == 0:
                return render_template_string("帳號密碼請勿留白")
            
            #成功通過前面檢查則將回傳資料寫進資料庫
            sql.execute(f"INSERT INTO database (USERNAME, PASSWORD) VALUES ('{username}', '{password}')")
            connect.commit()

            #回傳資串"帳號創建完畢"
            return render_template_string("帳號創建完畢!")
        
    else:
        #將表單回傳到網頁上
        return'''
    <form method="post" action="/create">
        <p>創建帳號</p>
        <input type="text" name="username">
        <p>創建密碼</p>
        <input type="text" name="password">
        <input type="submit" name="submit" value="創建帳號">
    </form>
    '''

#設定網頁路由
@app.route("/login", methods = ['GET', 'POST'])
def login():
    
    #連線資料庫
    connect = sqlite3.connect('database.db')
    sql = connect.cursor()

    #若傳輸協定為POST(網路概論內容)，則觸發下面判斷式
    if request.method == 'POST':
        
        #嘗試接收網頁回傳資料
        try:
            username = request.values["username"]
            password = request.values["password"]

        #若沒成功接收回傳"請輸入帳密"
        except:
            return render_template_string("請輸入帳密")
        
        #成功接收執行以下敘述
        else:

            #判斷回傳資料是否為空字串
            if len(username) == 0:
                return render_template_string("帳號請勿留白")
            if len(password) == 0:
                return render_template_string("密碼請勿留白")
            if len(username) and len(password) == 0:
                return render_template_string("帳號密碼請勿留白")
            
            #驗證輸入是否等於資料庫存在的資料
            user = sql.execute(f"SELECT USERNAME FROM database WHERE USERNAME = '{username}' AND PASSWORD = '{password}'")

            #驗證資料庫中是否存在該項
            if user.fetchone() is None:
                return render_template_string("請輸入有效帳號密碼")

            #調出使用者輸入的帳號名稱
            user_name = user.fetchone()
            #導向welcome.html且在welcome.html上的username變數顯示使用者登入時輸入的帳號
            return render_template("welcome.html", username = user_name)

    return'''
    <form method="post" action="/login">
        <p>登入帳號</p>
		<input type="text" name="username">
        <p>登入密碼</p>
        <input type="text" name="password">
		<input type="submit" name="submit" value="登入">
	</form>'''


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
