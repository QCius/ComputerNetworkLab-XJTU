import socket
import threading
import os
import time

# 存储已连接的客户端信息
clients = {}
clientfs= {}
clientvs= {}
# 存储已登录的用户名和密码
users = {"u1": "1", "u2": "2"}  # 在实际应用中应使用更安全的存储方式

# 处理客户端连接
def handle_client(client_socket, client_address):
    username = client_socket.recv(1024).decode()  # 接收客户端发送的用户名
    password = client_socket.recv(1024).decode()  # 接收客户端发送的密码

    if username in users and users[username] == password:
        client_socket.send("Login successful".encode())
        clients[username] = client_socket
        print(f"{username} connected from {client_address}")
        listen_for_messages(username)
    else:
        client_socket.send("Invalid username or password".encode())
        client_socket.close()

# 监听客户端消息
def listen_for_messages(username):
    client_socket = clients[username]
    while True:
        try:
            message = client_socket.recv(1024).decode()
            broadcast_message(username,message)
        except Exception as e:
            print(f"Exception occurred: {e}")
            print(f"{username} excep happen ...NOTE!!")
            break
            

# 广播消息给所有客户端
def broadcast_message(sender, message):
    for username, client_socket in clients.items():
        if username != sender:
            client_socket.send(f"{sender}: {message}".encode())



def handle_client_f(client_socket_f, client_address_f):
    print("file_trans handleing test0")
    username = str(client_socket_f.recv(1024).decode())
    print("file_trans handleing test1")
    clientfs[username] = client_socket_f
    print(f"{username} connected from {client_address_f} to server port 6657 to handle file")
    path = str(client_socket_f.recv(1024).decode())
    print(f"file_trans handleing test2  here know path = {path}")
    filesize = int(client_socket_f.recv(1024).decode())
    print("file_trans handleing test3 here know filesize = {filesize}")
    size = filesize
    time.sleep(0.2)
    client_socket_f.send("Ready to receive file".encode())
    print("file_trans handleing test4")
    
    with open(path, 'wb') as file:
        while size > 0:
            data = b''
            data = client_socket_f.recv(1024)
            file.write(data)
            size -= len(data)
    print("file_trans handleing test5")
    for user_loop, client_socket_loop in clientfs.items():
        if user_loop !=username:
            target_socket = client_socket_loop
            client_socket_loop.send(f"Are you ready?{path}?{filesize}".encode())
    # file_to_send_message = target_socket.recv(1024).decode()
    if True: # if file_to_send_message == "Ready to receive file"
        print("!! try to send data")
        for user, client_socket in clientfs.items():
            if user != username:
                with open(path, 'rb') as file:
                    for data in file:
                            client_socket.send(data)
                            print(f"data sending ,len = {len(data)}")

def file_thread(server_socket_f):
    while True:
        client_socket_f, client_address_f = server_socket_f.accept()
        client_handler_f = threading.Thread(target=handle_client_f, args=(client_socket_f, client_address_f))
        client_handler_f.start()

def handle_client_v(client_socket_v, client_address_v):
    CHUNK = 1024
    print("voice_trans handleing")
    username = str(client_socket_v.recv(1024).decode())
    broadcast_message(username, "want to voice, input quit and then input voice to accept.")
    clientvs[username] = client_socket_v
    print("voice_trans handleing t0")
    try:
        while True:
            # 接收音频数据
            print("voice_trans handleing t1")
            data = client_socket_v.recv(CHUNK)
            for user, client_socket in clientvs.items():
                if user != username:
                    client_socket.send(data)
                    print(f"voice data sending ,len = {len(data)}")
            if not data:
                break
            
    except Exception as e:
        print("Error:", e)
    finally:
        print("Closing audio stream...")


def voice_thread(server_socket_v):
    while True:
        client_socket_v, client_address_v = server_socket_v.accept()
        client_handler_v = threading.Thread(target=handle_client_v, args=(client_socket_v, client_address_v))
        client_handler_v.start()

# 主函数
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8888))
    server_socket.listen(5)
    print("Server started, listening on port 8888")

    server_socket_f = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_f.bind(('0.0.0.0', 6657))
    server_socket_f.listen(5)
    print("Server started, listening on port 6657")

    server_socket_v = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_v.bind(('0.0.0.0', 9090))
    server_socket_v.listen(5)
    print("Server started, listening on port 9090")

    while True:
        handle_file_thread = threading.Thread(target=file_thread, args=(server_socket_f,))
        handle_file_thread.start()

        handle_voice_thread = threading.Thread(target=voice_thread, args=(server_socket_v,))
        handle_voice_thread.start()

        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

    

if __name__ == "__main__":
    main()
