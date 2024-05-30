import socket
import threading
import os
import sys
import time
import pyaudio

user = 0

def connect_to_server(port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('8.141.1.208', port))
    return client_socket


def login(client_socket):
    while True:
        print("--------------------------------------")
        print("--------------------------------------")
        print("--------------------------------------")
        print("-------- Welcome to chat room --------")
        username = input("--------Enter username: ")
        password = input("--------Enter password: ")
        client_socket.send(username.encode())
        client_socket.send(password.encode())
        global user 
        user = username
        response = client_socket.recv(1024).decode()
        print(f"--------{response}--------")
        print("---------------------------")
        return response == "Login successful"

def chat(client_socket):
    chat_recv_handler = threading.Thread(target = chat_recv, args = (client_socket,))
    chat_recv_handler.daemon = True
    chat_recv_handler.start()

    while True:
        sys.stdout.flush()
        message = input()
        if message.lower() == "quit":
            break
        else:
            print("you:",message)
            client_socket.send(message.encode())

def chat_recv(client_socket):
    while True:
        message = client_socket.recv(1024).decode()
        print(message)

def trans_file(username):

    client_socket_f = connect_to_server(6657)
    time.sleep(0.5)
    client_socket_f.send(f"{username}".encode())

    file_recv_handler = threading.Thread(target = file_recv, args = (client_socket_f,))
    file_recv_handler.daemon = True
    file_recv_handler.start()

    print("--------input file path you want to transfer:")
    path = input()
    if(send_file(client_socket_f, path)):
        print(f"--------{path} upload success--------")
    else:
        print(f"--------{path} upload failed--------")
    return


def send_file(client_socket, filename):
    try:
        filesize = os.path.getsize(filename)
    except FileNotFoundError:
        print("--------NO SUCH FILE!--------")
        return False
    print("te1")
    client_socket.send(f"{filename}".encode())
    client_socket.send(str(filesize).encode())
    print("te2")
    time.sleep(0.05) # 不能删去，否则服务器会来不及收到上面的包
    # message = str(client_socket.recv(1024).decode())  can not catch....
    print("--------uploading--------")
    if True:
        with open(filename, 'rb') as file:
            for data in file:
                client_socket.send(data)
        return True
    return False

def file_recv(client_socket):
    save_dir = "D:/"
    message = client_socket.recv(1024).decode()
    if message.startswith("Are you ready?"):
        print("t2")
        new_filename = (message.split("?")[1]).split("\\")[1]
        filesize = int(message.split("?")[2])
        client_socket.send("Ready to receive file".encode())
        file_path = f"{save_dir}{new_filename}"  
        print(f"filesize={filesize}")
        print(f"file_name = {new_filename}")
        print(f"file_path = {file_path}")
        with open(f"{save_dir}{new_filename}", 'wb') as file:
            while filesize > 0:
                data = client_socket.recv(1024)
                file.write(data)
                filesize -= len(data)
    return


def voice(user):
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

    client_socket = connect_to_server(9090)
    client_socket.send(f"{user}".encode())

    voice_recv_handler = threading.Thread(target = voice_recv, args = (client_socket,))
    voice_recv_handler.daemon = True
    voice_recv_handler.start()

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

# 主函数
def main():
    while True:
        client_socket = connect_to_server(8888)
        logged_in = login(client_socket)
        if logged_in:
            while True:
                print("--------input chat,file,voice or quit--------")
                print("--------input:")
                func_choose = input()
                if func_choose == "chat":
                    chat_handler = threading.Thread(target = chat, args = (client_socket,))
                    chat_handler.start()
                elif func_choose == "file":
                    global user
                    file_handler = threading.Thread(target = trans_file, args = (user,))
                    file_handler.start()
                elif func_choose == "voice":
                    voice_handler = threading.Thread(target = voice, args = (user,))
                    voice_handler.start()
                elif func_choose == "quit":
                    break
                else:
                    print("--------Wrong input--------")
                try:
                    chat_handler.join()
                except:
                    pass
                try:
                    file_handler.join()
                except:
                    pass
                try:
                    voice_handler.join()
                except:
                    pass
        client_socket.close()

if __name__ == "__main__":
    main()
