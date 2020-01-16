import sys
import socket
import tkMessageBox
import threading
import time
import Tkinter as tk


'''Main Class'''

class MainFrame():
    
    def __init__ (self,parent=None):
        container = tk.Frame(parent,background="#b22222")
        container.columnconfigure(605, weight=1)
        container.rowconfigure(349, weight=1)      
        container.pack(side='top',expand=True,fill="both")
        global framesdict
        framesdict=dict()
        for F in (LoginPage,RegisterPage,ChatPage):
            frame=F(container,self)
            framesdict[F]=frame
            frame.grid(row=349,column=605,sticky="nsew")
            
            
        self.show_frame(LoginPage)
        
        
    def show_frame(self,frameclass):
        frame=framesdict[frameclass]
        if frameclass==LoginPage:
            frame.userentry.delete(first=0,last=tk.END)
            frame.passentry.delete(first=0,last=tk.END) 
        elif frameclass==RegisterPage:
            frame.userentry.delete(first=0,last=tk.END)
            frame.passentry.delete(first=0,last=tk.END)
            frame.passentry1.delete(first=0,last=tk.END)    
            
        frame.tkraise()
        
        
'''Login Frame '''
class LoginPage(tk.Frame):
    
        def __init__ (self,parent,controller):
                tk.Frame. __init__ (self,parent,background="#104e8b") 
                #Logo Image
                self.img = tk.PhotoImage(file="icon.gif")
                self.logo = tk.Label(self, image = self.img, background="#104e8b") 
                self.logo.pack()  
                #Label
                self.userlbl = tk.Label(self,text='User name', fg='white', bg='#104e8b')
                self.userlbl.pack()  
                #User name entry
                self.userentry = tk.Entry(self)
                self.userentry.pack()  
                #Label
                self.passlbl = tk.Label(self,text='Password',fg='white', bg='#104e8b')
                self.passlbl.pack()
                #Password Entry showing '*' instead of the password itself
                self.passentry = tk.Entry(self,show = '*')
                self.passentry.pack() 
                #Login Button calls function sendlogin sending userentry and passentry
                self.loginbtn = tk.Button(self,text='Login',fg="black",bg="white", command=lambda:sendlogin(self.userentry.get(),self.passentry.get(),controller))
                self.loginbtn.pack()
                #Label
                self.label2=tk.Label(self,text="Don't have a zagel?",fg="Black")
                self.label2.pack() 
                #Sign Up Button
                self.backbtn = tk.Button(self, text='Sign up',fg="black",bg="white",command=lambda:controller.show_frame(RegisterPage))
                self.backbtn.pack()
        
       

            
''' Register Frame'''            
class RegisterPage(tk.Frame):
    def __init__ (self,parent,controller):
        tk.Frame. __init__ (self,parent)
        self.img = tk.PhotoImage(file="icon.gif")
        self.logo = tk.Label(self, image = self.img)
        self.logo.pack()          
        #username
        self.userlbl = tk.Label(self,text='User name')
        self.userlbl.pack()
        self.userentry = tk.Entry(self)
        self.userentry.pack()
        #pass1
        self.passlbl = tk.Label(self,text='Password')
        self.passlbl.pack()
        self.passentry = tk.Entry(self,show = '*')
        self.passentry.pack()
        #pass2
        self.passlbl1 = tk.Label(self,text='Re-write Password')
        self.passlbl1.pack()
        self.passentry1 = tk.Entry(self,show = '*')
        self.passentry1.pack()   
        
        self.regbtn = tk.Button(self,text='Go and Zagel',command=lambda:registeruser(self.userentry.get(),self.passentry.get(),self.passentry1.get(),controller))
        self.regbtn.pack()
        self.backbtn1 = tk.Button(self, text='Back', command=lambda:controller.show_frame(LoginPage)).pack()  
        
'''ClientChat Frame  '''        
class ChatPage (tk.Frame) :
    global onlineuserslist
    def __init__ (self,parent,controller):
        tk.Frame. __init__ (self,parent) 
        #Send Button
        self.sendbtn = tk.Button(self,text='Send',command=send2server)
        self.sendbtn.place(relx=0.5, rely=0.63, height=33, width=116)
                
        #Chat Text
        self.Text1 = tk.Text(self,background="white",font='9',insertbackground="black",state="disabled")
        self.Text1.place(relx=0.02, rely=0.03, relheight=0.58, relwidth=0.95)
        
        #Scrollbar to navigate through chat 
        self.scrollbar = tk.Scrollbar(self, command=self.Text1.yview)
        self.scrollbar.place(relx=0.97,rely=0.03,relheight=0.58)         
        self.Text1['yscrollcommand'] = self.scrollbar.set
    
        #Chat entry box
        self.chatentry = tk.Entry(self,width=284)
        self.chatentry.place(relx=0.02, rely=0.63, relheight=0.09, relwidth=0.47)
        #Send username button
        self.useridbtn = tk.Button(self,text='Send ID',command=lambda:sendid(self.userentry.get()))
        self.useridbtn.place(relx=0.90, rely=0.63, height=34, width=57)
        #User Name Entry
        self.userentry = tk.Entry(self,width=284)
        self.userentry.place(relx=0.7, rely=0.63, relheight=0.1, relwidth=0.15)
        #Back Button
        self.logoutbtn = tk.Button(self,text='Log out',command=LogOut)
        self.logoutbtn.place(relx=0.5, rely=0.75, relheight=0.1, relwidth=0.15)
        #show usrlist
        self.usrlistbtn = tk.Button(self,text='Select receiver',command=self.onlineuser)
        self.usrlistbtn.place(relx=0.7, rely=0.75, relheight=0.1, relwidth=0.15) 
        
    #List box of online users    
    def onlineuser(self): 
        global onlineuserslist
        t = tk.Toplevel(self)
        t.title("Users List")
        t.columnconfigure(273, weight=1)
        t.rowconfigure(242, weight=1)  
        
        self.lbox = tk.Listbox(t)
        self.lbox.grid(row = 242,column=273,sticky="nsew")
        
        self.yscroll = tk.Scrollbar(t,command=self.lbox.yview)
        self.yscroll.grid(row=242,column=274,sticky=tk.N+tk.S+tk.E)    
            
            
        self.lbox.configure(yscrollcommand=self.yscroll.set)        
        self.lbox.bind("<Double-Button-1>", self.printlist)
        print "ff",onlineuserslist      
        for i in onlineuserslist:
            self.lbox.insert(tk.END, i)
    #send the user selected by anchor to server to connect with him        
    def printlist(self,z):
            x = self.lbox.get(tk.ANCHOR)
            sendid(x)
            
            
        
        
        

#ask user if he is sure to quit
def callback():
    if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
        ClientSocket.close()       
        root.destroy() 
        sys.exit()
'''Recieve data from server encoded, decode it then depending on the decoded data it decides what is the received data is for
:recieved chat or user to logout etc '''
def recievefromserver():
    frame=framesdict[ChatPage]
    global mylogin
    global Terminitarecvthread,onlineuserslist
    while 1:
        dataafterdecode=None
        try:
            recieved_data=ClientSocket.recv(1024)
        except:
            break
        
        try:
            dataafterdecode=recieved_data.decode('hex')
        except:
            pass 
        
        if dataafterdecode=='recieve':
            onlineuserslist=ClientSocket.recv(1024)
            onlineuserslist=onlineuserslist.split(':')
            onlineuserslist.remove(mylogin)
            
        elif dataafterdecode!="client,Log Out:?":
            frame.Text1.config(state="normal")
            frame.Text1.insert(tk.INSERT,recieved_data+'\n')
            frame.Text1.config(state="disabled")
            frame.Text1.see('end')
                
        if Terminitarecvthread:
            Terminitarecvthread=False
            break
        
        

#send id you want to connect to to the server
def sendid(username):
    requesttoserver="connect to a user:".encode("hex")
    ClientSocket.send(requesttoserver)
    targetid=username
    ClientSocket.send(targetid) 
    
#sends chat to server after getting the data from the entry    
def send2server():
    frame=framesdict[ChatPage]
    datatosend = frame.chatentry.get()
    ClientSocket.send(datatosend)
    frame.Text1.config(state="normal")  
    frame.Text1.tag_configure('tag-center', justify='right')
    frame.Text1.insert(tk.END,"You"+": "+datatosend+ '\n' , 'tag-center')  
    frame.Text1.config(state="disabled")     
    frame.chatentry.delete(first=0,last=tk.END)
        
        
#send  to server login username and password
def sendlogin(username,password,controller):
    global mylogin
    if len(username)==0:
        tkMessageBox.showwarning("Error",'Please enter Your username')        
    elif len(password)==0:
        tkMessageBox.showwarning("Error",'Please enter Your password')
    else:     
        ClientSocket.send("checkuser?".encode("hex"))
        time.sleep(0.001)
        ClientSocket.send(username)        
        time.sleep(0.001)
        ClientSocket.send(password)
        checkuser=ClientSocket.recv(1024) 
        checkpass=ClientSocket.recv(1024)          
        if checkuser== "True":
            if checkpass == "True":
                controller.show_frame(ChatPage)
                mylogin=username
                recievingthread=threading.Thread(target=recievefromserver)
                recievingthread.start()
            else:
                tkMessageBox.showwarning("Error",'Wrong Password')
        else:
            tkMessageBox.showwarning("Error",'Invalid Username')
        

#register new user
def registeruser(username,password,password1,controller):
      
    if len(password)==0 or len(username)==0:
        tkMessageBox.showwarning("Error",'Please fill the empty spaces')  
    elif password != password1:
        tkMessageBox.showwarning("Error",'Non_matching passwords')        
    else:
        ClientSocket.send("registeruser?".encode("hex"))
        time.sleep(0.1)
        ClientSocket.send(username)
        time.sleep(0.001)
        ClientSocket.send(password) 
        tkMessageBox.showwarning("Message",ClientSocket.recv(1024))
        controller.show_frame(LoginPage)
        frame=framesdict[RegisterPage]
        frame.userentry.delete(first=0,last=tk.END)
        frame.passentry.delete(first=0,last=tk.END)
        frame.passentry1.delete(first=0,last=tk.END)
        



#logout by terminating the thread not just leaving the frame
def LogOut():
    global Terminitarecvthread
    Terminitarecvthread=True
    ClientSocket.send("Log Out the user:?".encode("hex"))
    Thecontroller.show_frame(LoginPage)
    frame=framesdict[ChatPage]
    frame.Text1.config(state="normal")
    frame.Text1.delete('0.0',tk.END)
    frame.Text1.config(state="disabled")    
    



                    
if __name__ == '__main__':
    
    global Terminitarecvthread,onlineuserslist
    onlineuserslist=[5,3,2]
    Terminitarecvthread=False
    #create a socket and connect with the sever
    ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host=socket.gethostname()
    try:                
            ClientSocket.connect((host,9998))
    except:                       
            print "Connection Failed"
            
    
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", callback)
    root.wm_title("This is my title")
    root.geometry("605x349+297+259")
    root.title("Zagel")    
    Thecontroller=MainFrame(parent=root)
    guithread=threading.Thread(target=root.mainloop)
    guithread.start() 
    
    