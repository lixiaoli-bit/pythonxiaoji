print("脚本已启动")  # 放在 import 之前
from flask import Flask,render_template,request
import db

app = Flask(__name__)   # __name__ 当前模块

@app.route('/')
def hello():
    return 'nihao lixiaoli'



if __name__ == '__main__':
    app.run(debug=True)