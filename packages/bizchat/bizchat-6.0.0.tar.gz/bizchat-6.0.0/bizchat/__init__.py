
from socket import*
import socket


def server():
    
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(hostname, local_ip)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = input("enter address  ")
    port = int(input("Enter Port : "))
    server.bind((address, port))
    server.listen()
    print("server listening...")
    connection, address = server.accept()
    print("connected to client...")

    while True:
        data = input("server : ")
        connection.send(bytes(data, 'utf-8'))
        recdata = connection.recv(1024).decode()
        print('client : ', recdata)




def client():
    client = socket.socket()
    address = input("enter address : ")
    port = int(input("Enter Port : "))
    client.connect((address, port))
    print("connected to server..")
    
    while True:
        recdata = client.recv(1024).decode()
        print('server : ', recdata)
        data = input("client: ")
        client.send(bytes(data, 'utf-8'))



