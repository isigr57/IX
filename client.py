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
id=input("ID for the new ONT or leave blank for autogenerate: ") or ''.join([random.choice(string.ascii_letters + string.digits) for n in range(16)])
bandwith=input("BANDWITH in MB/s for the new ONT or blank for random [0-2480]: ") or str(random.randint(0,2480))
priority=input("PRIORITY for the new ONT or blank for randon [0-4]: ") or str(random.randint(1,4))
id_OLTStandard=priority+bandwith+id;
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
