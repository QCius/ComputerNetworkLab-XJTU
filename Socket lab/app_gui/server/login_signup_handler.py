import base64
import socket
import threading
import os
import time
import sqlite3
global users
usersl = {"u1": "1", "u2": "2"} 
def log_in(_socket):
    while 1:
        print("log in procedure")
        usrname = _socket.recv(1024).decode()
        print("usr=",usrname)
        time.sleep(0.1)
        passwrd = _socket.recv(1024).decode()
        print("pwd=",passwrd)
        time.sleep(0.1)
        if usrname in usersl:
            print("testpoint1")
            if (usersl[usrname] == passwrd):
                print("testpoint3")
                _socket.sendall("success".encode())
                break
            else:
                _socket.sendall("failure".encode())
        else:
            print("testpoint2")
            _socket.sendall("failure".encode())
    return usrname

def sign_up(_socket):
    print("sign up procedure")
    usrname = _socket.recv(1024).decode()
    passwrd = _socket.recv(1024).decode()
    _socket.sendall("success".encode())
    return (usrname,passwrd)