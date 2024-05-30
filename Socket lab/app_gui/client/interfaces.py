from sendandrecv import *
from login_signup import *
from tkinter.dnd import * 
import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import *
from enum import Enum
import multiprocessing
import base64
import socket
import threading
import os
import time


def init_interface(_socket):
    global root
    global login_page
    global signup_page
    global id_entry
    global id_entry2
    global pwd_entry
    global pwd_entry1
    global pwd_entry2
    root = tk.Tk()
    root.title("VVeChat")
    root.geometry("320x240+630+80")
    #log in page
    login_page = tk.Frame(root)
    id_frame = tk.Frame(login_page)
    id_frame.pack()
    id_label = tk.Label(id_frame,text="ID number:")
    id_label.pack(side="left")
    id_entry = tk.Entry(id_frame)
    id_entry.pack(side="left")
    pwd_frame = tk.Frame(login_page)
    pwd_frame.pack()
    pwd_label = tk.Label(pwd_frame,text="password:")
    pwd_label.pack(side="left")
    pwd_entry = tk.Entry(pwd_frame)
    pwd_entry.pack(side="left")
    btn_login = tk.Button(login_page, text="Log In", command=lambda: login_container(_socket,id_entry.get(),pwd_entry.get()))
    btn_login.pack()
    btn_signup = tk.Button(login_page, text="Sign up", command=lambda: show_signup())
    btn_signup.pack()
    #sign up page
    signup_page = tk.Frame(root)
    id_frame2 = tk.Frame(signup_page)
    id_frame2.pack()
    id_label = tk.Label(id_frame2,text="ID number:")
    id_label.pack(side="left")
    id_entry2 = tk.Entry(id_frame2)
    id_entry2.pack(side="left")
    pwd_frame1 = tk.Frame(signup_page)
    pwd_frame1.pack()
    pwd_label = tk.Label(pwd_frame1,text="password:")
    pwd_label.pack(side="left")
    pwd_entry1 = tk.Entry(pwd_frame1)
    pwd_entry1.pack(side="left")
    pwd_frame2 = tk.Frame(signup_page)
    pwd_frame2.pack()
    pwd_label = tk.Label(pwd_frame2,text="repeat password:")
    pwd_label.pack(side="left")
    pwd_entry2 = tk.Entry(pwd_frame2)
    pwd_entry2.pack(side="left")
    btn_login = tk.Button(signup_page, text="Sign up", command = lambda: signup_container(_socket,id_entry2.get(),pwd_entry1.get(),pwd_entry2.get()))
    btn_login.pack()
    btn_signup = tk.Button(signup_page, text="Log in", command = lambda: show_login())
    btn_signup.pack()
    #initialize
    signup_page.pack_forget()
    login_page.pack()
    return root

def signup_container(_socket, username, password, repeat):
    while 1:
        if ((password == repeat)&(signup(_socket,username,password))):
            id_entry2.delete(0, tk.END)
            pwd_entry1.delete(0, tk.END)
            pwd_entry2.delete(0, tk.END)
            root.destroy()
            print("haha")
        else:
            pwd_entry1.delete(0, tk.END)
            pwd_entry2.delete(0, tk.END)
            print("repeated password not identical,try again")


def login_container(_socket,username,password):
    while 1:
        if ((username != '')&(password != '')):
            if (login(_socket,username,password)):
                id_entry.delete(0, tk.END)
                pwd_entry.delete(0, tk.END)
                root.destroy()
                break
            else:
                id_entry.delete(0, tk.END)
                pwd_entry.delete(0, tk.END)
                print("try again")
                break

def show_login():
    signup_page.pack_forget()
    login_page.pack()

def show_signup():
    login_page.pack_forget()
    signup_page.pack()

def main_interface(_socket,_socketf,_socketol,_socketv):
    global page
    global entry
    global text
    global chat_page
    global file_page
    global entry_sv
    global entry5
    global user_list
    global file_list
    global download_list
    page = TkinterDnD.Tk()
    page.title("VVeChat Main Table")
    page.geometry("1280x640")
    #chat page
    chat_page = tk.Frame(page)
    chat_frame = tk.Frame(chat_page)
    chat_frame.pack(side=tk.LEFT, padx=10, pady=10)
    text = tk.Text(chat_frame)
    text.pack()
    text.tag_configure("green",foreground= "green")
    textbox_frame = tk.Frame()
    textbox_frame.pack(side=tk.BOTTOM)
    entry = tk.Entry(textbox_frame)
    entry.pack(side=tk.LEFT)
    entry.bind('<Return>', on_enter_press)
    button = tk.Button(textbox_frame, text="Send", command = lambda: send_msg(_socket,1,entry.get(),"u1","broadcast"))
    button.pack(side=tk.LEFT)

    recv_thread = threading.Thread(target= receive_msg, args= (_socket,))
    recv_thread.daemon = True
    recv_thread.start()

    recv_file = threading.Thread(target= recv_file_container, args= (_socketf,))
    recv_file.daemon = True
    recv_file.start()

    online_socket = threading.Thread(target= online_update, args= (_socketol,))
    online_socket.daemon = True
    online_socket.start()

    recv_handler =  threading.Thread(target= recv_voice_container, args= (_socketv,))
    recv_handler.daemon = True
    recv_handler.start()

    '''time.sleep(0.1)
    voice_handler =  threading.Thread(target= voice, args= (_socketv,))#bbb
    voice_handler.daemon = True
    voice_handler.start()'''

    print("Am I working")
    user_list_frame = tk.Frame(chat_page)
    user_list_frame.pack(side=tk.RIGHT, padx=10, pady=10)
    user_list_label = tk.Label(user_list_frame, text="currently online")
    user_list_label.pack()
    user_list = tk.Listbox(user_list_frame)
    user_list.bind("<Double-Button-1>", lambda event: voice_call_start(event, _socketv))
    user_list.pack()

    send_file = tk.Frame(chat_page)
    send_file.pack(side = tk.RIGHT)
    file_list = tk.Listbox(send_file)
    file_list.pack()
    file_list.bind("<Double-Button-1>", lambda event : download_file(event, _socketf))
    send_file_label = tk.Button(send_file, text = "send file", command = send_file_func)
    send_file_label.pack()
    chat_page.pack()

    # send_voice = tk.Frame(chat_page)
    # send_voice.pack(side = tk.RIGHT)
    # send_voice_label = tk.Button(send_voice, text = "send voice", command =send_voice_func)
    # send_voice_label.pack()
    # chat_page.pack()

    #file_page
    file_page = tk.Frame()
    entry_sv = tk.StringVar()
    entry5 = tk.Entry(file_page, textvar = entry_sv, width = 80)
    entry5.pack(fill = tk.X)
    entry5.drop_target_register(DND_FILES)
    entry5.dnd_bind('<<Drop>>', drop)
    send_btn = tk.Button(file_page, text= "send",command = lambda: send_file_and_return(_socketf))
    send_btn.pack(side=tk.BOTTOM)

    #voice_page

    return page

def on_enter_press(event):
    entry.insert(tk.END,'\n')

def download_file(event, _socketf):
    print("double click to download")
    file_name = file_list.get(file_list.curselection())
    _socketf.sendall("GET".encode("utf-8"))
    time.sleep(0.1)
    _socketf.sendall(str(file_name).encode("utf-8"))


def voice_call_start(event, _socketv):
    print("double click detected")
    voice_handler =  multiprocessing.Process(target= voice, args= (_socketv,))#bbb
    voice_handler.start()
    callee = user_list.get(user_list.curselection())
    calling_interface = tk.Toplevel(page)
    calling_interface.title("calling")
    exitbtn = tk.Button(calling_interface,text = "press to exit",command=lambda: exit_calling(voice_handler))
    exitbtn.pack()
    calling_interface.mainloop()
    #calling_interface.mainloop()

def exit_calling(handler_process):
    print("exit calling")
    handler_process.terminate()
    handler_process.join()
    print("calling terminated")


def recv_file_container(_socket):
    while 1:
        print("begin listening on file socket")
        name_ = recv_file_(_socket)
        file_list.insert(tk.END,name_)
        #print("I`ll be back on file socket")

def recv_voice_container(_socket):
    print("begin receiving voice")
    while 1:
        #print("begin listening on voice socket")
        voice_recv(_socket)

def online_update(_socketol):
    on = []
    print("begin listening on online users")
    while 1:
        rcv = _socketol.recv(1024).decode()
        if (rcv != "EOUL"):
            print(rcv)
            if (rcv not in on):
                on.append(rcv)
                user_list.insert(tk.END, rcv)
        else:
            print("end for this round")
        
def send_msg(_socket,i,text,srce,dest):
    if (text != ""):
        send(_socket,text,srce,dest)
        entry.delete(0, tk.END)
        print("sent ",text)
    else:
        print("can not send nothing")

def receive_msg(_socket):
    while 1:
        msg = recv_msg(_socket)
        text.insert(tk.END, msg.srce + ":    \n","green")
        text.insert(tk.END, msg.text + "\n")
        
def drop(event):
    entry_sv.set(event.data)

def send_file_func():
    chat_page.pack_forget()
    file_page.pack()
    page.title("drag file here")
    page.geometry("480x320")

'''def send_voice_func():
    chat_page.pack_forget()
    file_page.pack()
    page.title("drag file here")
    page.geometry("480x320")'''

def send_file_and_return(_socketf):
    while 1:
        print("uuu")
        time.sleep(0.5)
        path = entry5.get()
        offset = 0
        if (send_file(path,_socketf,offset)):
            print("successfully sent")
            break
        else:
            print("try again")
    file_page.pack_forget()
    chat_page.pack()
    page.title("VVeChat Main Table")
    page.geometry("960x640")


'''def receive_file(_socketf, _socket):
    dl_dir = str(_socket.getsockname()[1]) + '.txt'
    offset = 0
    while 1:
        try:
            with open(dl_dir, 'ab') as file:
                while 1:
                    data = _socketf.recv(1024)
                    if not data:
                        break
                    #offset_data = data.split(b'|')
                    #offset = int(offset_data[0])
                    file.write(data)
        except IOError:
            print("something went wrong while downloading")'''

#root = init_interface()
#page = main_interface()
#page.mainloop()