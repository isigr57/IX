# Python program to implement server side of chat room.
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
pre_table_ONTS={}
table_ONTS_out=[]

def print_table(table):
    out=AsciiTable(table)
    print(out.table)

def clientthread(conn, addr):
    #conn.send("Welcome to ONT service")
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
    while True:
        os.system("clear")
        time.sleep(0.000125)
        if bool(table_ONTS_in):
            print_table(DBA(table_ONTS_in))

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
    pre_table_ONTS=table_in
    table_out=[]
    for key in table_in.keys():
        temp = [key,table_in[key][0],table_in[key][1]]
        #print(temp)
        table_out.append(temp)
    return table_out




_thread.start_new_thread(serverupdatetread,())
while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(addr[0] + " connected")
    _thread.start_new_thread(clientthread,(conn,addr))

conn.close()
server.close()
