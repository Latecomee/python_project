import re
from pymysql import connect

"""
URL_FUNC_DICT = {
    "/index.html" : index,
    "/center.html" : center
    }
"""

URL_FUNC_DICT =dict()  # 字典用来保存server发过来需要访问的url做为key,相对应的value是要执行的函数.例如:{"/index.html" : index}

# 路由功能,在函数执行之前给字典添加内容.
def route(url):
    def set_func(func):
        URL_FUNC_DICT[url]=func
        def call_func(*args,**kwargs):
            return func(*args,**kwargs)
        return call_func
    return set_func
    

# 首页的处理函数
@route("/index.html")
def index(ret):
    with open("./templates/index.html") as f:
        content = f.read()

    conn = connect(host="localhost",port=3306,user='root',password="123456",database="stock_db",charset="utf8")
    cs = conn.cursor()
    cs.execute("select * from info;")
    stock_infos = cs.fetchall()
    cs.close()
    conn.close()

    html_template = """
    <tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>
            <input type="button" value="添加" id="toAdd" name="toAdd" >
        </td>
    </tr>
    """ 
    html_at = ""
    for line_info in stock_infos:
        print("*"*50)
        html_at += html_template % (line_info[0],line_info[1],line_info[2],line_info[3],line_info[4],line_info[5],line_info[6],line_info[7])

    # content = re.sub(r"\{%content%\}",str(stock_infos),content)
    content = re.sub(r"\{%content%\}", html_at, content)
    return content


@route("/center.html")
def center(ret):
    with open("./templates/center.html") as f:
        content = f.read()

    conn = connect(host="localhost",port=3306,user='root',password="123456",database="stock_db",charset="utf8")
    cs = conn.cursor()
    cs.execute("select i.code,i.short,i.chg,i.turnover,i.priece,i.highs,f.code from info as i inner join focus as f on i.id=f.info_id;")
    stock_infos = cs.fetchall()
    cs.close()
    conn.close()

    html_template = """
    <tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>
            <a type="button" class="btn btn-default btn-xs" href="/update/300268.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
        </td>
        <td>
            <input type="button" value="添加" id="toAdd" name="toAdd" >
        </td>
    </tr>
    """ 
    html_at = ""
    for line_info in stock_infos:
        print("*"*50)
        html_at += html_template % (line_info[0],line_info[1],line_info[2],line_info[3],line_info[4],line_info[5],line_info[6])

    content = re.sub(r"\{%content%\}", html_at, content)
    return content


""" 
* 给路由参数添加正则表达式的原因:
* 在实际开发中,url中往往会带有很多的参数,如果没有正则的话,那么就需要写很多函数来对url进行处理. 例如/add/0003.html中的0003就是参数,
* 后面还会有0004,0005,... 如果每个url都要写进字典,还要写函数,即不方便又不灵活. 此时正则可以很好的解决此类问题.
"""
@route(r"/add/(\d+)\.html")
def add_focus(ret):
    return "add Ok ....."


def application(env,start_response_header):
    start_response_header("200 Ok",[("Content-Type","text/html;charset=utf-8"),("Connection", "keep-alive")])

    file_name = env["PATH_INFO"]

    # if file_name == "/index.py":        
    #     return index()
    # elif file_name == "/center.py":
    #     return center()

    try:  
        # return URL_FUNC_DICT[file_name]()
        for url, func in URL_FUNC_DICT.items():
            ret = re.match(url,file_name)
            if ret:
                return func(ret)
            else:
                return "请求的url(%s)没有对应的函数...." % file_name
    except Exception as e:
        return "产生异常: %s" % e
