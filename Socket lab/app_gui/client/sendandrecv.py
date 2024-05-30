import socket
import os
import sys
import time
import struct
import pyaudio


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
        return struct.pack('iiii',self.type, len(self.text), len(self.srce), len(self.dest)) + self.text.encode("utf-8") + self.srce.encode("utf-8") + self.dest.encode("utf-8")

'''def send_msg(_socket,msg):
    if (msg.type == 1):
        _socket.sendall(msg.to_frame())
    print(msg.to_frame())

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

def recv_msg(_socket):
    msg_type, text_length, srce_length, dest_length = struct.unpack("iiii", _socket.recv(16))
    text = _socket.recv(text_length).decode()
    time.sleep(0.1)
    srce = _socket.recv(srce_length).decode()
    dest = _socket.recv(dest_length).decode()
    msg = message()
    msg.type = msg_type
    msg.text = text
    msg.srce = srce
    msg.dest = dest
    return msg'''

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
    try:
        filesize = os.path.getsize(path)
    except FileNotFoundError:
        print("--------NO SUCH FILE!--------")
        return False
    _socketf.send("heads up".encode())
    time.sleep(0.1)
    _socketf.send(path.encode())
    time.sleep(0.1)
    _socketf.send(str(filesize).encode())
    time.sleep(0.5)
    if True:
        with open(path, 'rb') as file:
            file.seek(offset)
            data = file.read(1024)
            while data:
                _socketf.sendall(data)
                offset += len(data)
                data = file.read(1024)
        return True
    return False

def recv_file_(_socketf):
    print("receive file thread running")
    while 1:
        if (_socketf.recv(1024).decode() == "heads up"):
            #print("heads up")
            name = _socketf.recv(1024).decode()
            print(name)
            size = float(_socketf.recv(1024).decode())
            print(str(_socketf.getsockname()[1]))
            try:
                with open(name ,'ab') as file:
                    print("open")
                    while 1:
                        if (size != 0):
                            data = _socketf.recv(1024)
                        #offset_data = data.split(b'|')
                        #offset = int(offset_data[0])
                        if (size == 0):
                            #print("bye, file sending process")
                            break
                        file.write(data)
                        size -= len(data)
            except IOError:
                print("receive file error occurs")
        else:
            print("unknown")
            name = '/0'
        if (name != '/0'):
            return name

def voice(client_socket):
    p = pyaudio.PyAudio()
    input_device_info = p.get_default_input_device_info()
    input_device_index = input_device_info['index']
    print("Default input device:", input_device_info['name'])
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    input_device_index=input_device_index,
                    frames_per_buffer=1024)
    time.sleep(0.1)
    try:
        while True:                
            data = stream.read(1024) # 从麦克风读取音频数据
            client_socket.sendall(data)
            print("voice sending...")
    except KeyboardInterrupt:
        print("VOICE ERROR...")
        stream.stop_stream()
        stream.close()
        p.terminate()
        client_socket.close()
            
    return



def voice_recv(client_socket):
    p = pyaudio.PyAudio()
    output_device_info = p.get_default_output_device_info()
    output_device_index = output_device_info['index']
    print("Default output device:", output_device_info['name'])
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    output=True,
                    output_device_index=output_device_index,
                    frames_per_buffer=1024)
    try:
        while True:
            data = client_socket.recv(1024)
            print(f"recv voice data len = {len(data)}")
            if not data:
                break
            # 播放音频数据
            stream.write(data)

    except Exception as e:
        print("Error:", e)

    finally:
        print("Closing audio stream...")
        stream.stop_stream()
        stream.close()
        p.terminate()

#port = 8888
#client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##client_socket.connect(('localhost', port))
#text = input()
#dest = "u1"
#msg1 = build_msg(1,text,dest)
#send_msg(client_socket,msg1)