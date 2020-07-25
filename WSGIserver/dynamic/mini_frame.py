import re

URL_FUNC_DICT =dict()

def index():
    with open("./templates/index.html") as f:
        context = f.read()
    return context

def center():
    with open("./templates/center.html") as f:
        context = f.read()
    return context


URL_FUNC_DICT = {
    "/index.py" : index,
    "/center.py" : center
    }


def application(env,start_response_header):
    start_response_header("200 Ok",[("Content-Type","text/html;charset=utf-8"),("Connection", "keep-alive")])

    file_name = env["PATH_INFO"]

    # if file_name == "/index.py":        
    #     return index()
    # elif file_name == "/center.py":
    #     return center()

    func = URL_FUNC_DICT[file_name]
    return func()