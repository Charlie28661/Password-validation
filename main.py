from flask import Flask
from flask import request
from flask import render_template
from flask import render_template_string
import sqlite3

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return "歡迎你的到來"


@app.route("/create", methods = ['GET', 'POST'])
def create():

    connect = sqlite3.connect('database.db')
    sql = connect.cursor()

    if request.method == 'POST':
        try:
            username = request.values["username"]
            password = request.values["password"]
        except:
            return render_template_string("請輸入完整帳密")
        else:
            if len(username) == 0:
                return render_template_string("帳號請勿留白")
            if len(password) == 0:
                return render_template_string("密碼請勿留白")
            if len(username) and len(password) == 0:
                return render_template_string("帳號密碼請勿留白")
            sql.execute(f"INSERT INTO database (USERNAME, PASSWORD) VALUES ('{username}', '{password}')")
            connect.commit()
            return render_template_string("帳號創建完畢!")
            
    else:
        return'''
    <form method="post" action="/create">
        <p>創建帳號</p>
        <input type="text" name="username">
        <p>創建密碼</p>
        <input type="text" name="password">
        <input type="submit" name="submit" value="創建帳號">
    </form>
    '''


@app.route("/login", methods = ['GET', 'POST'])
def login():
    
    connect = sqlite3.connect('database.db')
    sql = connect.cursor()

    if request.method == 'POST':
        try:
            username = request.values["username"]
            password = request.values["password"]
        except:
            return render_template_string("請輸入完整帳密")
        else:
            if len(username) == 0:
                return render_template_string("帳號請勿留白")
            if len(password) == 0:
                return render_template_string("密碼請勿留白")
            if len(username) and len(password) == 0:
                return render_template_string("帳號密碼請勿留白")
            user = sql.execute(f"SELECT USERNAME FROM database WHERE USERNAME = '{username}' AND PASSWORD = '{password}'")
            user_name = user.fetchone()
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
