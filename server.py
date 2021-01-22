import sys
import socket
import struct

serverIP = sys.argv[1]
serverPort = int(sys.argv[2])
colors = ("red", "orange", "white", "blue", "yellow")
stat = "off"
qlen = 0

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))
print("The server is ready to receive on port:  " + str(serverPort) + "\n")

while True:
    #request from client
    question, address = serverSocket.recvfrom(1024)

    length = len(question)
    megsiz = length - struct.calcsize('hhihh')
    formate = '!hhihh' + str(megsiz) + 's'
    firststruct = struct.Struct(formate)

    s = (firststruct.unpack(question)[5]).decode()
    retcode = (firststruct.unpack(question)[1])
    mestype = (firststruct.unpack(question)[0])
    messageid = (firststruct.unpack(question)[2])

    if ',' in s:
        s = s.split(",")
        function = s[0].lower()
        color = s[1].lower()
    else:
        function = s.lower()

    if function == "status":
        mestype = 1
        formate2 = '!hhihh' + str(len(stat)) + 's'
        secondstruct = struct.Struct(formate2)
        sendback = secondstruct.pack(mestype, retcode, messageid, qlen, len(stat), stat.encode())
        serverSocket.sendto(sendback, address)

    elif function == "set":
        if color == "on":
            stat = "Light bulb is on."
            formate2 = '!hhihh' + str(len(stat)) + 's'
            secondstruct = struct.Struct(formate2)
            sendback = secondstruct.pack(mestype, retcode, messageid, qlen, len(stat), stat.encode())
            serverSocket.sendto(sendback, address)
            
        elif color == "off":
            stat = "Light bulb is off."
            formate2 = '!hhihh' + str(len(stat)) + 's'
            secondstruct = struct.Struct(formate2)
            sendback = secondstruct.pack(mestype, retcode, messageid, qlen, len(stat), stat.encode())
            serverSocket.sendto(sendback, address)
            
        elif color not in colors:
            answer = "Color not supported"
            formate2 = '!hhihh' + str(len(answer)) + 's'
            secondstruct = struct.Struct(formate2)
            sendback = secondstruct.pack(mestype, retcode, messageid, qlen, len(answer), answer.encode())
            serverSocket.sendto(sendback, address)
        else:
            stat = "Light bulb is on. Color " + color + "."
            formate2 = '!hhihh' + str(len(stat)) + 's'
            secondstruct = struct.Struct(formate2)
            sendback = secondstruct.pack(mestype, retcode, messageid, qlen, len(stat), stat.encode())
            serverSocket.sendto(sendback, address)

    else:
        err = "Function not supported"
        formate2 = '!hhihh' + str(len(err)) + 's'
        secondstruct = struct.Struct(formate2)
        sendback = secondstruct.pack(mestype, retcode, messageid, qlen, len(err), err.encode())
        serverSocket.sendto(sendback, address)
