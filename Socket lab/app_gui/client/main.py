from sendandrecv import *
from login_signup import *
from interfaces import *
import tkinter as tk
from tkinter import messagebox
import time

global _socket
global _socketf
global myname

def main():
    while 1:
        _socket = connect_to_server(19046)
        myaddr = (_socket.getsockname()[0],str(_socket.getsockname()[1]))
        print("my ip and port is",myaddr)
        time.sleep(1)
        #_socket.send("this is a test".encode())
        print("-----test-----")
        root = init_interface(_socket)
        root.mainloop()
        status = 1
        print("now we are in the main loop")
        _socketf = connect_to_server(19047)
        fileaddr = (_socketf.getsockname()[0],str(_socketf.getsockname()[1]))
        print("file addr is ", fileaddr)
        _socketol = connect_to_server(19048)
        _socketv = connect_to_server(19049)
        page = main_interface(_socket,_socketf,_socketol,_socketv)
        page.mainloop()

        while 1:
            if (status == 1):
                print("have we reached here?")
                time.sleep(100)
                #recv_thread = threading.Thread(target= receive_msg, args= (_socket,))
                #recv_thread.daemon = True
                #recv_thread.start()
            else:
                break



'''def main():
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
                    print("")
                try:
                    file_handler.join()
                except:
                    print("")
        client_socket.close()'''

if __name__ == "__main__":
    main()
