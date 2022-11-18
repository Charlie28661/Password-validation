from flask import Flask
from flask import request
from flask import render_template

import datetime
import json

app = Flask(__name__)

today = datetime.datetime.today()
print('程式已成功運行!\n運行時間為:' + today.ctime())


@app.route("/")
@app.route("/index")
def index():
    return "歡迎你的到來"


@app.route("/create", methods = ['GET', 'POST'])
def create():
    if request.method == 'POST':
        create_user = request.values["createuser"]
        create_pw = request.values["createpw"]
        create = {
            "username" : create_user,
            "password" : create_pw
        }
    
        with open('datebase.json', mode = 'w', encoding = 'utf-8') as datebase:
            json.dump(create, datebase, indent=4)
            return "帳號創建完畢!"
    else:
        return'''
    <form method="post" action="/create">
        <p>創建帳號</p>
        <input type="text" name="createuser">
        <p>創建密碼</p>
        <input type="text" name="createpw">
        <input type="submit" name="submit" value="send">
    </form>
        '''


@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.values["name"]
        pw = request.values["pw"]
        with open('datebase.json', mode = 'r', encoding = 'utf-8') as datebase:
            date = json.load(datebase)
        if name == (date["username"]) and pw == (date["password"]):
            return render_template("admin.html")
        else:
            return "帳號或密碼錯誤！"
    return'''
    <form method="post" action="/login">
        <p>登入帳號</p>
		<input type="text" name="name">
        <p>登入密碼</p>
        <input type="text" name="pw">
		<input type="submit" name="submit" value="send">
	</form>'''


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
