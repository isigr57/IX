# IX GPON SIMULATOR.
import socket
import pickle
import _thread
from terminaltables import AsciiTable
import os
import time
import collections

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
IP_address = "localhost"
Port = 5001
server.bind((IP_address, Port))
server.listen(4096)
list_of_clients = []
table_ONTS_in={}
table_ONTS_error=[]

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
            print("\n\n----ALLOCATED TABLE----\n\n")
            print_table(DBA(table_ONTS_in))
            print("\n\n----ERROR TABLE----\n\n")
            print_table(table_ONTS_error)
            refresh=input("Enter 'R' for refreshing output: ")
            while refresh not in ('r','R'):
                refresh=input("Enter 'R' for refreshing output: ")
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
    pr=[0,0,0,0]
    bd=[0,0,0,0]
    allocid=1000
    global max_cap
    global table_ONTS_error
    table_ONTS_error=[['Id ONT','Bandwith in MB/s','Priority', 'Alloc-ID', 'Assigned Bandwith']]
    restant = max_cap
    table_out=[]
    table_in=collections.OrderedDict(sorted(table_in.items()))
    print(table_in)
    table_out.append(['Id ONT','Bandwith in MB/s','Priority', 'Alloc-ID', 'Assigned Bandwith'])
    for key in table_in.keys():
        pr[int(key[0])-1]=pr[int(key[0])-1]+1
        bd[int(key[0])-1]=bd[int(key[0])-1]+int(table_in[key][1])
    for i in range (0,4):
        iter=0
        #print("change" + str(i) +"bd: "+str(bd[i])+"  "+str(restant))
        selectedkeys=[]
        if restant==0:
            factor=-1
        elif bd[i]>restant:
            factor = restant/bd[i]
        else:
            factor=1
        for key in table_in.keys():
            if iter==pr[i]:
                #print("break in iter  "+str(iter))
                break
            if factor==-1:
                table_ONTS_error.append([table_in[key][0],table_in[key][1],table_in[key][2],"Not Allocated",0])
            else:
                table_out.append([table_in[key][0],table_in[key][1],table_in[key][2],allocid,"{:.2f}".format(int(table_in[key][1])*factor)])
                restant=restant-(int(table_in[key][1])*factor)
            selectedkeys.append(key)
            allocid=allocid+1
            if restant<0:
                restant=0
            iter=iter+1
        for key in selectedkeys:
            if key in table_in:
                del table_in[key]
    #print(pr)
    #print(bd)
    return table_out


max_cap = int(input("Enter Gran Map Size [0-2480] (MB/s) or leave blank for default 2480: ") or "2480")
_thread.start_new_thread(serverupdatetread,())
while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    _thread.start_new_thread(clientthread,(conn,addr))
conn.close()
server.close()
