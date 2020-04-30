# IX GPON SIMULATOR.
import socket
import pickle
import _thread
from terminaltables import AsciiTable
import os
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
IP_address = "localhost"
Port = 5001
server.bind((IP_address, Port))
server.listen(4096)
list_of_clients = []
table_ONTS_in={}
table_ONTS_out=[]
max_cap = 2480

def print_table(table):
    out=AsciiTable(table)
    print(out.table)

def clientthread(conn, addr):
    while True:
            try:
                message = conn.recv(4096)
                if message:
                    ONT = pickle.loads(message);
                    table_ONTS_in.update(ONT)
                else:
                    remove(conn)
            except:
                continue

def serverupdatetread():
    refresh = '0'
    global table_ONTS_in
    while True:
        if bool(table_ONTS_in):
            os.system("clear")
            print_table(DBA(table_ONTS_in))
            refresh=input("Enter 'R' for refreshing: ")
            while refresh not in ('r','R'):
                refresh=input("Enter 'R' for refreshing: ")
            table_ONTS_in.clear()
        else:
            os.system("clear")
            print("SEARCHING FOR ONTS....REFRESHIG")
            time.sleep(1)




def broadcast(message, connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


def DBA(table_in):
    priority_con=[0,0,0,0]
    acumband=[0,0,0,0]
    allocid=1000
    global max_cap
    table_out=[]
    table_in={k: v for k, v in sorted(table_in.items(), key=lambda item: item[1])}
    table_out.append(['Id ONT','Bandwith in MB/s','Priority', 'Alloc-ID', 'Assigned Bandwith'])
    for key in table_in.keys():
        priority_con[int(key[0])-1]=priority_con[int(key[0])-1]+1
        priority_con[int(key[0])-1]=priority_con[int(key[0])-1]+int(key.value[1])
    return table_out



max_cap = input("Enter Gran Map Size [0-2480] (MB/s) or leave blank for default 2480: ")
_thread.start_new_thread(serverupdatetread,())
while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    _thread.start_new_thread(clientthread,(conn,addr))

conn.close()
server.close()
