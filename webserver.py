from socket import socket, AF_INET, SOCK_STREAM, gethostname, gethostbyname
import sys
import os
from os import path
import time
from datetime import datetime
import threading
import hashlib
from getmac import get_mac_address as gma
def syn(req):
    l = ['GET', 'PUT', 'POST', 'HEAD', 'DELETE','OPTIONS']
    x = req.split()
    if len(x) == 3 or len(x) == 2:
        if x[0] in l:
            return True
    return False
def csum(x):
    x = hashlib.md5(x.encode())
    x = '"'+str(x.hexdigest())+'"'
    return x
def creatdate(x, m):
    if ',' in x:
        p=x.split(',')[-1]
        p = p.split()
        date = int(p[0].strip())
        mon = int(m[p[1].strip()])
        year = int(p[2].strip())
        hr, min, sec = map(int, p[3].strip().split(':'))
        mt = datetime(year, mon, date)
        mt = mt.replace(hour = hr, minute = min, second = sec)
        return mt
    else:
        return datetime.strptime(x, "%a %b %d %H:%M:%S %Y")
        
        #return mt
def cookies(fil):
    f = open(fil, 'r')
    c = f.read()
    return csum(c)
class serthr(threading.Thread):
    def __init__(self, month, port, rootpath):
        threading.Thread.__init__(self)
        self.moved = dict()
        self.month = month
        self.port = port
        self.conn = conn
        self.rootpath = rootpath+'/'
        self.file = rootpath+'/'
        self.errorlog = self.file +'logs/error.log'
        self.alllog = self.file + 'logs/access.log'
        self.imp = [self.file+'index.html']
    def closeconn(self):
        self.conn.send(self.res(408,'').encode())
        global f
        f = 1
        self.conn.close()
    def res(self, resno,op):
        c =''
        if int(resno/100) == 4 or int(resno/100) == 5:
            lo = open(self.errorlog, 'a+')
        else:
            lo = open(self.alllog, 'a+')
        if resno == 400 :
            c += 'ATWS/0.1 400 Bad Request\n'
            x = datetime.now()
            c += 'Date:{},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S"))
            lo.write('Log Date and Time:{},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S")))
            c += "Server:AT's Server/0.0.1\n"
            x = open('html/400r.html', 'r')
            p = x.read().format(self.port)
            c += 'Content-Length:{}\n'.format(len(p))
            c += 'Connection-Type: Close\n'
            c += 'Content-Type:text/html; charset=iso-8859-1\n'
            c += '\n'
            c += p
        elif resno == 404:
            c += 'ATWS/0.1 404 Not Found\n'
            x = datetime.now()
            c += '{},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S"))
            lo.write('Log Date and Time:{},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S")))
            c += "Server:AT's Server/0.0.1\n"
            x = open('html/404r.html', 'r')
            p = x.read().format(self.port)
            c += 'Content-Length:{}\n'.format(len(p))
            c += 'Connection-Type: Close\n'
            c += 'Content-Type:text/html; charset=iso-8859-1\n'
            c += '\n'
            c += p
        elif resno == 408:
            c += 'ATWS/0.1 408 Request Timeout\n'
            x = datetime.now()
            c += '{},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S"))
            lo.write('Log Date and Time:{},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S")))
            c += "Server:AT's Server/0.0.1\n"
            x = open('html/408r.html', 'r')
            p = x.read().format(self.port)
            c += 'Content-Length:{}\n'.format(len(p))
            c += 'Connection-Type: Close\n'
            c += 'Content-Type:text/html; charset=iso-8859-1\n'
            c += '\n'
            c += p
        elif resno == 405:
            c += 'ATWS/0.1 405 Method Not Allowed\n'
            x = datetime.now()
            c += 'Date: {},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S"))
            lo.write('Log Date and Time:{},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S")))
            c += "Server:AT's Server/0.0.1\n"
            c += "Allow: GET,PUSH,PUT,HEAD,DELETE\n"
            x = open('html/405r.html', 'r')
            p = x.read().format(op, self.port)
            c += 'Content-Length:{}\n'.format(len(p))
            c += 'Content-Type:text/html; charset=iso-8859-1\n'
            c += '\n'
            c += p
        elif resno == 501:
            c += 'ATWS/0.1 501 Not Implemented\n'
            x = datetime.now()
            c += 'Date: {},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S"))
            lo.write('Log Date and Time:{},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S")))
            c += "Server:AT's Server/0.0.1\n"
            c += "Allow: GET,PUSH,PUT,HEAD,DELETE\n"
            x = open('html/501r.html', 'r')
            p = x.read().format(self.port)
            c += 'Content-Length:{}\n'.format(len(p))
            c += 'Content-Type:text/html; charset=iso-8859-1\n'
            c += '\n'
            c += p
        elif resno == 200:
            if op == 'GET' or op == 'HEAD':
                c += 'ATWS/0.1 200 OK\n'
                x = datetime.now()
                c += 'Date: {},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S"))
                lo.write('Log Date and Time:{},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S")))
                c += "Server:AT's Server/0.0.1\n"
                x= creatdate(time.ctime(path.getmtime(self.file)), self.month)
                c += 'Last-Modified:{},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S"))
                
                if op == 'GET':
                    f = open(self.file, 'r')
                    k = f.read()
                    f.close()
                    f = open(self.file, 'w')
                    f.write(k)
                    f.close()
                else:
                    k = ''
                c += 'ETag: {}\n'.format(csum(self.file))
                c += 'Accept-Ranges: bytes\n'
                c += 'Content-Length: {}\n'.format(len(k))
                c += 'Vary: Accept-Encoding\n'
                c += 'Content-Type: text/html\n'
                c += '\n'
                c += k
            elif op == 'POST' or op == 'PUT':
                x = datetime.now()
                lo.write('Log Date and Time:{},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S")))
                c += 'ATWS/0.1 200 OK\n'
                c += 'Location:{}\n'.format(self.file)
            else:
                c += 'ATWS/0.1 200 OK\n'
                x = datetime.now()
                c += 'Date: {},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S"))
                lo.write('Log Date and Time:{},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S")))
                c += '\n'
                f = open('html/del.html', 'r')
                c += f.read()
                f.close()
        elif resno == 301:
            c += 'ATWS/0.1 301 Moved Permanently\n'
            c += 'Location: {}\n'.format(self.moved[self.file])
            c += 'Content-Type: text/html; charset = iso-8859-1\n'
            x = datetime.now()
            lo.write('Log Date and Time:{},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S")))
            c += 'Date: {},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S"))
        elif resno == 412:
            c += 'ATWS/0.1 412 Precondition Failed\n'
            x = datetime.now()
            c += 'Date: {},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S"))
            lo.write('Log Date and Time:{},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S")))
            c += "Server:AT's Server/0.0.1\n"
            x= creatdate(time.ctime(path.getmtime(self.file)), self.month)
            c += 'Last-Modified:{},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S"))
                    
        elif resno == 403:
            c += 'ATWS/0.1 403 Forbidden\n'
            x = datetime.now()
            c += 'Date: {},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S"))
            lo.write('Log Date and Time:{},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S")))
            c += "Server:AT's Server/0.0.1\n"
            c += 'Content-Length: 0\n'
            c += 'Content-Type: text/html\n'
            f = open('html/403r.html', 'r')
            k = f.read()
            c += k
            f.close()

        elif resno == 304:
            c += 'ATWS/0.1 304 Not Modified\n'
            x = datetime.now()
            c += 'Date: {},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S"))
            lo.write('Log Date and Time:{},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S")))
            c += "Server:AT's Server/0.0.1\n"
            c += 'ETag:{}\n'.format(csum(self.file))
            c +='Accept-Range: bytes\n'
            c += 'Content-Length: 0\n'
            c += 'Content-Type: text/html\n'
        elif resno == 500:
            c += 'ATWS/0.1 500 Internal Server Error\n'
            x = datetime.now()
            c += 'Date: {},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S"))
            lo.write('Log Date and Time:{},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S")))
            c += "Server:AT's Server/0.0.1\n"
            c += 'Etag: {}\n'.format(csum(self.file))

        elif resno == 201:
            x = datetime.now()
            lo.write('Log Date and Time:{},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S")))
            c += 'ATWS/0.1 201 Created\n'
            c += 'Location: {}\n'.format(self.file)
        
        ip = gethostbyname(gethostname())
        mac = gma()
        lo.write('IP address:{}\n'.format(ip))
        lo.write('MAC address:{}\n'.format(mac))
        lo.write('Request Name:{}\n'.format(op))
        lo.write('Response Number: {}\n'.format(resno))
        if path.exists(self.file):
            lo.write('Filename:{}\n'.format(self.file.replace(self.rootpath, '')))
            x= creatdate(time.ctime(path.getmtime(self.file)), self.month)
            lo.write('LastModifiedDate:{},{} {} {} {}:{}:{} IST\n'.format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"),x.strftime("%Y"), x.strftime("%H"),x.strftime("%M"),x.strftime("%S")))
        else:
            lo.write('Status:File does not exist or File path is wrong or file is moved to some other location\n')    
        lo.write('\n')
        lo.close()
        return c
    def run(self):
        while True:
            req1 = self.conn.recv(1024).decode()
            r = req1.split()
            fil = r[1].strip()
            if syn(req1):
                if len(r) == 2:
                    if 'GET' in r[0]:
                        if fil == '/':
                            self.file += 'index.html'
                        elif fil[0] == '/':
                            self.file += fil[1:]
                        if path.exists(self.file):
                            f = open(self.file, 'r')
                            c = f.read()
                            self.conn.send(c.encode())
                            self.conn.close()
                            break
                        else:
                            f = open('html/404r.html', 'r')
                            c = f.read().format(self.port)
                            self.conn.send(c.encode())
                            self.conn.close()
                            break
                    else:
                        f = open('html/400r.html', 'r')
                        c = f.read().format(self.port)
                        self.conn.send(c.encode())
                        self.conn.close()
                        break
                else:#len = 3
                    protver = r[2].split('/')
                    if protver[0] == 'ATWS' and protver[1] == '0.1':
                        msg = []
                        f = 0
                        while f == 0:
                            t =threading.Timer(20,self.closeconn)
                            t.start()
                            msg.append(self.conn.recv(1024).decode())
                            t.cancel()
                            if not(msg[-1].strip()):
                                break
                        if f==1:
                            try :
                                self.conn.close()
                            except:
                                pass
                            break

                        if fil =='/':
                            self.file += 'index.html'
                        elif fil[0] == '/':
                            self.file += fil[1:]
                        else:
                            self.conn.send(self.res(400, r[0].strip()).encode())
                            self.conn.close()
                            break

                        if 'PUT' in  r[0] or 'POST' in r[0]:
                            if 'PUT' in r[0]:#handling two headers content type and length Host is imp
                                f = 0
                                htm = []
                                while f == 0:
                                    t = threading.Timer(150, self.closeconn)
                                    t.start()
                                    try:
                                        htm.append(self.conn.recv(1024).decode())
                                    except:
                                        break
                                    t.cancel()
                                    if not(htm[-1].strip()):
                                        break
                                if f == 1:
                                    try:
                                        self.conn.close()
                                    except:
                                        pass
                                    break
                                unap = 0
                                c = 0
                                for i in msg:
                                    if not(i.strip()):
                                        break
                                    try:
                                        x = i.split(':')
                                    except:
                                        self.conn.send(self.res(400, r[0].strip()).encode())
                                        self.conn.close()
                                        unap = 1
                                        break
                                    if 'Host' in x[0]:
                                        if not(x[1].strip()):
                                            self.conn.send(self.res(400, r[0].strip()).encode())
                                            self.conn.close()
                                            unap = 1
                                            break
                                        c = 1
                                    elif 'Content-Length' in x[0]:
                                        if x[1].strip().isdigit():
                                            size = int(x[1]) 
                                            if size <0:
                                                self.conn.send(self.res(501, r[0].strip()).encode())
                                                self.conn.close()
                                                unap = 1
                                                break
                                        else:
                                            self.conn.send(self.res(501, r[0].strip()).encode())
                                            self.conn.close()
                                            unap = 1
                                            break
                                    elif 'Content-type' in x[0]:
                                        if x[1].strip().split('/')[-1] != self.file.strip().split('.')[-1]:
                                            self.conn.send(self.res(501, r[0].strip()).encode())
                                            self.conn.close()
                                            unap  =1
                                            break
                                if unap == 1:
                                    break
                                if path.exists(self.file):
                                    f = open(self.file, 'w')
                                    ex = 1
                                else:
                                    f = open(self.file, 'w+')
                                    ex = 0
                                for i in htm:
                                    if size < len(i):
                                        f.write(i[:size])
                                        size = 0
                                                                        
                                    else:
                                        f.write(i)
                                        size -= len(i)
                                if ex == 1:
                                    self.conn.send(self.res(200, r[0].strip()).encode())
                                    self.conn.close()
                                    break
                                else:
                                    self.conn.send(self.res(201, r[0].strip()).encode())
                                    self.conn.close()
                                    break
                            else:#POST
                                unap = 0
                                c = 0
                                a = 0
                                t = 0
                                size = -1
                                vars =dict()
                                boundary = None
                                for i in msg:
                                    try:
                                        x = i.split(':')
                                    except:
                                        self.conn.send(self.res(400, r[0].strip().encode()))
                                        self.conn.close()
                                        unap = 1
                                        break
                                    if 'Host' in x[0]:
                                        if not(x[1].strip()):
                                            self.conn.send(self.res(400, r[0].strip()).encode())
                                            self.conn.close()
                                            unap = 1
                                            break
                                        c = 1
                                    elif 'Content-Type' in x[0]:
                                        if 'multipart/form-data' in x[1]:
                                            if 'boundary=' in x[1]:
                                                boundary = x[1].split('=')[-1]
                                            else:
                                                self.conn.send(self.res(400, r[0].strip()).encode())
                                                self.conn.close()
                                                unap =1
                                                break
                                        else:
                                            if 'application/x-www-form-urlencoded' in x[1]:
                                            	a = 1
                                            elif 'text/plain' in x[1]:
                                                t = 1
                                    elif 'Content-Length' in x[0]:
                                        try:
                                            size = int(x[1])
                                        except:
                                            self.conn.send(self.res(400, r[0].strip()).encode())
                                            self.conn.close()
                                            unap = 1
                                            break
                                        if size < 0:
                                            self.conn.send(self.res(400, r[0].strip()).encode())
                                            self.conn.close()
                                            unap = 1
                                            break
                                    elif 'Content-Disposition' in x[0]:
                                        if 'form-data' in x[1]:
                                            try:
                                                varname = x[1].split('=')[-1]
                                            except:
                                                self.conn.send(self.res(400, r[0].strip()))
                                                self.conn.close()
                                                unap = 1
                                                break
                                            while '"' in varname:
                                                varname = varname.replace('"', '')
                                        else:
                                            self.conn.send(self.res(400, r[0].strip()).encode())
                                            self.conn.close()
                                            unap = 1
                                            break
                                if unap == 1:
                                    break
                                if (a == 1 or t == 1) and boundary == None :
                                    t = threading.Timer(150, self.closeconn)
                                    t.start()
                                    try:
                                        x = self.conn.recv(1024).decode()
                                    except:
                                        break
                                    t.cancel()
                                    if a == 1 and t == 1:
                                        self.conn.send(self.res(400, r[0].strip()).encode())
                                        self.conn.close()
                                        break
                                    if a == 1:
                                        try:
                                            m = x.split('&')
                                        except:
                                            m = [x]
                                        for i in m:
                                            p = i.strip().split('=')
                                            vars[p[0]]  = p[1]
                                    else:
                                        if varname == None:
                                            self.conn.send(self.res(400, r[0].strip()).encode())
                                            self.conn.close()
                                            unap = 1
                                            break
                                        while '"' in varname:
                                            varname = varname.replace('"', '')
                                        if size == -1:
                                            vars[varname] = x
                                        else:
                                            if len(x) <= size:
                                                vars[varname] = x
                                            else:
                                                vars[varname] = x[:size]
                                elif boundary:
                                    boundary = boundary.strip()
                                    data = []
                                    n = 0
                                    f = 0
                                    while f == 0:
                                        t = threading.Timer(150, self.closeconn)
                                        t.start()
                                        try:
                                            data.append(self.conn.recv(1024).decode())
                                        except:
                                            break
                                        t.cancel()
                                        if '--'+boundary+'--' in data[-1]:
                                            break
                                        if not(data[-1].strip()):
                                            n += 1
                                    if f== 1:
                                        break
                                    pos = 0
                                    for i in range(n):
                                        k = data[pos]
                                        a = 0
                                        t = 0
                                        if '--'+boundary in k:
                                            pos += 1
                                            k = data[pos]
                                        elif '--'+boundary+'--' in k:
                                            break
                                        while k.strip():
                                            if 'Content-Disposition:' in k:
                                                try:
                                                    m = k.split(':')
                                                except:
                                                    unap = 1
                                                    self.conn.send(self.res(400, r[0].strip()).encode())
                                                    self.conn.close()
                                                    break
                                                if 'form-data' in m[1] and 'name=' in m[1]:
                                                    try:
                                                        la = m[1].strip('=')[-1]
                                                        while '"' in la:
                                                            la = la.replace('"', '')
                                                    except:
                                                        unap = 1
                                                        self.conn.send(self.res(400, r[0].strip()).encode())
                                                        self.conn.close()
                                                        break
                                                else:
                                                    self.conn.send(self.res(400, r[0].strip()).encode())
                                                    self.conn.close()
                                                    unap = 1
                                                    break
                                            elif 'Content-Type:' in k:
                                                try:
                                                    ty = k.split(':')[-1]
                                                except:
                                                    self.conn.send(self.res(400, r[0].strip()).encode())
                                                    self.conn.close()
                                                    unap = 1
                                                    break
                                                if 'application/x-www-form-urlencoded' in ty:
                                                    a= 1
                                                elif 'text/plain' in ty:
                                                    t = 1
                                                else:
                                                    self.conn.send(self.res(400, r[0].strip()).encode())
                                                    self.conn.close()
                                                    unap = 1
                                                    break
                                            elif 'Content-Length' in k:
                                                try:
                                                    size = int(k.strip().split(':')[-1])
                                                except:
                                                    unap = 1
                                                    self.conn.send(self.res(400, r[0].strip()).encode())
                                                    self.conn.close()
                                                    break
                                                if size < 0:
                                                    self.conn.send(self.res(400, r[0].strip()).encode())
                                                    self.conn.close()
                                                    unap = 1
                                                    break
                                            else:
                                                self.conn.send(self.res(400, r[0].strip()).encode())
                                                self.conn.close()
                                                unap = 1
                                                break
                                            pos += 1
                                            k = data[pos]
                                        if unap == 1:
                                            break
                                        pos += 1
                                        k = data[pos]
                                        if a == 1:
                                            try:
                                                val = k.split('&')
                                            except:
                                                val = [k]
                                            for i in val:
                                                eq = i.split('=')
                                                vars[eq[0]] = eq[1]
                                        else:
                                            if size == -1:
                                                vars[la] = k
                                            elif len(k) > size:
                                                vars[la]= k[:size]
                                            else:
                                                vars[la] = k
                                        pos += 1
                                    if unap == 1:
                                        break
                                else:
                                    self.conn.send(self.res(400, r[0].strip()).encode())
                                    self.conn.close()
                                    unap = 1
                                    break
                                post = '{\n'
                                for i in vars:
                                    post += '{}:{}'.format(i, vars[i])
                                post += '}\n'
                                if path.exists(self.file):
                                    f = open(self.file, 'a')
                                    f.write(post)
                                    f.close()
                                    self.conn.send(self.res(200, r[0].strip()).encode())
                                else:
                                    f = open(self.file, 'a+')
                                    f.write(post)
                                    f.close()
                                    self.conn.send(self.res(201, r[0].strip()).encode())
                                self.conn.close()
                                break
                        elif self.moved.get(self.file):
                            self.conn.send(self.res(301, r[0].strip()))
                            self.conn.close()
                            break
                        else:
                            if path.exists(self.file):
                                del msg[-1]
                                if os.access(self.file, os.R_OK) and os.access(self.file, os.W_OK):
                                    headers = dict()
                                    headers['Host'] = 0
                                    headers['If-Match'] =0
                                    headers['If-Modified-Since'] = 0
                                    headers['If-Unmodified-Since'] = 0
                                    headers['If-None-Match'] = 0
                                    unap = 0
                                    for i in msg:
                                        if not(msg[msg.index(i)].strip()):
                                            break
                                        else:
                                            try:
                                                x = i.split(':')
                                            except:
                                                self.conn.send(self.res(400, r[0].strip()).encode())
                                                self.conn.close()
                                                unap = 1
                                                break
                                            if 'Host' in x[0].strip():
                                                if not(x[1].strip()):
                                                    self.conn.send(self.res(400, r[0].strip()).encode())
                                                    self.conn.close()
                                                    break
                                                headers['Host'] = 1
                                            elif 'If-Match' in x[0].strip():
                                                try:
                                                    Et = x[1].strip().split(',')
                                                    for i in range(len(Et)):
                                                        Et[i] = Et[i].strip()
                                                except:
                                                    Et = x[1].strip()
                                                if '*' in Et:
                                                    headers['If-Match'] = 1
                                                elif csum(self.file) in Et:
                                                    headers['If-Match'] = 1
                                                else:
                                                    headers['If-Match'] = -1
                                            elif 'If-None-Match' in x[0].strip():
                                                try:
                                                    Et = x[1].strip().split(',')
                                                    for i in range(len(Et)):
                                                        Et[i] = Et[i].strip()
                                                except:
                                                    Et = x[1].strip()
                                                if '*' in Et:
                                                    headers['If-None-Match'] = -1
                                                elif csum(self.file) in Et:
                                                    headers['If-None-Match'] = -1
                                                else:
                                                    headers['If-None-Match'] = 1
                                            elif 'If-Modified-Since' in x[0].strip():
                                                x[1] += ':'+x[2]+':'+x[3]
                                                if creatdate(x[1].strip(), self.month) >= datetime.now():
                                                    headers['If-Modified-Since'] = -2
                                                elif creatdate(x[1].strip(), self.month) >= creatdate(time.ctime(path.getmtime(self.file)), self.month):
                                                    headers['If-Modified-Since'] = -1
                                                elif creatdate(x[1].strip(), self.month) < creatdate(time.ctime(path.getmtime(self.file)), self.month):
                                                    headers['If-Modified-Since'] = 1
                                            elif 'If-Unmodified-Since' in x[0].strip():
                                                x[1] += ':'+x[2]+':'+x[3]
                                                if creatdate(x[1].strip(), self.month) >= datetime.now():
                                                    headers['If-Unodified-Since'] = -2
                                                elif creatdate(x[1].strip(), self.month) >= creatdate(time.ctime(path.getmtime(self.file)), self.month):
                                                    headers['If-Unodified-Since'] = 1
                                                elif creatdate(x[1].strip(), self.month) < creatdate(time.ctime(path.getmtime(self.file)), self.month):
                                                    headers['If-Unodified-Since'] = -1
                                            else:
                                                self.conn.send(self.res(400, r[0].strip()).encode())
                                                self.conn.close()
                                                unap = 1
                                                break
                                    if unap == 1:
                                        break
                                    if headers['Host'] == 1:
                                        if r[0] == 'DELETE':
                                            if self.file in self.imp:
                                                self.conn.send(self.res(403, r[0].strip()).encode())
                                                self.conn.close()
                                                break
                                            else:
                                                self.conn.send(self.res(200, r[0].strip()).encode())
                                                if path.isdir(self.file):
                                                    os.rmdir(self.file)
                                                else:
                                                    os.remove(self.file)
                                                self.conn.close()
                                                break
                                        else:
                                            if len(msg) == 1:
                                                self.conn.send(self.res(200, r[0].strip()).encode())
                                                self.conn.close()
                                                break
                                            elif len(msg) == 2:
                                                if headers['If-Modified-Since'] == -1 or headers['If-Unmodified-Since'] == -1:
                                                    self.conn.send(self.res(304, r[0].strip()).encode())
                                                    self.conn.close()
                                                    break
                                                elif headers['If-Modified-Since'] == -2 or headers['If-Unmodified-Since'] == -2:
                                                    self.conn.send(self.res(400, r[0].strip()).encode())
                                                    self.conn.close()
                                                    break
                                                elif headers['If-Match'] == -1:
                                                    self.conn.send(self.res(412, r[0].strip()).encode())
                                                    self.conn.close()
                                                    break
                                                elif headers['If-None-Match'] == -1:
                                                    self.conn.send(self.res(304, r[0].strip()).encode())
                                                    self.conn.close()
                                                    break
                                                else:
                                                    self.conn.send(self.res(200, r[0].strip()).encode())
                                                    self.conn.close()
                                                    break
                                            elif len(msg) == 3:
                                                #applying combinations
                                                if (headers['If-Modified-Since'] != 0 and headers['If-Match'] != 0) or  (headers['If-Modified-Since'] != 0 and headers['If-Unmodified-Since'] != 0) or(headers['If-Match'] != 0 and headers['If-None-Match'] != 0) or(headers['If-None-Match'] != 0 and headers['If-Unmodified-Since'] != 0):
                                                    self.conn.send(self.res(200, r[0].strip()).encode())
                                                    self.conn.close()
                                                    break
                                                elif headers['If-Modified-Since'] == 1:
                                                    if headers['If-None-Match'] == -1 or headers['If-None-Match'] == 0:
                                                        self.conn.send(self.res(304, r[0].strip()).encode())
                                                        self.conn.close()
                                                        break
                                                    else:
                                                        self.conn.send(self.res(200, r[0].strip()).encode())
                                                        self.conn.close()
                                                        break
                                                elif headers['If-Modified-Since'] == -1:
                                                    self.conn.send(self.res(304, r[0].strip()).encode())
                                                    self.conn.close()
                                                    break
                                                elif headers['If-Modified-Since'] == -2:
                                                    if headers['If-None-Match'] == -1:
                                                        self.conn.send(self.res(304, r[0].strip()).encode())
                                                        self.conn.close()
                                                        break
                                                    else:
                                                        self.conn.send(self.res(200, r[0].strip()).encode())
                                                        self.conn.close()
                                                        break
                                                elif headers['If-Match'] == 1:
                                                    if headers['If-Unmodified-Since'] == 1 or headers['If-Unmodified-Since'] == -2:
                                                        self.conn.send(self.res(200, r[0].strip()).encode())
                                                        self.conn.close()
                                                        break
                                                    else:
                                                        self.conn.send(self.res(412, r[0].strip()).encode())
                                                        self.conn.close()
                                                        break
                                                elif headers['If-Match'] == -1:
                                                    self.conn.send(self.res(412, r[0].strip()).encode())
                                                    self.conn.close()
                                                    break
                                            elif len(msg) == 4:
                                                if (headers['If-Modified-Since'] != 0 and headers['If-Match'] != 0):
                                                    if headers['If-Unmodified-Since'] == 1 or headers['If-Unmodified-Since'] == -2 or headers['If-None-Match'] == 1:
                                                        self.conn.send(self.res(200, r[0].strip()).encode())
                                                        self.conn.close()
                                                        break
                                                    else:
                                                        self.conn.send(self.res(412, r[0].strip()).encode())
                                                        self.conn.close()
                                                        break
                                                    
                                                elif (headers['If-Modified-Since'] != 0 and headers['If-Unmodified-Since'] != 0):
                                                    if headers['If-Match'] == 1 or headers['If-None-Match'] == 1:
                                                        self.conn.send(self.res(200, r[0].strip()).encode())
                                                        self.conn.close()
                                                        break
                                                    elif headers['If-Match'] == -1:
                                                        self.conn.send(self.res(412, r[0].strip()).encode())
                                                        self.conn.close()
                                                        break
                                                    else:
                                                        self.conn.send(self.res(304, r[0].strip()).encode())
                                                        self.conn.close()
                                                        break
                                                elif (headers['If-Match'] != 0 and headers['If-None-Match'] != 0):
                                                    if headers['If-Modified-Since'] == -1:
                                                        self.conn.send(self.res(304, r[0].strip()).encode())
                                                        self.conn.close()
                                                        break
                                                    elif headers['If-Unmodified-Since'] == -1:
                                                        self.conn.send(self.res(412, r[0].strip()).encode())
                                                        self.conn.close()
                                                        break
                                                    else:
                                                        self.conn.send(self.res(200, r[0].strip()).encode())
                                                        self.conn.close()
                                                        break
                                                elif (headers['If-None-Match'] != 0 and headers['If-Unmodified-Since'] != 0):
                                                    if headers['If-Match'] == -1:
                                                        self.conn.send(self.res(412, r[0].strip()).encode())
                                                        self.conn.close()
                                                        break
                                                    elif headers['If-Modified-Since'] == -1:
                                                        self.conn.send(self.res(304, r[0].strip()).encode())
                                                        self.conn.close()
                                                        break
                                                    else:
                                                        self.conn.send(self.res(200, r[0].strip()).encode())
                                                        self.conn.close()
                                                        break
                                            elif len(msg) == 5:
                                                self.conn.send(self.res(200, r[0].strip()).encode())
                                                self.conn.close()
                                                break
                                            else:
                                                self.conn.send(self.res(400, r[0].strip()).encode())
                                    else:#Host
                                        self.conn.send(self.res(400, r[0].strip()).encode())
                                        self.conn.close()
                                        break
                                else:#file permission
                                    self.conn.send(self.res(500, r[0].strip()).encode())
                                    self.conn.close()
                                    break

                            else:#file exists
                                self.conn.send(self.res(400, r[0].strip()).encode())
                                self.conn.close()
                                break
                    else:#proto
                        self.conn.send(self.res(400, r[0].strip()).encode())
                        self.conn.close()
                        break
            else: #syn
                self.conn.send(self.res(400, r[0].strip()).encode())
                self.conn.close()
                break                
#path determination
f = open('ancan.conf', 'r')
c = f.readline()
while c:
    if 'DocumentRoot' in c:
        rootfile = c.split('DocumentRoot')[-1].strip()
    elif 'ErrorLog' in c:
        errorfile = c.split('/')[-1].strip()
    elif 'CustomLog' in c:
        accessfile = c.split('/')[-1].strip()
        accessfile = accessfile.split(' ')[0]
    c= f.readline()

month = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6,'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11,
'Dec':12}

server = socket(AF_INET, SOCK_STREAM)
try:
    port=int(sys.argv[1])
except:
    print('Enter proper port number')
    sys.exit()
sthr = []
server.bind(('', port))
server.listen(100)
while True:
    conn, addr = server.accept()
    th = serthr( month, port, rootfile)
    sthr.append(th)
    th.start()
    
