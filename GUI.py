from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import threading
from threading import Thread
import math, os, shutil, time
from numpy import *
import re
global value
global i, xmin,xmax,ymin,ymax, valxprev,valyprev,valxnew,valynew, vali,valj, xMin,xMax,yMin,yMax, flag, valg, scalex, scaley, SelectedfileFlag, a, b, c, d
a,b,c,d=0,0,0,0
rectangle_width = 174.17
rectangle_height = 348.34
valuex, valuey, valuez=0,0,0
SelectedfileFlag=0
newest=''
to_exclude = ['select']

from numpy import *

for name in to_exclude:
    del globals()[name]
	
import json
import socket
from socket import *
import select
import time

data = None

#folder="/home/pi/Desktop/Orangewood_gerber"
folder="C:\\Users\\Ankit Kumar\\Desktop\\Deskto"

s = socket(AF_INET, SOCK_STREAM)             # TCP Socket
s1 = socket(AF_INET, SOCK_DGRAM)             # UDP Socket
print(s, type(s))
print("Socket made")
timeout = 3 # timeout in seconds
ready = select.select([s],[],[],timeout)

########### Functions #################

def utf8len(s):
    return len(s.encode('utf-8'))

def hashing(var):
    hash = 0
    i=0
    while(i<len(var)):
        c=var[i]
        i+=1
        hash += ord(c)%101

    return hash

def colorChange():
    """Changes the button's color"""
    global SelectedfileFlag
    clean()                                  # Cleans Target Folder
    global s1
    HOST = '0.0.0.0'                         # Listens from Devices on Network
    # Listen on Port
    PORT = 44444
    #Size of receive buffer
    BUFFER_SIZE = 1024
    # Bind the socket to the host and port
    s1.bind((HOST, PORT))
    data = s1.recvfrom(BUFFER_SIZE)
    Host=data[1]
    host=Host[0]                             # ESP's IP Address
# Close connection
    print(data[0], host)
    print("Closing Socket")
    s1.close()                               # Closes UDP Socket
    global s
    print("Connecting to " + host)
    port = 80
    s.connect((host,port))
    print("Connection made")
    ip_address=s.getsockname()[0]
    ipaddress.config(text="IP Address: "+ ip_address)   # Host's Ip Address
    print (ip_address)
    z1='Q'                       
    req=z1.encode()                          # Sends 'Q' to ESP
    s.sendall(req)
    e=s.recv(1)                              # Receives 'P' in return
    h=e.decode()
    print(h)
    Connectbutton.configure(bg = "red")      
    stopbutton.configure(bg = "white")
    pausebutton.configure(bg = "white")
    playbutton.configure(bg = "white")
    SelectedfileFlag=1
    rem()                                    # Makes Sure that not more that 1 file(Latest File) is in Target folder 

def clean():
    global folder
    for the_file in os.listdir(folder):      # Iteration on files present in Target Folder begins here.
        file_path = os.path.join(folder, the_file)     # Joins folder path and file name to obtain file path
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)         # Removes file from the folder iteratively.
        except Exception as e:               
            print(e)                         # Prints Exception
    	
def rem():
    t=threading.Timer(1.0, rem)              # Timer of Specified time 
    t.start()                                # Timer Starts
    global SelectedfileFlag, folder
    os.chdir(folder)                         # Changes working directory to Target Folder
    files=[]
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)	# Sorts File Present, Newest File lies at the End in the Target Folder
    if(len(files)>0):
        newest = files[-1]                                  # Newest File
        oldest = files[0:len(files)-1]                      # Oldest Files
        for i in oldest:                                    # Iterates on Oldest Files
            file_path=os.path.join(folder, i)               # Gets file_path by joining Folder and file name            
            os.unlink(file_path)                            # Unlinks File
        newfilename.config(text="File Name: "+newest)       # Displays Newest File Name present in the Folder ON GUI
        #SelectedfileFlag=1
        if(SelectedfileFlag==1):                          
           play()                                           # If File is found, Plots Gcode on GUI
           #SelectedfileFlag=0
    else:
        newfilename.config(text="Load File")                # If File is Not Found, displays text on GUI

def sethome():
    global valuex, valuey, valuez, s
    valuex, valuey, valuez=0,0,0
    selection = "X = " + str(valuex) + " Y = " + str(valuey) + " Z = " + str(valuez)
    currentX.config(text = selection)                       # Displays Coordinates on GUI
    if(int(movevar.get())==1):                              # If MoveCNC is enabled
        c='G'                                               # Sends 'G'                   
        e=c.encode()
        s.sendall(e)
        homeStr="G10L20P1X0Y0Z0\n$G\n$#\n"                 
        data={}                                             # Creates Empty Dictionary
        data["GCode"]=homeStr                               # Associates Value 'homeStr' with Key 'GCode'
        d=json.dumps(data)                                  # Dumps String in JSON Format
        b=d.encode()                                        
        s.sendall(b)                                        # Sends String 'homeStr', this Should Make MPOS X,Y,Z=0,0,0
    
        c=s.recv(1)                                         # Receives
        j=c.decode()
        print(j)
	
def xpos():
    value = entrybox.get()
    astring="Moving in X+ \nG00 X"
    debugSec.insert(INSERT, astring + value + "\n")
    global valuex, valuey, valuez, s
    valuex=int(value)+valuex
    selection = "X = " + str(valuex) + " Y = " + str(valuey) + " Z = " + str(valuez)
    currentX.config(text = selection)
    if(int(movevar.get())==1):
        homeStr="G90G0X"+str(valuex)+"\nG90\n"
        data={}
        data["GCode"]=homeStr
        d=json.dumps(data)
        print(d)
        b=d.encode()
        s.sendall(b)
    
        c=s.recv(128)
        j=c.decode()
        print(j)
        #Spindle_Position(j)

def xneg():
    value = entrybox.get()
    astring="Moving in X- \nG00 X-"
    debugSec.insert(INSERT, astring + value + "\n")
    global valuex, valuey, valuez, s
    valuex=valuex-int(value)
    selection = "X = " + str(valuex) + " Y = " + str(valuey) + " Z = " + str(valuez)
    currentX.config(text = selection)
    if(int(movevar.get())==1):
        homeStr="G90G0X"+str(valuex)+"\nG90\n"
        data={}
        data["GCode"]=homeStr
        d=json.dumps(data)
        b=d.encode()
        s.sendall(b)
    
        c=s.recv(128)
        j=c.decode()
        print(j)

def ypos():
    value = entrybox.get()
    astring="Moving in Y \nG00 Y"
    debugSec.insert(INSERT, astring + value + "\n")
    global valuex, valuey, valuez, s
    valuey=valuey+int(value)
    selection = "X = " + str(valuex) + " Y = " + str(valuey) + " Z = " + str(valuez)
    currentX.config(text = selection)
    if(int(movevar.get())==1):
        homeStr="G90G0Y"+str(valuey)+"\nG90\n"
        data={}
        data["GCode"]=homeStr
        d=json.dumps(data)
        b=d.encode()
        s.sendall(b)
    
        c=s.recv(128)
        j=c.decode()
        print(j)
	
def yneg():
    value = entrybox.get()
    astring="Moving in Y- \nG00 Y-"
    debugSec.insert(INSERT, astring + value + "\n")
    global valuex, valuey, valuez, s
    valuey=valuey-int(value)
    selection = "X = " + str(valuex) + " Y = " + str(valuey) + " Z = " + str(valuez)
    currentX.config(text = selection)
    if(int(movevar.get())==1):
        homeStr="G90G0Y"+str(valuey)+"\nG90\n"
        data={}
        data["GCode"]=homeStr
        d=json.dumps(data)
        b=d.encode()
        s.sendall(b)
    
        c=s.recv(128)
        j=c.decode()
        print(j)

def zpos():
    value = entrybox.get()
    astring="Moving in Z \nG00 Z"
    debugSec.insert(INSERT, astring + value + "\n")
    global valuex, valuey, valuez, s
    valuez=valuez+int(value)
    selection = "X = " + str(valuex) + " Y = " + str(valuey) + " Z = " + str(valuez)
    currentX.config(text = selection)
    if(int(movevar.get())==1):
        homeStr="G90G0Z"+str(valuez)+"\nG90\n"
        data={}
        data["GCode"]=homeStr
        d=json.dumps(data)
        b=d.encode()
        s.sendall(b)
    
        c=s.recv(128)
        j=c.decode()
        print(j)
	
def zneg():
    value = entrybox.get()
    astring="Moving in Z- \nG00 Z-"
    debugSec.insert(INSERT, astring + value + "\n")
    global valuex, valuey, valuez, s
    valuez=valuez-int(value)
    selection = "X = " + str(valuex) + " Y = " + str(valuey) + " Z = " + str(valuez)
    currentX.config(text = selection)
    if(int(movevar.get())==1):
        homeStr="G90G0Z"+str(valuez)+"\nG90\n"
        data={}
        data["GCode"]=homeStr
        d=json.dumps(data)
        b=d.encode()
        s.sendall(b)
    
        c=s.recv(128)
        j=c.decode()
        print(j)
	
def home():
    print("Moving to Home")
    global valuex, valuey, s
    if(int(movevar.get())==1):
        #homeStr="G90G0X"+str(valuex)+"Y"+str(valuey)+"\nG90\n"
        homeStr="$H"

        data={}
        data["GCode"]=homeStr
        d=json.dumps(data)
        b=d.encode()
        s.sendall(b)
    
        c=s.recv(128)
        j=c.decode()
        print(j)

def unlock():
    print("Moving to Home")
    global valuex, valuey, s
    if(int(movevar.get())==1):
        #homeStr="G90G0X"+str(valuex)+"Y"+str(valuey)+"\nG90\n"
        homeStr="$X"

        data={}
        data["GCode"]=homeStr
        d=json.dumps(data)
        b=d.encode()
        s.sendall(b)
    
        c=s.recv(128)
        j=c.decode()
        print(j)


def diag1():
    #print("Moving diagonally 1")
    value = entrybox.get()
    astring1="Moving diagonally 1 \nG00 X-"
    astring2=" Y"
    debugSec.insert(INSERT, astring1 + value + astring2 + value + "\n")
    global valuex, valuey, valuez, s
    valuex=valuex-int(value)
    valuey=valuey+int(value)
    selection = "X = " + str(valuex) + " Y = " + str(valuey) + " Z = " + str(valuez)
    currentX.config(text = selection)
    if(int(movevar.get())==1):
        homeStr="G90G0X"+str(valuex)+"Y"+str(valuey)+"\nG90\n"
        data={}
        data["GCode"]=homeStr
        d=json.dumps(data)
        b=d.encode()
        s.sendall(b)
    
        c=s.recv(128)
        j=c.decode()
        print(j)
	
def diag2():
    value = entrybox.get()
    astring1="Moving diagonally 2 \nG00 X"
    astring2=" Y"
    debugSec.insert(INSERT, astring1 + value + astring2 + value + "\n")
    global valuex, valuey, valuez, s
    valuex=valuex+int(value)
    valuey=valuey+int(value)
    selection = "X = " + str(valuex) + " Y = " + str(valuey) + " Z = " + str(valuez)
    currentX.config(text = selection)
    if(int(movevar.get())==1):
        homeStr="G90G0X"+str(valuex)+"Y"+str(valuey)+"\nG90\n"
        data={}
        data["GCode"]=homeStr
        d=json.dumps(data)
        b=d.encode()
        s.sendall(b)
    
        c=s.recv(128)
        j=c.decode()
        print(j)
	
def diag3():
    value = entrybox.get()
    astring1="Moving diagonally 3 \nG00 X-"
    astring2=" Y-"
    debugSec.insert(INSERT, astring1 + value + astring2 + value + "\n")
    global valuex, valuey, valuez, s
    valuex=valuex-int(value)
    valuey=valuey-int(value)
    selection = "X = " + str(valuex) + " Y = " + str(valuey) + " Z = " + str(valuez)
    currentX.config(text = selection)
    if(int(movevar.get())==1):
        homeStr="G90G0X"+str(valuex)+"Y"+str(valuey)+"\nG90\n"
        data={}
        data["GCode"]=homeStr
        d=json.dumps(data)
        b=d.encode()
        s.sendall(b)
    
        c=s.recv(128)
        j=c.decode()
        print(j)
	
def diag4():
    value = entrybox.get()
    astring1="Moving diagonally 3 \nG00 X"
    astring2=" Y-"
    debugSec.insert(INSERT, astring1 + value + astring2 + value + "\n")
    global valuex, valuey, valuez, s
    valuex=valuex+int(value)
    valuey=valuey-int(value)
    selection = "X = " + str(valuex) + " Y = " + str(valuey) + " Z = " + str(valuez)
    currentX.config(text = selection)
    if(int(movevar.get())==1):
        homeStr="G90G0X"+str(valuex)+"Y"+str(valuey)+"\nG90\n"
        data={}
        data["GCode"]=homeStr
        d=json.dumps(data)
        b=d.encode()
        s.sendall(b)
    
        c=s.recv(128)
        j=c.decode()
        print(j)

def increment():
	value=int(entrybox.get())                    # Gets Entry Box Value in 'Home' Tab
	value=value+1                                # Increment 1 to Current Value in Entry Box
	entrybox.delete(0, 'end')                    # Deletes Previous Entry 
	entrybox.insert(0, value)                    # Inserts Updated Entry
	
def decrement():
	value=int(entrybox.get())
	value=value-1
	entrybox.delete(0, 'end')
	entrybox.insert(0, value)
	
def multiplyTen():
	value=int(entrybox.get())
	value=value*10
	entrybox.delete(0, 'end')
	entrybox.insert(0, value)
	
def divideTen():
	value=int(entrybox.get())
	value=int(value/10)
	entrybox.delete(0, 'end')
	entrybox.insert(0, value)
'''	
def Scale():
	value=int(scaleBox.get())
	scaleBox.delete(0, 'end')
	scaleBox.insert(0, value)
	return value
'''

def checkered(canvas, scalex, scaley):
   # vertical lines at an interval of "line_distance" pixel
   for x in range(scalex,rectangle_width,scalex):
      w.create_line(x+25, 25, x+25, rectangle_height+25, fill="#476042")
   # horizontal lines at an interval of "line_distance" pixel
   for y in range(scaley,rectangle_height,scaley):
      w.create_line(25, y+25, rectangle_width+25, y+25, fill="#476042")
	  
def getScaleVal(): 
    scalex=int(var1.get())
    scaley=int(var2.get())
    checkered(w, scalex, scaley)

xmin,xmax,ymin,ymax, valxprev,valyprev,valxnew,valynew, vali,valj, xMin,xMax,yMin,yMax, flag, valg, scalex, scaley= 0.0,0.0,0.0,0.0, 0.0,0.0,0.0,0.0, 0.0,0.0, 0.0,0.0,0.0,0.0, 0, 0, 5, 5
x=''
y=''
i=''
j=''
g=''
	
def findMinMax(x1, x2, y1, y2, xc, yc,direction):
    # xMin, yMin, xMax, yMax
    # compute radius of circle
    global xMin, xMax, yMin, yMax
    radius = double(math.sqrt(pow((xc - x1), 2) + pow((yc - y1), 2)))

    # c(x1, x2, y1, y2, xc, yc):compute starting and ending points in polar coordinates
    # atan2 function is used so as to get the full range of the theta calculated .

    t1 = math.atan2((y1-yc) , (x1-xc))
    t2 = math.atan2((y2 - yc), (x2 - xc))

    # determine starting and ending polar angles

    if direction == 0:
        if (t1 < t2):
            tStart = t1
            tEnd = t2
        else:
            tStart = t2
            tEnd = t1

        delta = 0.01                          # increment Step
        '''
        xMin = xc + radius * cos(tStart)
        yMin = yc + radius * sin(tStart)
        xMax = xMin
        yMax = yMin
        '''
        theta = tStart

        while theta < tEnd:
            # compute coordinates
            x = xc + radius * cos(theta)
            y = yc + radius * sin(theta)

            if (x > xMax):
                xMax = x
            if (x < xMin):
                xMin = x
            if (y > yMax):
                yMax = y
            if (y < yMin):
                yMin = y

            theta = theta + delta


    elif direction == 1:
        if (t1 < t2):
            tStart = t2
            tEnd = t1
        else:
            tStart = t1
            tEnd = t2
        delta = 0.01

        theta = tStart

        while theta <= tEnd:
            # compute coordinates
            x = xc + radius * cos(theta)
            y = yc + radius * sin(theta)

            if (x > xMax):
                xMax = x
            if (x < xMin):
                xMin = x
            if (y > yMax):
                yMax = y
            if (y < yMin):
                yMin = y

            theta = theta + delta
    
    #print("findMinMax function values: xMax= {0}, xMin= {1}, yMax= {2}, yMin= {3}".format(xMax, xMin, yMax, yMin))
    # now scan the polar space at fixed radius and find the minimum AND maximum Cartesian x and y values
    # print ("cos of " + str(tStart) + " is : " + str(round(cos(tStart))))
    # initialize min and max coordinates to first point
    return xMin,yMin,xMax, yMax 


filename=''

def UploadAction(event=None):                            # USB Option of Uploading File
    global SelectedfileFlag, folder 
    print("SelectedFileFlag", SelectedfileFlag)	
    if(SelectedfileFlag==1):
        filename = filedialog.askopenfilename()          # Gets File Location
        print("UploadAction:", filename)
        folder, file = os.path.split(filename)           # Splits it into Folder and File                          
        BoundingBox(SelectedfileFlag, filename)          # Creates Bounding Box
    print('Selected:', filename, folder, file)

def BoundingBox(SelectedfileFlag, filename):
    global xmin,xmax,ymin,ymax,valuex, valuey
    xmin,xmax,ymin,ymax, valxprev,valyprev,valxnew,valynew, vali,valj, xMin,xMax,yMin,yMax, flag, valg, scalex, scaley= 0.0,0.0,0.0,0.0, 0.0,0.0,0.0,0.0, 0.0,0.0, 0.0,0.0,0.0,0.0, 0, 0, 5, 5
    x=''
    y=''
    i=''
    j=''
    g=''
    if(SelectedfileFlag==1):
        with open(filename,'r') as f:               # Opens File 
            for line in f.readlines():              # Reads Line
                for word in line.split():           # Splits line in to words
                    if(word[0]== "G"):              # Parsing Begins
                        g=word[1]
                        valg=float(g)	
                        if(valg==2):
                            flag=0
                        elif(valg==3):
                            flag=1   
                    elif(word[0] == "X"):
                        x=word[1:]
                        valxnew=float(x)
                        if(valxnew>xmax):
                            xmax=valxnew
                        if(valxnew<xmin):
                            xmin=valxnew
                    elif(word[0] == "Y"):
                        y=word[1:]
                        valynew=float(y)
                        if(valynew>ymax):
                            ymax=valynew
                        if(valynew<ymin):
                            ymin=valynew
                    elif(word[0]== "I"):
                        i=word[1:]
                        vali=float(i)
                    elif(word[0]== "J"):
                        j=word[1:]
                        valj=float(j)

                xMin, yMin, xMax, yMax = findMinMax(valxprev,valxnew, valyprev, valynew, valxprev + vali, valyprev + valj, flag)
                valxprev= valxnew
                valyprev= valynew
                vali=0
                valj=0	
        # minimum and maximum values from findMinMax and BoundingBox are compared 
        if(xmax<xMax):                 
            xmax=xMax
        if(xmin>xMin):
            xmin= xMin
        if(ymax<yMax):
            ymax=yMax
        if(ymin>yMin):
            ymin=yMin
    plot()             # Bounding Box is being plotted as per final values of xmax, xmin, ymax, ymin

def play():
    global SelectedfileFlag
    #SelectedfileFlag=1
    global folder
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)         
        BoundingBox(SelectedfileFlag, file_path)              # Plots Bounding Box

def clear():
    boundingbox=w.create_rectangle(2,2, rectangle_width+2, rectangle_height+2, fill='white')
    w.tag_raise(boundingbox)            # 'boundingbox' is placed highest on STACK

flag=0
prevx=0
prevy=0

global SetClear
SetClear=0

def Clear():
    global SetClear
    movevar.set("0")                    # Clear all Radio Buttons
    SetClear=1
    w.delete("all")
    boundingbox=w.create_rectangle(2,2, rectangle_width+2, rectangle_height+2, fill='white')
    w.tag_raise(boundingbox)

prevX, prevY=0,0

def move():
    global xmax, xmin, ymax, ymin, SetClear
    SetClear=0
    if(int(movevar.get())==2):
        t2=threading.Timer(1.0, plot)
        t2.start()
    elif(int(movevar.get())==1):
        t3=threading.Timer(1.0, Spindle_Display)
        t3.start()

SpindleX=0
SpindleY=0

def plot():
    global valuex, valuey,flag1, prevx,prevy, xmax, xmin,ymax,ymin, SetClear,a ,b, c, d
    t=threading.Timer(1.0, move)
    t.start()
    # (a,b) makes lower left coordinate of Bounding Box, c and d makes length and breadth of Bounding Box based on values of xmin, xmax, ymin, ymax, valuex, valuey
    a=(valuex/7.0)+2
    b=350.34-(valuey/7.0)
    c=float((xmax-xmin+valuex)/7.0+2)
    d=float(350.34-(ymax-ymin+valuey)/7.0)
    
    if(valuex!=prevx or valuey!=prevy):
        flag1=0

    if(a>=2 and b<=350.34 and c<=rectangle_width+2 and d>=2):                  # Condition for retaining Bounding Box within Canvas Boundary
        clear()
        if(SetClear==0):
            boundingbox=w.create_rectangle(a, b, c, d, fill = 'red')
            w.tag_raise(boundingbox)
            flag1=0
    elif(flag1==0):                                                            # If Condition isn't met then error is being shown
        top = Toplevel()
        top.title('Error')
        Message(top, text="Crossed CNC Bed").grid(row=0, column=1)
        top.after(1000, top.destroy)
        flag1=1	
    prevx=valuex
    prevy=valuey
    
global PauseFlag, PlayCounter
PauseFlag=0
initial=0
PlayCounter=0
switch=True
def PlayFile(): 
    initial=time.time()
    def runn():
        global running, initial, PauseFlag, PlayCounter, s, folder, file
        if(PlayCounter==0):  		# First time File is played
            print("PLAYFILE", folder, file)
            for file in os.listdir(folder):
                file_path = os.path.join(folder, file)
            data = open(file_path,"r")
            d = data.readlines()
            p=""
            i=0
            j=0
            dic ={}
            totalCount=0
            passk='F'
            passkey=passk.encode()
            s.sendall(passkey)

            while i<len(d):
                p=p+d[i]
                count= utf8len(d[i])                                     
                totalCount=totalCount+count
                if (totalCount>10 or i==len(d)-1):                         # create blocks of Gcode to be Processed
                    q={j:p}
                    p=""
                    dic.update(q)
                    totalCount=0
                    j+=1
                i+=1
            print(dic, i)
        i=0
        PlayCounter=1
        playbutton.configure(bg = "green")
        pausebutton.configure(bg = "white")
        stopbutton.configure(bg = "white")
        while(i<len(dic)):
            print(running)
            if(running == False):                                                       # when STOP button is Pressed
                break 
            a=json.dumps({"index":i, "GCode":dic[i], "Hash_value":hashing(dic[i])})     # Dumps Gcode in JSON Format
            b=a.encode()
            s.send(b)
            c=s.recv(1)
            j=c.decode()
            flag=1;
            if(PauseFlag==1 or j=='P'):                                                 # Pauses file when Pause button is clicked or 'P' is being received from ESP on Power Cut
                PauseFlag=1
                continue
            elif(j=='Y'):                                                               # Sends Next Block
                i=i+1
                j=""
            elif(j=='N'):                                                               # Doesn't send Next Block until 'Y' is being received
                while(j=='N'):
                    b=a.encode()
                    s.send(b)
                    c=s.recv(1)
                    j=c.decode()
                    if(j=='Y'):
                        i=i+1
                        j=""
            else:
                break
        l='@'                                                                           # Stops File Processing
        m=l.encode()
        s.sendall(m)
        PlayCounter=0
        PauseFlag=0
        stopbutton.configure(bg = "red")
        pausebutton.configure(bg = "white")
        playbutton.configure(bg = "white")
        data.close() 
    thread = threading.Thread(target=runn)  
    thread.start()  	

def Play():
    global running, PauseFlag
    PauseFlag=0                                          # Disables Pause FLag
    running = True                                       # Make Gcode Blocks running
    PlayFile()

def Stop():
    global running, initial
    running = False
    final=time.time()
    stopbutton.configure(bg = "red")
    pausebutton.configure(bg = "white")
    playbutton.configure(bg = "white")
    print("Time:"+(final-initial))

def Pause():
    global PauseFlag
    PauseFlag=1                                          # Enables PauseFlag
    pausebutton.configure(bg = "orange")
    playbutton.configure(bg = "White")
    stopbutton.configure(bg = "White")
    
def GRBL_Settings():
    '''
    STEPS="$100="+XSteps.get()+"\n" + "$101="+YSteps.get()+"\n" + "$102="+YSteps.get()+"\n"
    MAXRATE="$110="+XMaxRate.get()+"\n" + "$111="+YMaxRate.get()+"\n" + "$112="+ZMaxRate.get()+"\n"
    ACCELERATION="$120="+XAcceleration.get()+"\n" + "$121="+YAcceleration.get()+"\n" + "$122="+ZAcceleration.get()+"\n"
    SettingSec.insert(INSERT, STEPS+MAXRATE+ACCELERATION + "\n")
    '''
    c='G'
    e=c.encode()
    s.sendall(e)
    homeStr="$"+str(getGRBL.get())+"="+str(valueGRBL.get())                 # Creates string of format "$100=100" to be sent to ESP
    print(homeStr)
    data={}
    data["GCode"]=homeStr
    d=json.dumps(data)
    b=d.encode()
    s.sendall(b)
    
    c=s.recv(128)
    j=c.decode()
    print(j)

def Spindle_Position(text): 
    global SpindleX, SpindleY
    x1=text.find("W")
    b=text[x1+5:]

    data=b.split(",")
    # Spindle Position of X, Y based on MPOS String
    SpindleX=data[0]
    SpindleY=data[1]
delete=0
def Spindle_Display():
    global SpindleX, SpindleY, valuex, valuey, delete, a, b, c, d
    t=threading.Timer(0.1, move)
    t.start()
    w.delete("all")
    clear()
    boundingbox=w.create_rectangle(a, b, c, d, fill = 'red')
    w.tag_raise(boundingbox)
    spindle=w.create_oval((valuex-30)/7.0, 350.34-(valuey-30)/7.0, (valuex+30)/7.0, 350.34- (valuey+30)/7.0, fill="green")    # use SpindleX and SpindleY to display Spindle Position
    w.tag_raise(spindle)
    if(SetClear==1):
        w.delete('all')
        clear()

def SET_X_STEPS():
    v10.set("100")

def SET_Y_STEPS():
    v10.set("101")

def SET_Z_STEPS():
    v10.set("102")

def SET_X_MAX():
    v10.set("110")

def SET_Y_MAX():
    v10.set("111")

def SET_Z_MAX():
    v10.set("112")

def SET_X_ACCELERATION():
    v10.set("120")

def SET_Y_ACCELERATION():
    v10.set("121")

def SET_Z_ACCELERATION():
    v10.set("122")

def incrementGRBL():
    value1=int(variable.get())
    value2=int(valueGRBL.get())
    value=value1+value2
    valueGRBL.delete(0, 'end')
    valueGRBL.insert(0, value)

def decrementGRBL():
    value1=int(variable.get())
    value2=int(valueGRBL.get())
    value=value2-value1
    valueGRBL.delete(0, 'end')
    valueGRBL.insert(0, value)

GRBL_code=[]
GRBL_value=[]

def Refresh():
    counter=0
    c='G'
    e=c.encode()
    s.sendall(e)
    homeStr="$$"                                               
    data={}
    data["GCode"]=homeStr
    d=json.dumps(data)
    b=d.encode()
    s.sendall(b)
    
    c1=s.recv(1024)                                            # Receives GRBL Settings
    L1=c1.decode()
    L=(re.split('\n', L1))
    if 'Y' in L:
        L.remove('Y')
    print("L1", L1)
    print(L)
    GRBL_code=[]
    GRBL_value=[]

    for x in L:
        if(x.startswith('$')):                                 # Parses String Received from ESP
            x1=x.find(" ")
            #b=x[0:x1]
            #print(b)
            head, sep, tail=x.partition('=')                   # Seperates it into head, tail w.r.t partition symbol
            GRBL_code.append(head)
            GRBL_value.append(tail)
    x=0
    print(GRBL_code, GRBL_value)
    x=GRBL_code.index("$100")
    y=GRBL_value[x]
    v1.set(y)
    y=GRBL_value[x+1]
    v2.set(y)
    y=GRBL_value[x+2]
    v3.set(y)
    y=GRBL_value[x+3]
    v4.set(y)
    y=GRBL_value[x+4]
    v5.set(y)
    y=GRBL_value[x+5]
    v6.set(y)
    y=GRBL_value[x+6]
    v7.set(y)
    y=GRBL_value[x+7]
    v8.set(y)
    y=GRBL_value[x+8]
    v9.set(y)

# Input Parameters:
# (x1, y1) first point on arc
# (x2, y2) second point on arc
# (xc, yc) center point of circle
# direction : 1 ( clockwise ) , 0 ( anticlockwise )
	  
########## CNC Control Window ###########
	
main=Tk()                                                        # Main Window
main.title("CNC Control Box")                                    # Title of the Main Window
main.geometry('{}x{}'.format(500, 300))
noteb = ttk.Notebook(main)                                       # Tabs Creation
noteb.grid(row=1, column=0, columnspan='50', rowspan='49')
window=ttk.Frame(noteb)
noteb.add(window, text='Home')
window2=ttk.Frame(noteb)
noteb.add(window2, text='Settings')

############### Frames ##################

frame0=Frame(window)
frame0.grid(row=0, column=0, sticky='N')

frame1=Frame(window)
frame1.grid(row=1, column=0, sticky='N')

frame3=Frame(window)
frame3.grid(row=2, column=0, sticky='N')

frame4=Frame(window)
frame4.grid(row=3, column=0)

frame5=Frame(window)
frame5.grid(row=4, column=0)

frame6=Frame(window2)
frame6.grid(row=0, column=0, sticky='W')

frame7=Frame(window2)
frame7.grid(row=1, column=0, sticky='W', pady=20)

frame8=Frame(window2)
frame8.grid(row=2, column=0, sticky='W')

############### Labels ##################

currentX=Label(frame1, height='1', width='20')
currentX.grid(row=2, column=0)

zlabel=Label(frame3, text="Z", height='1', width='2')
zlabel.grid(row=0, column=0)

ylabel=Label(frame3, text="Y", height='1', width='2')
ylabel.grid(row=0, column=3)

xlabel=Label(frame3, text="X", height='2', width='2')
xlabel.grid(row=2, column=1)

setXSteps=Label(frame6, text="$100", height='1', width='4')
setXSteps.grid(row=0, column=0, sticky='W')
xstepbutton=Button(frame6, text='X steps/mm', height='1', width='20', command=SET_X_STEPS)
xstepbutton.grid(row=0, column=1)
v1=StringVar(frame6, value="250.00")
XSteps=Entry(frame6, width='7', textvariable=v1)
XSteps.grid(row=0, column=2, columnspan=2)

setYSteps=Label(frame6, text="$101", height='1', width='4')
setYSteps.grid(row=1, column=0, sticky='W')
ystepbutton=Button(frame6, text='Y steps/mm', height='1', width='20', command=SET_Y_STEPS)
ystepbutton.grid(row=1, column=1)
v2=StringVar(frame6, value="250.00")
YSteps=Entry(frame6, width='7', textvariable=v2)
YSteps.grid(row=1, column=2, columnspan=2)

setZSteps=Label(frame6, text="$102", height='1', width='4')
setZSteps.grid(row=2, column=0, sticky='W')
zstepbutton=Button(frame6, text='Z steps/mm', height='1', width='20', command=SET_Z_STEPS)
zstepbutton.grid(row=2, column=1)
v3=StringVar(frame6, value="250.00")
ZSteps=Entry(frame6, width='7', textvariable=v3)
ZSteps.grid(row=2, column=2, columnspan=2)

setXMaxRate=Label(frame6, text="$110", height='1', width='4')
setXMaxRate.grid(row=3, column=0, sticky='W')
xmaxbutton=Button(frame6, text='X Max Rate, mm/min', height='1', width='20', command=SET_X_MAX)
xmaxbutton.grid(row=3, column=1)
v4=StringVar(frame6, value="500.00")
XMaxRate=Entry(frame6, width='7', textvariable=v4)
XMaxRate.grid(row=3, column=2, columnspan=2)

setYMaxRate=Label(frame6, text="$111", height='1', width='4')
setYMaxRate.grid(row=4, column=0, sticky='W')
ymaxbutton=Button(frame6, text='Y Max Rate, mm/min', height='1', width='20', command=SET_Y_MAX)
ymaxbutton.grid(row=4, column=1)
v5=StringVar(frame6, value="500.00")
YMaxRate=Entry(frame6, width='7', textvariable=v5)
YMaxRate.grid(row=4, column=2, columnspan=2)

setZMaxRate=Label(frame6, text="$112", height='1', width='4')
setZMaxRate.grid(row=5, column=0, sticky='W')
zmaxbutton=Button(frame6, text='Z Max Rate, mm/min', height='1', width='20', command=SET_Z_MAX)
zmaxbutton.grid(row=5, column=1)
v6=StringVar(frame6, value="500.00")
ZMaxRate=Entry(frame6, width='7', textvariable=v6)
ZMaxRate.grid(row=5, column=2, columnspan=2)

setXAcceleration=Label(frame6, text="$120", height='1', width='4')
setXAcceleration.grid(row=6, column=0, sticky='W')
setxaccelerationbutton=Button(frame6, text='X Acceleration, mm/sec^2 ', height='1', width='20', command=SET_X_ACCELERATION)
setxaccelerationbutton.grid(row=6, column=1)
v7=StringVar(frame6, value="10.00")
XAcceleration=Entry(frame6, width='7', textvariable=v7)
XAcceleration.grid(row=6, column=2, columnspan=2)

setYAcceleration=Label(frame6, text="$121", height='1', width='4')
setYAcceleration.grid(row=7, column=0, sticky='W')
setyaccelerationbutton=Button(frame6, text='Y Acceleration, mm/sec^2 ', height='1', width='20', command=SET_Y_ACCELERATION)
setyaccelerationbutton.grid(row=7, column=1)
v8=StringVar(frame8, value="10.00")
YAcceleration=Entry(frame6, width='7', textvariable=v8)
YAcceleration.grid(row=7, column=2, columnspan=2)

setZAcceleration=Label(frame6, text="$122", height='1', width='4')
setZAcceleration.grid(row=8, column=0, sticky='W')
setzaccelerationbutton=Button(frame6, text='Z Acceleration, mm/sec^2 ', height='1', width='20', command=SET_Z_ACCELERATION)
setzaccelerationbutton.grid(row=8, column=1)
v9=StringVar(frame8, value="10.00")
ZAcceleration=Entry(frame6, width='7', textvariable=v9)
ZAcceleration.grid(row=8, column=2, columnspan=2)

slabel=Label(frame7, text="$", height='1', width='1')
slabel.grid(row=1, column=0, sticky='W')
v10=StringVar(frame7, value='0')
getGRBL=Entry(frame7, width='7', textvariable=v10)
getGRBL.grid(row=1, column=1)
equallabel=Label(frame7, text="=", height='1', width='1')
equallabel.grid(row=1, column=2, sticky='W')
v11=StringVar(frame7, value='0')
valueGRBL=Entry(frame7, width='7', textvariable=v11)
valueGRBL.grid(row=1, column=3)
v12=StringVar(frame7, value='10')
changeamountGRBL=Entry(frame7, width='7', textvariable=v12)
changeamountGRBL.grid(row=1, column=4, padx=10)
GRBL_Update= Button(frame7, text="Update", height='1', width='7', command=GRBL_Settings)
GRBL_Update.grid(row=1, column=5)

OPTIONS = ["1","10","100", "1000", "10000"]
variable = StringVar(frame7)
variable.set(OPTIONS[0])

w1 = OptionMenu(frame7, variable, *OPTIONS)
w1.config(width='5')
w1.grid(row=1, column=4, padx=10)

addvalueGRBL=Button(frame7, text="+", height='1', width='1', command=incrementGRBL)
addvalueGRBL.grid(row=0, column=3)

subvalueGRBL=Button(frame7, text="-", height='1', width='1', command= decrementGRBL)
subvalueGRBL.grid(row=2, column=3)

UnlockGRBL=Button(frame8, text="Unlock", height='1', width='7', command= unlock)
UnlockGRBL.grid(row=0, column=3)

homeGRBL=Button(frame8, text="Home", height='1', width='7', command= home)
homeGRBL.grid(row=0, column=4)

#scalelabel=Label(frame6, text="SCALE:", height='2', width='8')
#scalelabel.grid(row=5, column=0)

Refresh= Button(frame7, text="Refresh", height='1', width='7', command=Refresh)
Refresh.grid(row=2, column=5)



############### Manual Control Panel ##################

Connectbutton=Button(frame0, text="Connect", height='2', width='8', command = colorChange)
Connectbutton.grid(row=0, column=0, padx=(0, 2))

SetHomebutton=Button(frame0, text="Set Home", height='2', width='8', command=sethome)
SetHomebutton.grid(row=0, column=3, padx=(0, 2))

clearbutton=Button(frame0, text="Clear", height='2', width='8', command = Clear)
clearbutton.grid(row=0, column=4)

ipaddress = Label(frame1, height=1, width=25)
ipaddress.grid(row=0, column=0, sticky="e")

newfilename = Label(frame1, height=1, width=20)
newfilename.grid(row=1, column=0)

zpbutton=Button(frame3, text="+", height='2', width='2', command=zpos)
zpbutton.grid(row=1, column=0, padx=(10,10), pady=5)

xnypbutton= Button(frame3, height='2', width='2', command= diag1)
xnypbutton.grid(row=1, column=2, padx=(0,5))

ypbutton= Button(frame3, text="+", height='2', width='2', command=ypos)
ypbutton.grid(row=1, column=3)

xpypbutton= Button(frame3, height='2', width='2', command=diag2)
xpypbutton.grid(row=1, column=4)

mulbutton= Button(frame3, text="x10", height='1', width='2', command=multiplyTen)
mulbutton.grid(row=1, column=5)

addbutton= Button(frame3, text="+", height='1', width='2', command=increment)
addbutton.grid(row=1, column=6)

xnbutton= Button(frame3, text="-", height='2', width='2', command=xneg)
xnbutton.grid(row=2, column=2, padx=(0,5))

homebutton= Button(frame3, text="O", height='2', width='2')
homebutton.grid(row=2, column=3)

xpbutton= Button(frame3, text="+", height='2', width='2', command=xpos)
xpbutton.grid(row=2, column=4, padx=(5, 5))

v=StringVar(window, value="20")
entrybox=Entry(frame3, width='7', textvariable=v)
entrybox.grid(row=2, column=5, columnspan=2)

znbutton=Button(frame3, text="-", height='2', width='2', command=zneg)
znbutton.grid(row=3, column=0)

xnynbutton= Button(frame3, height='2', width='2', command=diag3)
xnynbutton.grid(row=3, column=2, padx=(0,5))

ynbutton= Button(frame3, text="-", height='2', width='2', command=yneg)
ynbutton.grid(row=3, column=3, pady=5)

xpynbutton= Button(frame3, height='2', width='2', command=diag4)
xpynbutton.grid(row=3, column=4, pady=5)

divbutton= Button(frame3, text="/10", height='1', width='2', command=divideTen)
divbutton.grid(row=3, column=5, pady=5)

subbutton= Button(frame3, text="-", height='1', width='2', command=decrement)
subbutton.grid(row=3, column=6)
'''
var1 = IntVar()
scaleXBox = Scale(frame6, orient='horizontal', from_=0, to=20, variable = var1, tickinterval=5)
scaleXBox.grid(row=5, column=0, padx=(0,5))
var2 = IntVar()
scaleYBox = Scale(frame6, orient='vertical', from_=0, to=20, variable = var2, tickinterval=5)
scaleYBox.grid(row=5, column=1)
button = Button(frame7, text="Get Scale Value", command=getScaleVal)
button.grid(row=6, column=2)
'''

movevar = IntVar()
moveCNC = Radiobutton(frame5, text="Move CNC", variable=movevar, value=1, command=move)
moveCNC.grid(row=0, column=0, columnspan=2)

moveGcode = Radiobutton(frame5, text="Move GCode", variable=movevar, value=2, command=move)
moveGcode.grid(row=0, column=2, columnspan=2)

label = Label(frame5)
label.grid(row=0, column=4)

#print("Scale Value X: {0}".format(var.get()))
#label = Label(frame7)
#label.grid(row=6, column=2)

############## FILE CONTROL PANEL ################

importbutton=Button(frame4, text="U", height='2', width='3', command=UploadAction)
importbutton.grid(row=0, column=0, padx=(0,5))

playbutton=Button(frame4, text="|>", height='2', width='3', command=Play)
playbutton.grid(row=0, column=1, padx=(0,5))

pausebutton=Button(frame4, text="||", height='2', width='3', command=Pause)
pausebutton.grid(row=0, column=2, padx=(0,10))

stopbutton=Button(frame4, text="[]", height='2', width='3', command=Stop)
stopbutton.grid(row=0, column=3)

############## CANVAS BEDSHEET ##################

w = Canvas(window, width=175.2, height=350.4)
w.grid(row=0, column=4, rowspan=5)

bedarea=w.create_rectangle(2, 2, rectangle_width+2, rectangle_height+2)
spindle=w.create_oval(valuex-1, valuey-1, valuex+1, valuey+1, fill="green")
w.tag_raise(spindle)

#scale1=int(var.get())
#scale1=changescale(val)
#print("h",scale1)
#checkered(w, 5)

############### Debugger Box ####################

debugSec=Text(window, width=25, height=20, fg="red")
debugSec.insert(1.0, "Debugger>>\n")
debugSec.grid(row=0, column=5, rowspan=5, sticky='N')

SettingSec=Text(frame6, width=45, height=12, fg="red")
SettingSec.insert(1.0, "Debugger>>\n")
SettingSec.grid(row=0, column=5, rowspan=30, padx=(10,0), pady=(1,0), sticky='N')

main.mainloop()
