Compiling code
GET has four headers -If-Match, If-Modified-Since, If-Unmodified-Since, If-None-Match
Compiling code is
python3 webserver.py port-no // port no is some integer
Host and above headers has this format and spelling is any other like host, etc gives error
Error.log contains errors 4xx and 5xx entries
Access.log contains all 
ancan.conf has all document root

format of access.log(res 1xx. 2xx, 3xx): log Date, Device ip,Device mac,  Request name, response number, file name, last modified date
format of error.log(res 4xx, 5xx):log Date, Device ip,Device mac,  Request name, response number, file name, last modified date

SYNTAX :
server side: python3 webserver.py portno
client side: protocol name: ATWS
version:0.1
Host:  field not empty
Date format: Day, Date Month Year Time IST only this format
request: GET, PUT,POST, HEAD, DELETE

POST format:
POST /filename ATWS/0.1 // filename: please give path to a file only 
Host: 127.0.0.1
Content-Type: type //compulsory
Content-Length: some value >=  0 //temporary actually not needed for application/x-www.form-urlencoded type

type can be application/x-www-form-urlencoded, multipart/form-data;boundary=somevalue(ex:akl)(some value = anything example ram, shyam etc), text/plain
a space to be left compulsarily after above headers

format for application/x-www-form-urlencoded
field1=value1&field2=value2&....so on

format for text/plain type
simple line 

format for multipart/form-data
--akl
Content-Disposition: form-data;name=somevalue(enclosed in "")
Content-Type: text/plain /application-x-www-form-urlencoded
Content-Length: same as above 

as per from line no 30-34
--akl
same pattern

--akl-- //to end place --akl-- instead for --akl


PUT format:
PUT /filename ATWS/0.1
Host: 127.0.0.1
Content-Length: some value>=0
Content-Type: text/html

some html content

