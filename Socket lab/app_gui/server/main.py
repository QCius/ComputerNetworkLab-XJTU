from login_signup_handler import *
from sendandrecv import *
import time
import sqlite3

def main():
    global online_clients
    global notify_list
    global sockets
    global f_list
    global v_list
    global addr_to_usrname
    global addr
    global file_list
    file_list = []
    online_clients = {}
    sockets = []
    notify_list = []
    unsent_list = []
    sent_list = []
    addr_to_usrname = {}
    addr = []
    f_list = []
    v_list = []
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 19046))
    server_socket.listen(5)
    file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    file_socket.bind(('0.0.0.0', 19047))
    file_socket.listen(5)
    online_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    online_socket.bind(('0.0.0.0', 19048))
    online_socket.listen(5)
    voice_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    voice_socket.bind(('0.0.0.0', 19049))
    voice_socket.listen(5)

    print("Server started, listening on port 19046")
    print("Server started, listening on port 19047")
    print("Server started, listening on port 19048")
    print("Server started, listening on port 19049")

    while 1:
        client_socket, client_address = server_socket.accept()
        #if (client_socket not in online_clients):
            #online_clients.append(client_socket)
        print("{} has connected to us".format(client_address))
        i = log_in_sign_up(client_socket)
        addr_to_usrname[client_address] = i
        online_clients[i] = client_socket
        unsent_list.append(i)
        addr.append(client_address)
        sockets.append(client_socket)
        client_socketf, client_addressf = file_socket.accept()
        f_list.append(client_socketf)
        print("{} has connected to file system".format(client_addressf))
        client_socketol, client_addressol = online_socket.accept()
        print("{} has connected to online notice".format(client_addressol))
        notify_list.append(client_socketol)
        p = threading.Thread(target= handle, args= (client_socket,))
        p.daemon = True
        p.start()
        f = threading.Thread(target= handle_f, args= (client_socketf,))
        f.daemon = True
        f.start()
        time.sleep(0.2)
        for skt in notify_list:
            notify(skt, online_clients, sent_list)
            print("notify once")
        #t = threading.Thread(target= notify, args= (online_socket, online_clients))

        
        client_socketv, client_addressv = voice_socket.accept()
        print("voice socket established")
        v_list.append(client_socketv)
        print("{} has connected to voice system".format(client_addressv))
        v = threading.Thread(target= handle_v, args= (client_socketv,))
        v.daemon = True
        v.start()

def handle_v(client_socketv):
    CHUNK = 1024
    print("voice_trans handleing")
    print("voice_trans handleing t0")
    try:
        while True:
            # 接收音频数据
            print("voice_trans handleing t1")
            data = client_socketv.recv(CHUNK)
            for socket in v_list:
                if socket != client_socketv:
                    socket.send(data)
                    print(f"voice data sending ,len = {len(data)}")
            if not data:
                break
            
    except Exception as e:
        print("Error:", e)
    finally:
        print("Closing audio stream...")

def notify(_socket, unsent_list, sent_list):
    for client in unsent_list:
        if (1):
            _socket.send(client.encode())
            time.sleep(0.1)
            sent_list.append(client)
    _socket.send("EOUL".encode())

def log_in_sign_up(_socket):
    command = _socket.recv(1024).decode()
    print(command)
    flag = 0
    if (command == "1"):
        flag = 1
        usr = log_in(_socket)
        return usr
    elif (command == "2"):
        flag = 2
        usr,pwd = sign_up(_socket)
        return usr
    else:
        print("ERROR")

def handle(client_socket):
    while 1:
        msg = receive_text(client_socket)
        print("receive",msg.text)
        for skt in sockets:
#if skt != client_socket:
            #for key in addr:
                #if (msg.srce == key):
            send(skt,msg.text,msg.srce,"broadcast")
            print(msg.text , "sent to", msg.dest)
            
    
def handle_f(_socketf):
    while 1:
        flag = 0
        (name, flag) = recv_file(_socketf)
        print("save file")
        if flag == 1:
            for sock in f_list:
                print("send file to",sock.getsockname())
                send_file(name,sock,0)
        else:
            print("sent elsewhere")


if __name__ == "__main__":
    main()