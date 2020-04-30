import socket
import pickle
import select
import sys
import os
import random
import string

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = "localhost"
Port = 5001
server.connect((IP_address, Port))
trama_up={}
id=input("ID for the new ONT or 'A' for autogenerate: ")
if id=='A':
    id=''.join([random.choice(string.ascii_letters + string.digits) for n in range(16)])
bandwith=input("BANDWITH for the new ONT: ")
priority=input("PRIORITY for the new ONT: ")
id_OLTStandard=priority+bandwith;
trama_up.update({id_OLTStandard : [id, bandwith, priority]})
os.system("clear")
print("Information: ID = "+id+" | Bandwith = "+bandwith+" | Priority = "+priority)
print("ENTER TO START THE SYSTEM.....")
while True:
    sockets_list = [sys.stdin, server]
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
    for socks in read_sockets:
        if socks == server:
            message = socks.recv(4096)
            print(message)
        else:
            server.send(pickle.dumps(trama_up))
server.close()
