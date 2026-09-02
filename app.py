# ============================================
# 第1步：导入需要的工具
# ============================================
from flask import Flask, send_from_directory  # Flask框架和文件下载功能
from db import query_data                      # 从db.py导入查询数据库的函数
import openpyxl                                # 操作Excel的工具
import os                                      # 处理文件和文件夹
from datetime import datetime                  # 获取当前时间（用来命名文件）

app = Flask(__name__)  # 创建Flask应用

# ============================================
# 第2步：设置下载文件夹
# ============================================
DOWNLOAD_DIR = 'downloads'  # 文件夹名字叫 downloads

# 检查这个文件夹存不存在
if not os.path.exists(DOWNLOAD_DIR):  # 如果不存在
    os.makedirs(DOWNLOAD_DIR)         # 就创建它


# ============================================
# 第3步：创建Excel的函数（核心）
# ============================================
def create_excel(data, table_name='user'):
    """
    这个函数的作用：把数据变成Excel文件，保存到硬盘上
    
    参数：
        data: 从数据库查出来的数据，格式是 [{'id':1, 'name':'张三'}, ...]
        table_name: 表名，用来给文件起名字
    
    返回：
        filename: 生成的文件名（比如 'user_20260831_223110.xlsx'）
    """
    
    # ----- 3.1 创建一个空白的Excel工作簿 -----
    wb = openpyxl.Workbook()  # 相当于新建一个Excel文件
    ws = wb.active            # 获取当前激活的工作表（默认叫Sheet1）
    
    # ----- 3.2 准备表头（第一行要写什么） -----
    # data[0] 是第一条数据，比如 {'id': 1, 'name': '张三', 'age': 25}
    # data[0].keys() 获取所有键，就是 ['id', 'name', 'age']
    headers = list(data[0].keys())  # 转成列表形式
    
    # ----- 3.3 写入表头（第1行） -----
    # enumerate 的作用：自动数数
    # 比如 headers = ['id', 'name', 'age']
    # 第1次循环：col=1, header='id'    → 在第1行第1列写 'id'
    # 第2次循环：col=2, header='name'  → 在第1行第2列写 'name'
    # 第3次循环：col=3, header='age'   → 在第1行第3列写 'age'
    #
    # 最终Excel第1行变成：  id  name  age
    for col, header in enumerate(headers, start=1):
        ws.cell(row=1, column=col, value=header)
        # ws.cell(行, 列, 值) 就是在Excel的指定位置写东西
    
    # ----- 3.4 写入数据（从第2行开始） -----
    # 外层循环：遍历每一条数据（每一行）
    # 比如 data = [
    #     {'id': 1, 'name': '张三', 'age': 25},   ← 第1条数据，写到第2行
    #     {'id': 2, 'name': '李四', 'age': 30},   ← 第2条数据，写到第3行
    #     {'id': 3, 'name': '王五', 'age': 28}    ← 第3条数据，写到第4行
    # ]
    #
    # enumerate(data, start=2) 的意思是：
    #   - 第1次循环：row_idx=2, row={'id':1, 'name':'张三', 'age':25}
    #   - 第2次循环：row_idx=3, row={'id':2, 'name':'李四', 'age':30}
    #   - 第3次循环：row_idx=4, row={'id':3, 'name':'王五', 'age':28}
    for row_idx, row in enumerate(data, start=2):
        # row_idx = 当前写到第几行（从2开始，因为第1行是表头）
        # row = 当前这条数据（是一个字典）
        
        # 内层循环：遍历当前数据的每个字段（每一列）
        # 以第1条数据 {'id': 1, 'name': '张三', 'age': 25} 为例：
        #   - 第1次内循环：col_idx=1, header='id'   → 在第2行第1列写 row['id']   → 写 1
        #   - 第2次内循环：col_idx=2, header='name' → 在第2行第2列写 row['name'] → 写 "张三"
        #   - 第3次内循环：col_idx=3, header='age'  → 在第2行第3列写 row['age']  → 写 25
        #
        # 最终Excel变成：
        #    A列(第1列)  B列(第2列)  C列(第3列)
        # 第1行  id         name        age        ← 表头
        # 第2行  1          张三        25         ← 第1条数据
        # 第3行  2          李四        30         ← 第2条数据
        # 第4行  3          王五        28         ← 第3条数据
        for col_idx, header in enumerate(headers, start=1):
            ws.cell(row=row_idx, column=col_idx, value=row[header])
            # row[header] 的意思：从字典里取值
            # 比如 row['id'] 就是 1，row['name'] 就是 "张三"
    
    # ----- 3.5 给文件起名字并保存 -----
    # datetime.now() 获取当前时间
    # strftime("%Y%m%d_%H%M%S") 把时间格式化成：年月日_时分秒
    # 比如 2026年8月31日22点31分10秒 → '20260831_223110'
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 拼凑文件名：表名_时间.xlsx
    # 比如 'user_20260831_223110.xlsx'
    filename = f'{table_name}_{timestamp}.xlsx'
    
    # 拼凑完整路径：'downloads/user_20260831_223110.xlsx'
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    
    # 保存Excel到硬盘
    wb.save(filepath)
    
    # 返回文件名（告诉调用者文件叫什么名字）
    return filename


# ============================================
# 第4步：下载路由（用户访问的网址）
# ============================================
@app.route('/download')  # 当用户访问 http://localhost:5000/download
def download():
    """用户访问这个网址就会下载Excel"""
    
    # 4.1 从数据库查询数据
    # query_data() 是 db.py 里的函数
    # 执行 "SELECT * FROM user" 查询user表所有数据
    data = query_data("SELECT * FROM user")
    # data 现在长这样：
    # [
    #   {'id': 1, 'name': '张三', 'sex': '男', 'age': 25, 'email': 'zhangsan@qq.com'},
    #   {'id': 2, 'name': '李四', 'sex': '女', 'age': 30, 'email': 'lisi@qq.com'}
    # ]
    
    # 4.2 调用上面的函数，创建Excel
    # 把数据传进去，告诉它表名叫 'user'
    filename = create_excel(data, 'user')
    # create_excel 会把Excel保存到 downloads/ 文件夹
    # 然后返回文件名，比如 'user_20260831_223110.xlsx'
    
    # 4.3 把文件发送给用户下载
    # send_from_directory(文件夹, 文件名, as_attachment=True)
    # 意思：从 downloads 文件夹里，找到 filename 这个文件
    # as_attachment=True 的意思是：强制弹出下载框，让用户保存
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)


# ============================================
# 第5步：启动程序
# ============================================
if __name__ == '__main__':
    app.run(debug=True)  # 运行Flask，debug=True表示出错时显示详细信息