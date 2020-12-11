from socket import socket, gethostbyname, gethostname, AF_INET, SOCK_STREAM
import threading
from datetime import datetime
from getmac import get_mac_address as gma
import sys

client  = socket(AF_INET, SOCK_STREAM)
try:
    port = int(sys.argv[1])
except:
    print('Enter a integer port no')
    sys.exit()
input = ['GET / ATWS/0.1', 'Host: 127.0.0.1', '']
client.connect(('127.0.0.1', port))
for i in input:
    print(i)
    client.send(i.encode())
x = datetime.now()
op = client.recv(1024).decode()
x = datetime.now()
c = 'Date: {},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S"))
print(op)
print(c)            