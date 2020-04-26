import socket
import pickle
import select
import time
import sys
import random


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = "localhost"
Port = 5001
server.connect((IP_address, Port))
trama_up={}
id=input("ID for the new ONT: ")
bandwith=input("BANDWITH for the new ONT: ")
priority=input("PRIORITY for the new ONT: ")
trama_up.update({id : [bandwith, priority]})

while True:
    sockets_list = [sys.stdin, server]
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
    for socks in read_sockets:
        if socks == server:
            message = socks.recv(4096)
            print(message)
        else:
            for i in range(0, random.randint(0, 1000)):
                server.send(pickle.dumps(trama_up))
                print("send"+str(trama_up))
                time.sleep(0.000125)
            time.sleep(random.randint(0, 10))
server.close()
