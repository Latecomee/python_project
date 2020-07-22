import socket
import re
import multiprocessing
import time
import mini_frame

class mini_server(object):

    def __init__(self):
        # 创建套接字
        self.tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        # 绑定端口
        self.tcp_socket.bind(("",7788))
        # 将套接字设为监听模式
        self.tcp_socket.listen(128)

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
            body = mini_frame.application(env, self.set_response_hearders)
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
    t = mini_server()
    t.run_forever()


if __name__ == "__main__":
    main()
