import socket
import os
import sys
import time
import struct


class info_type():
    words=1
    voicecall=2
    file=3

class message:
    def __init__(self):
        self.type = 1
        self.text = ""
        self.srce = ""
        self.dest = ""
    def to_frame(self):
        return struct.pack('iiii',self.type, len(self.text), len(self.srce), len(self.dest)) + self.text.encode() + self.srce.encode() + self.dest.encode()


def send(_socket,text,srce,dest):
    _socket.sendall(text.encode("utf-8"))
    time.sleep(0.1)
    _socket.sendall(srce.encode("utf-8"))
    time.sleep(0.1)
    _socket.sendall(dest.encode("utf-8"))

def recv_msg(_socket):
    msg_type = 1
    text = _socket.recv(1024).decode("utf-8")
    srce = _socket.recv(1024).decode("utf-8")
    dest = _socket.recv(1024).decode("utf-8")
    msg = message()
    msg.type = msg_type
    msg.text = text
    msg.srce = srce
    msg.dest = dest
    return msg


def send_file(path,_socketf,offset):
    print("trying to send out file")
    time.sleep(0.5)
    try:
        filesize = os.path.getsize(path)
        filesize -= offset
        size = filesize
    except FileNotFoundError:
        print("--------NO SUCH FILE!--------")
        return False
    _socketf.send("heads up".encode())
    time.sleep(0.1)
    _socketf.send(f"{path}".encode())
    time.sleep(0.1)
    _socketf.send(str(filesize).encode())
    time.sleep(0.5)
    if True:
        with open(path, 'rb') as file:
            file.seek(offset)
            while 1:
                if (size != 0):
                    data = file.read(1024)
                if (size == 0):
                    print("all sent")
                    break
                _socketf.sendall(data)
                offset += len(data)
                size -= len(data)
        return True
    return False

def recv_file(_socketf):
    print("receive file thread running")
    headsup = _socketf.recv(1024).decode()
    print(headsup)
    if ( headsup == "heads up"):
        offset = 0
        flag = 1
        name = _socketf.recv(1024).decode()
        print(name)
        name = name.split('/')[-1]
        size = float(_socketf.recv(1024).decode())
        try:
            with open(name,'ab') as file:
                while 1:
                    if (size != 0.0):
                        data = _socketf.recv(1024)
                    if (size == 0.0):
                        print("ready to go")
                        break
                    #offset_data = data.split(b'|')
                    #offset = int(offset_data[0])
                    file.write(data)
                    offset += len(data)
                    size -= len(data)
                    print(size)
        except IOError:
            print("receive file error occurs")
        return (name,flag)
    elif ( headsup == "GET" ):
        flag = 0
        name = _socketf.recv(1024).decode("utf-8")
        print(_socketf.getsockname(),"want to get", name)
        send_file(name,_socketf,0)
        return (name,flag)
            

def receive_text(socket):
    msg_type = 1
    text = socket.recv(1024).decode("utf-8")
    srce = socket.recv(1024).decode("utf-8")
    dest = socket.recv(1024).decode("utf-8")
    msg = message()
    msg.type = msg_type
    msg.text = text
    msg.srce = srce
    msg.dest = dest
    return msg
#port = 8888
#client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##client_socket.connect(('localhost', port))
#text = input()
#dest = "u1"
#msg1 = build_msg(1,text,dest)
#send_msg(client_socket,msg1)