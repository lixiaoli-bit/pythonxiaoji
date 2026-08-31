print("脚本已启动")  # 放在 import 之前
from flask import Flask,render_template,request
import db

app = Flask(__name__)   # __name__ 当前模块

@app.route('/')
def hello():
    return render_template("e.html")

@app.route('/biaodan')
def biaodan():
    return  render_template("biaodan.html")


@app.route("/do_add_user", methods=['POST'])
def do_add_user():
    print(request.form)
    name = request.form.get("name")
    sex = request.form.get("sex")
    age = request.form.get("age")
    email = request.form.get("email")
    sql = f"""
        insert into user (name, sex, age, email)
        values ('{name}', '{sex}', {age}, '{email}')
    """
    print(sql)
    db.insert_or_update_data(sql)
    return "tianjia success"

# 展示数据库所有数据
@app.route("/show_users")
def show_users():
    sql = "select id,name from user"
    datas = db.query_data(sql)
    return render_template("show_users.html", datas=datas)

# 展示数据库单个详情
@app.route("/user/<user_id>")
def show_user(user_id):
    sql = "select * from user where id=" + user_id
    datas = db.query_data(sql)
    user = datas[0]
    return render_template("show_user.html", user=user)


if __name__ == '__main__':
    app.run(debug=True)