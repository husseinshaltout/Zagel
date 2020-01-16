import socket
import sys
import time
from threading import *



def liveconnection (conn,addr,username):
    #Sending welcome message to connected client
    global usersonline
    targetusersocket=None
    dataafterdecode = None
    try:
        conn.send('Welcome to the server. Type something and hit enter') 
        time.sleep(0.1)
    except:
        pass
    
    while 1:
    #Receiving from client
        List=usersonline.keys()
        x='recieve'.encode('hex')
        conn.send(x)
        time.sleep(0.01)
        conn.send(':'.join(List))
        try:
            data = conn.recv(1024)
        except:
            #when client is disconnected,go out of the function 
            break
        
        try:
            dataafterdecode=data.decode("hex")
        except:
            pass
                
        #client want to connect to a user        
        if dataafterdecode=="connect to a user:":
            #check if the target user really exists
            targetusername = conn.recv(1024)
            fin = open('user.txt','r')
            checkusername = False
            usrlist = fin.readlines()
            for usr in usrlist:
                usr=usr.strip()
                x = usr.split(':')
                if x[0] == targetusername:
                    checkusername= True
                    break
            fin.close()
            if checkusername:
                if targetusername in usersonline:
                    targetusersocket=usersonline[targetusername]
                    conn.send("You are now connected with %s" %targetusername)
                else:
                    conn.send("User is not online")
            else:
                conn.send("Wrong Username")
                targetusersocket=None
            
            
        elif dataafterdecode=="Log Out the user:?" :
            conn.send("client,Log Out:?".encode("hex"))
            break
            
        else:
            if targetusersocket != None and targetusersocket!=conn:
                try:
                    targetusersocket.send('%s:' %targetusername +data)            
                except:
                    conn.send("%s has closed zagel" %targetusername)
                    
        dataafterdecode= None
        
        
    #came out of loop
    #delete user from online users list
    del usersonline[username]
    
    
#Check if username is registered or not,if it is registered check the passwords
def clientthread (conn,addr):
    dataafterdecode=None
    while True:
        checkusername = "False"
        checkuserpassword="False"          
        try:
            data = conn.recv(1024)
        except:
            #when client is disconnected
            print 'Disconnected with ' + addr[0] + ':' + str(addr[1])
            break
        try:   
            dataafterdecode=data.decode('hex')
        except:
            pass
        
        if dataafterdecode== "checkuser?"or  dataafterdecode=="registeruser?":
            username=conn.recv(1024)
            password=conn.recv(1024)
            fin = open('user.txt','r')
            usrlist = fin.readlines()
            for usr in usrlist:
                usr=usr.strip()
                x = usr.split(':')
                if x[0] == username:
                    checkusername="True"
                    if x[1]==password:
                        checkuserpassword= "True"
                        usersonline[username]=conn
                    break
            fin.close()
            if dataafterdecode=="registeruser?":
                if checkusername=="True":
                    conn.send("User name has already been used.")
                else:
                    f = open('user.txt','a')
                    f.write('\n'+username+':'+password)
                    f.close()
                    conn.send("You have registered sucessfully.Please login")
            else:
                conn.send(checkusername)
                time.sleep(0.01)
                conn.send(checkuserpassword)
                
            if (checkusername == "True" and checkuserpassword=="True" )and dataafterdecode=="checkuser?":
                liveconnection(conn,addr,username)
            
    #connection is closed,close the socket
    conn.close()
    
if __name__ == '__main__': 
    
    global usersonline
    usersonline=dict()
    HOST = socket.gethostname()  
    PORT = 9998 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created'
     
    #Bind socket to local host and port
    try:
        s.bind((HOST,PORT))
    except socket.error , msg:
        print False
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
         
    print 'Socket bind complete'
     
    #Start listening on socket
    s.listen(5)
    print 'Socket now listening'    
 
    #now keep talking with the client
    while 1:
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
         
        #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
        client=Thread(target=clientthread,args=(conn,addr))
        client.start()
        
    #close server socket after program ends
    s.close()
    
