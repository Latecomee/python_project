import socket
import re
import multiprocessing
import time
import sys

class mini_server(object):

    def __init__(self,port,app):
        # 创建套接字
        self.tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        # 绑定端口
        self.tcp_socket.bind(("",port))
        # 将套接字设为监听模式
        self.tcp_socket.listen(128)
        self.application = app

    def server_to_client(self,new_client_socket):
        '''处理client发过的数据,根据需求回发内容'''
        # 接收数据
        request = new_client_socket.recv(1024).decode("utf-8")
        print(request)
        # 分片接收到的表头,提取client的请求
        reqest_lines = request.splitlines()
        # GET / HTTP/1.1
        ret = re.match(r"[^/]+(/[^ ]*)",reqest_lines[0])
        if ret:
            file_name = ret.group(1)

        if not file_name.endswith(".py"):
            try:
                f = open("./html"+file_name,"rb")
            except:
                print("404 ---- 没找到这个网页 ----")
            else:
                context_text = f.read()
                f.close()
                # 准备表头和内容
                response = "HTTP/1.1 200 OK\r\n"
                response += "\r\n"
                new_client_socket.send(response.encode("utf-8"))
                new_client_socket.send(context_text)
        else:
            env = dict()  # 这个字典存放的是web服务器要传给client的内容的路径
            env["PATH_INFO"] = file_name
            body = self.application(env, self.set_response_hearders)
            response_header = "HTTP/1.1 "+ self.statu + "\r\n"
            for temp in self.header:
                response_header += "%s:%s\r\n" % (temp[0],temp[1])
            response_header += "\r\n"
            context_text = response_header + body
            new_client_socket.send(context_text.encode("utf-8"))

        # 关闭监听到的新套接字
        new_client_socket.close()

    def set_response_hearders(self,statu,header):
        self.statu = statu
        self.header = [("Server","mini_server v1.0")]
        self.header += header

    def run_forever(self):
        while  True:
            # accept接收套接字
            new_client_socket, client_Addr= self.tcp_socket.accept()
            # 将套接字传给server_to_client()进行数据处理
            self.server_to_client(new_client_socket)
            # # 创建多进程
            # p = multiprocessing.Process(target = self.server_to_client,args=(new_client_socket,))
            # p.start()

            # # 关闭主进程的client套接字,让子进程运行结束就释放资源
            # new_client_socket.close()

        # 关闭套接字
        self.tcp_socket.close()


def main():
    """整体控制,创建对象"""
    if len(sys.argv)==3:
        try:
            port = int(sys.argv[1])  # 端口
            frame_app_name = sys.argv[2]  # mini_server:application
        except:
            print("端口输入错误!请重新输入")
            return
    else:
        print("输入参数有误,请按照一下方式执行程序1:")
        print("python3 web_server.py 7788 mini_server:application")
        return

    ret = re.match(r"([^:]+):(.*)",frame_app_name)
    if ret:
        frame_name = ret.group(1)  # mini_server
        app_name = ret.group(2)  # application
    else:
        print("输入参数有误,请按照一下方式执行程序:")
        print("python3 web_server.py 7788 mini_server:application")
        return

    sys.path.append("./dynamic")  # 为了让__import__()函数找到 mini_server.py
    "import frame_name  # 此时import会将frame_name视为模块名,试图导入frame_name模块,而非frame_name保存的内容"
    frame = __import__(frame_name)  # 返回值标记这个导入的模块
    app = getattr(frame,app_name)  # 此时app指向了dynamic/mini_server模块中的application这个函数

    t = mini_server(port,app)
    t.run_forever()


if __name__ == "__main__":
    main()
