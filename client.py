import sys
import socket
import random
import struct

host = sys.argv[1] 
port = int(sys.argv[2])
function = str(sys.argv[3])
try:
    color = str(sys.argv[4])
    question = function + "," + color
except:
    question = function
returncode = 0
answer = 0
messagetype = 1

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
messageid = random.randint(1,100) #generating random number

#formating
question = question.encode()
formate = '!hhihh' + str(len(question)) + 's'
csstrict = struct.Struct(formate)
request = csstrict.pack(messagetype, returncode, messageid, len(question), answer, question)

#sending request
clientsocket.sendto(request,(host, port))
print("Sending Request to " + str(host) + ", " + str(port))
clientsocket.settimeout(1)


for x in range(3):
    try:
        response, address = clientsocket.recvfrom(1024)
        break
    
    except: 
        if x == 2:
            sys.exit("Timeout and exiting the program")
        print("Time out, trying again")
        print("Sending Request to " + str(host) + ", " + str(port))
        continue
    
#responce form the server
length = len(response)
megsiz = length - struct.calcsize('!hhihh')
formate2 = '!hhihh' + str(megsiz) + 's'
secondstruct = struct.Struct(formate2)
answer = secondstruct.unpack(response)[5].decode()

print("Received Response form " + str(host) + ", " + str(port))

if secondstruct.unpack(response)[1] == 1:
    print("Error: Function not supported.")
else:
    print("Answer: " + str(answer))

clientsocket.close()











