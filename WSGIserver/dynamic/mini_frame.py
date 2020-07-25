import re
from pymysql import connect

"""
URL_FUNC_DICT = {
    "/index.html" : index,
    "/center.html" : center
    }
"""

URL_FUNC_DICT =dict()

def route(PATH):
    def set_func(func):
        URL_FUNC_DICT[PATH]=func
        def call_func(*args,**kwargs):
            return func(*args,**kwargs)
        return call_func
    return set_func


@route("/index.html")
def index():
    with open("./templates/index.html") as f:
        content = f.read()

    conn = connect(host="localhost",port=3306,user='root',password="123456",database="stock_db",charset="utf8")
    cs = conn.cursor()
    cs.execute("select * from info;")
    stock_infos = cs.fetchall()
    cs.close()
    conn.close()

    content = re.sub(r"\{%content%\}",str(stock_infos),content)
    return content


@route("/center.html")
def center():
    with open("./templates/center.html") as f:
        context = f.read()
    return context


def application(env,start_response_header):
    start_response_header("200 Ok",[("Content-Type","text/html;charset=utf-8"),("Connection", "keep-alive")])

    file_name = env["PATH_INFO"]

    # if file_name == "/index.py":        
    #     return index()
    # elif file_name == "/center.py":
    #     return center()
    try:  
        return URL_FUNC_DICT[file_name]()
    except Exception as e:
        return "产生异常: %s" % e
