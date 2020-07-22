def index():
    return "hjahdfhah"

def login():
    return "jahhahahahhahhhh"

def application(env,start_response_header):
    start_response_header("200 Ok",[("Content-Type: text/html","charset=utf-8"),("Connection", "keep-alive")])

    file_name = env["PATH_INFO"]
    if file_name == "/index.py":
        index()
    elif file_name == "/login.py":
        login()
