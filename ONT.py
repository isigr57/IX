import socket
import pickle
import select
import sys
import os
import random
import string
import _thread


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = "localhost"
Port = 5001
server.connect((IP_address, Port))
trama_up={}
id=input("ID for the new ONT or leave blank for autogenerate: ") or ''.join([random.choice(string.ascii_letters + string.digits) for n in range(16)])
bandwith=input("BANDWITH in MB/s for the new ONT or blank for random [0-2480]: ") or str(random.randint(0,2480))
priority=input("PRIORITY for the new ONT or blank for randon [1-4]: ") or str(random.randint(1,4))
id_OLTStandard=priority+bandwith+id;
trama_up.update({id_OLTStandard : [id, bandwith, priority]})
os.system("clear")

def sendtramas():
    while True:
        sockets_list = [sys.stdin, server]
        read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
        for socks in read_sockets:
            if socks != server:
                server.send(pickle.dumps(trama_up))

print("Information: ID = "+id+" | Bandwith = "+bandwith+" | Priority = "+priority)
print("ENTER TO CONFIRM DATA.....")
_thread.start_new_thread(sendtramas,())

while True:
    sockets_list = [sys.stdin, server]
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
    for socks in read_sockets:
        if socks == server:
            message = socks.recv(1500)
            response=pickle.loads(message)
            if any(id in s for s in response):
                for item in response:
                    if item[0]==id:
                        os.system("clear")
                        print("\n\nInformation: ID = "+id+" | Bandwith = "+bandwith+" | Priority = "+priority)
                        print("-------------------------------------------------------------------------")
                        print("ONT is allocated on Alloc-ID: "+ str(item[3]))
                        print("Assigned Bandwith for the ONT : "+str(item[4])+" MB/s")
                        print("-------------------------------------------------------------------------\n\n")
            else:
                os.system("clear")
                print("\n\nInformation: ID = "+id+" | Bandwith = "+bandwith+" | Priority = "+priority)
                print("-------------------------------------------------------------------------")
                print("ONT is NOT allocated")
                print("-------------------------------------------------------------------------\n\n")
server.close()
