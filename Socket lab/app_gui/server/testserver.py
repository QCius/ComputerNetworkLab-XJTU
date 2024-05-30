import socket
import os
import sys
import time
import struct
import threading

global client_list
client_list = []

class info_type():
    words=1
    voicecall=2
    file=3

class message:
    def __init__(self):
        self.type = info_type
        self.text = ""
        self.srce = ""
        self.dest = ""
    def to_frame(self):
        return struct.pack('iiii',self.type, len(self.text), len(self.srce), len(self.dest)) + self.text.encode() + self.srce.encode() + self.dest.encode()

def receive_text(socket):
    msg_type, text_length, srce_length,dest_length = struct.unpack("iiii", socket.recv(16))
    text = socket.recv(text_length).decode()
    time.sleep(0.1)
    srce = socket.recv(srce_length).decode()
    dest = socket.recv(dest_length).decode()
    msg = message()
    msg.type = msg_type
    msg.text = text
    msg.srce = srce
    msg.dest = dest
    return msg

def recv(socket):
    usr = socket.recv(1024).decode()
    print(usr)
    pwd = socket.recv(1024).decode()
    print(pwd)
    socket.sendall("success".encode())

def build_msg(i,text,srce,dest):
    msg = message()
    msg.type = i
    msg.text = text
    msg.srce = srce
    msg.dest = dest
    return msg

def send(_socket, i, text, srce, dest):
    a = build_msg(i, text, srce, dest)
    send_msg(_socket,a)

def send_msg(_socket,msg):
    if (msg.type == 1):
        _socket.sendall(msg.to_frame())

def handle(client_socket):
    while 1:
        msg = receive_text(client_socket)
        print(msg.text , "sent to", msg.dest)
        for skt in client_list:
            send(skt,1,msg.text,msg.srce,"broadcast")
    
def handle_f(_socketf):
    dl_dir = "test.txt"
    offset = 0
    while 1:
        flag = 0
        try:
            with open(dl_dir, 'ab') as file:
                while 1:
                    data = _socketf.recv(1024)
                    print("receiving something")
                    if not data:
                        break
                    flag = 1
                    offset_data = data.split(b'|')
                    offset = int(offset_data[0])
                    file.write(offset_data[1])
        except IOError:
            print("something went wrong while downloading")
        if (flag == 1):
            try:
                with open(dl_dir, 'rb') as file:
                    file.seek(offset)
                    data = file.read(1024)
                    while data:
                        # 发送偏移量和数据
                        _socketf.sendall(str(offset).encode() + b'|' + data)
                        offset += len(data)
                        data = file.read(1024)
            except FileNotFoundError:
                print("File not found.")


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 19046))
server_socket.listen(5)
file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
file_socket.bind(('0.0.0.0', 19047))
file_socket.listen(5)
online_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
online_socket.bind(('0.0.0.0', 19048))
online_socket.listen(5)
print("Server started, listening on port 19046")
print("Server started, listening on port 19047")
while 1:
    client_socket, client_address = server_socket.accept()
    if (client_socket not in client_list):
        client_list.append(client_socket)
    print("{} has connected to us".format(client_address))
    recv(client_socket)
    p = threading.Thread(target= handle, args= (client_socket,))
    p.daemon = True
    p.start()
    f = threading.Thread(target= handle_f, args= (file_socket,))
    f.daemon = True
    f.start()
        
