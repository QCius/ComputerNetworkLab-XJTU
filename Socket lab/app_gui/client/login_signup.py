import base64
import socket
import threading
import os
import time

def connect_to_server(port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('8.141.1.208', port))
    return client_socket

def login(_socket,username,password):
    while True:
        _socket.sendall("1".encode())
        print("usrname: ",username)
        print("passwrd: ",password)
        time.sleep(0.1)
        _socket.sendall(username.encode())
        time.sleep(0.1)
        _socket.sendall(password.encode())
        global user 
        user = username
        response = _socket.recv(1024).decode()
        print(response)
        return (response == "success")
        
def signup(_socket,username,password):
    while True:
        _socket.sendall("2".encode())
        print("You are signing up as:")
        print("usrname: ",username)
        print("passwrd: ",password)
        _socket.sendall(username.encode())
        _socket.sendall(password.encode())
        global user 
        user = username
        response = _socket.recv(1024).decode()
        print(response)
        return (response == "success")