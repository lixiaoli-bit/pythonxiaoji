print("脚本已启动")  # 放在 import 之前
from flask import Flask,render_template,request
from db import query_data  # 导入你写好的查询函数
import db

from pyecharts.charts import Bar, Pie, Line

from pyecharts import options as opts

app = Flask(__name__)   # __name__ 当前模块


@app.route('/')
def hello():
    return render_template("e.html")


@app.route("/show_pyecharts")          # 第1行：路由装饰器
def show_pyecharts():                  # 第2行：视图函数
    bar = (                     # 第3行：创建图表对象
        Bar()                     # 第4行：实例化柱状图
        .add_xaxis(["苹果", "香蕉", "橘子"])   # 第5行：设置横轴
        .add_yaxis("销量", [50, 80, 30])       # 第6行：设置纵轴
        .set_global_opts(title_opts=opts.TitleOpts(title="水果销量"))  # 第7行：设置标题
    )                            # 第8行：括号结束
    return render_template(
        "show_pyecharts.html",
        bar_options=bar.dump_options_with_quotes()  # ✅ 用这个
    )



def get_pie() -> Pie:
    sql = """
        select sex,count(1) as cnt from user group by sex
    """
    datas = db.query_data(sql)
    c = (
        Pie()
            .add("", [(data['sex'], data['cnt']) for data in datas])
            .set_global_opts(title_opts=opts.TitleOpts(title="Pie-基本示例"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return c


def get_bar() -> Bar:
    sql = """
            select sex,count(1) as cnt from user group by sex
        """
    datas = db.query_data(sql)
    c = (
        Bar()
            .add_xaxis([data['sex'] for data in datas])
            .add_yaxis("数量", [data['cnt'] for data in datas])
            .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return c

@app.route("/show_myecharts")
def show_myecharts():
    pie = get_pie()
    bar = get_bar()
    return render_template("show_myecharts.html",
                           pie_options=pie.dump_options_with_quotes(),
                           bar_options=bar.dump_options_with_quotes())


if __name__ == '__main__':
    app.run(debug=True)