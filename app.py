print("脚本已启动")  # 放在 import 之前
from flask import Flask,render_template,request,session, redirect, url_for
import pandas as pd
import db

app = Flask(__name__)   # __name__ 当前模块

@app.route('/')
def flbootstrap():
    return render_template('flbootstrap.html')

app.config["SECRET_KEY"] = 'sdafasfsafsafd'
@app.route('/fldenglu', methods=['POST','GET'])
def fldenglu():
    if request.method == "POST":
        # ctrl d
        user_name = request.form.get("email")
        password = request.form.get("password")
        if user_name == "18435992007@163.com" and password == "bsj1011521":
            session["user_name"] = "admin"
            return redirect(url_for("flbootstrap"))

    return render_template('fldenglu.html')

@app.route('/out')
def out():
    session.pop("user_name")
    return redirect(url_for("flbootstrap"))


@app.route("/flzhanshi")
def flzhanshi():
    
    if "user_name" not in session:
        return redirect(url_for("flbootstrap"))

    df = pd.read_excel("学生成绩表.xlsx")
    return render_template("flzhanshi.html",
                           table_html=df.to_html(classes="table table-hover table-sm"))


@app.route("/flluru", methods=["POST", "GET"])
def submit_grade():
    if "user_name" not in session:
        return redirect(url_for("flbootstrap"))

    if request.method == "POST":
        name = request.form.get("name")
        yuwen = request.form.get("yuwen")
        shuxue = request.form.get("shuxue")
        yingyu = request.form.get("yingyu")
        df = pd.read_excel("学生成绩表.xlsx")
        # 姓名	语文成绩	数学成绩	英语成绩
        new_row = pd.DataFrame({
            "姓名" : [name],
            "语文成绩" : [yuwen],
            "数学成绩" : [shuxue],
            "英语成绩" : [yingyu],
        })
        df = pd.concat([new_row, df])
        df.to_excel("学生成绩表.xlsx", index=False)
        return redirect(url_for("flzhanshi"))
    return render_template("flluru.html")


if __name__ == '__main__':
    app.run(debug=True)