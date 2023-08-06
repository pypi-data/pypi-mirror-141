from socket import*

# server 

def server():
    server = socket.socket
    address=input("enter address  ")
    port=int(input("Enter Port : "))
    server.bind((address,port))
    server.listen()
    print("server listening...")
    connection,address = server.accept()
    print("connected to client...")

    while True:
        data = input("server : ")
        connection.send(bytes(data, 'utf-8'))
        recdata = connection.recv(1024).decode()
        print('client : ', recdata)
       

import socket

def host():
    s = socket.socket()
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    port = 1234
    s.bind((host, port))
    print(host, "(", ip, ")\n")




def client():
    client = socket()
    address = input("enter address : ")
    port = int(input("Enter Port : "))
    client.connect((address, port))
    print("connected to server..")
    
    while True:
        recdata = client.recv(1024).decode()
        print('server : ', recdata)
        data = input("client: ")
        client.send(bytes(data, 'utf-8'))



