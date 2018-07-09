#Tested Move GCode and Move CNC

from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import threading
from threading import Thread
import math, os, shutil, time
from numpy import *
import re
#from tkinter import messagebox
global value
global i, xmin,xmax,ymin,ymax, valxprev,valyprev,valxnew,valynew, vali,valj, xMin,xMax,yMin,yMax, flag, valg, scalex, scaley, SelectedfileFlag, flagRemoveBound
rectangle_width = 203.2
rectangle_height = 406.4
valuex, valuey, valuez=0,0,0
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

s = socket(AF_INET, SOCK_STREAM)
s1 = socket(AF_INET, SOCK_DGRAM)
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
    #SelectedfileFlag=
    #clean()
    global s1
    HOST = '0.0.0.0'
    # Listen on Port
    PORT = 44444
    #Size of receive buffer
    BUFFER_SIZE = 1024
    # Bind the socket to the host and port
    s1.bind((HOST, PORT))
    data = s1.recvfrom(BUFFER_SIZE)
    Host=data[1]
    host=Host[0]
# Close connection
    print(data[0], host)
    print("Closing Socket")
    s1.close()
    global s
    #host='192.168.43.147'
    print("Connecting to " + host)
    port = 80
    s.connect((host,port))
    print("Connection made")
    ip_address=s.getsockname()[0]
    ipaddress.config(text="IP Address: "+ ip_address)   
    print (ip_address)
    z1='Q'
    req=z1.encode()
    s.sendall(req)
    e=s.recv(1)
    h=e.decode()
    print(h)
    Connectbutton.configure(bg = "red")
    #os.system('./shell.sh')
    #print("Server Executed ")

    SelectedfileFlag=1
    rem()
    #print("Ab Play Chalega")
#    '''
    #os.system(folder) # This will change the present working directory 
    #os.system("uwsgi --socket 0.0.0.0:8080 --protocol=http -w run:app")

def clean():
    global folder
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
    
	
def rem():
    t=threading.Timer(1.0, rem)
    t.start()
    #t=threading.Thread(target=rem)
    #t.start()
    global SelectedfileFlag
    global folder
    os.chdir(folder)
    files=[]
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    if(len(files)>0):
        newest = files[-1]
        oldest = files[0:len(files)-1]
    #print(newest)
        for i in oldest:
            file_path=os.path.join(folder, i)
            print(file_path)
            os.unlink(file_path)
        newfilename.config(text="File Name: "+newest)
        if(SelectedfileFlag==1):
           print("first pl,ay")
           play()
           SelectedfileFlag=0
    else:
        newfilename.config(text="Load File")

def sethome():
    global valuex, valuey, valuez, s
    valuex, valuey, valuez=0,0,0
    selection = "X = " + str(valuex) + " Y = " + str(valuey) + " Z = " + str(valuez)
    currentX.config(text = selection)
    if(int(movevar.get())==1):
        c='G'
        e=c.encode()
        #print("wtf1")
        s.sendall(e)
        homeStr="G10L20P1X0Y0Z0\n$G\n$#\n"
        data={}
        data["GCode"]=homeStr
        d=json.dumps(data)
        print(d)
        b=d.encode()
        print("wtf1")
        s.sendall(b)
    
        c=s.recv(1)
        print("wtf2")
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
        print("wtf1")
        s.sendall(b)
    
        c=s.recv(128)
        print("wtf2")
        j=c.decode()
        print(j)
        Spindle_Position(j)

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
        print("wtf2")
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
        print("wtf2")
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
        print("wtf2")
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
        print("wtf2")
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
        print("wtf2")
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
        print("wtf2")
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
        print("wtf2")
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
        print("wtf2")
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
        print("wtf2")
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
        print("wtf2")
        j=c.decode()
        print(j)

def increment():
	value=int(entrybox.get())
	value=value+1
	entrybox.delete(0, 'end')
	entrybox.insert(0, value)
	
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
    #selection = "Value of X = " + str(var1.get()) + " Value of Y = " + str(var2.get())
    #label.config(text = selection) 
    scalex=int(var1.get())
    scaley=int(var2.get())
    #print("scaleX= {0}, scaleY= {1}".format(scalex, scaley))
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

        delta = 0.01
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
        '''
        xMin = xc + radius * cos(tStart)
        yMin = yc + radius * sin(tStart)
        xMax = xMin
        yMax = yMin
        '''
        theta = tStart
        #tEnd = tEnd + 6.283

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
                #print("yMin has now been changed at X: " + str(x) + " Y: " + str(y))
                yMin = y

            theta = theta + delta
    
    #print("findMinMax function values: xMax= {0}, xMin= {1}, yMax= {2}, yMin= {3}".format(xMax, xMin, yMax, yMin))
    # now scan the polar space at fixed radius and find the minimum AND maximum Cartesian x and y values
    # print ("cos of " + str(tStart) + " is : " + str(round(cos(tStart))))
    # initialize min and max coordinates to first point

    # display min and max values
    #print("xMin = " + str(xMin) + " yMin = " + str(yMin))
    #print("xMax = " + str(xMax) + " yMax = " + str(yMax))
    return xMin,yMin,xMax, yMax 
	
#findMinMax(-1/1.41, 1/1.41, 1/1.41, -1/1.41, 0, 0,0)

SelectedfileFlag, flagRemoveBound =0, 0
filename=''


def UploadAction(event=None):                             # Import File is getting selected and needs to be saved on RaspberryPi
    global SelectedfileFlag
    if(SelectedfileFlag==1):
        filename = filedialog.askopenfilename()
        global folder
        folder, file = os.path.split(filename)
        print(folder, file)
        BoundingBox(SelectedfileFlag, filename)
    print('Selected:', filename)

def BoundingBox(SelectedfileFlag, filename):
    global xmin,xmax,ymin,ymax,valuex, valuey
    xmin,xmax,ymin,ymax, valxprev,valyprev,valxnew,valynew, vali,valj, xMin,xMax,yMin,yMax, flag, valg, scalex, scaley= 0.0,0.0,0.0,0.0, 0.0,0.0,0.0,0.0, 0.0,0.0, 0.0,0.0,0.0,0.0, 0, 0, 5, 5
    x=''
    y=''
    i=''
    j=''
    g=''
    if(SelectedfileFlag==1):
        with open(filename,'r') as f:
            for line in f.readlines():
                for word in line.split():
                    if(word[0]== "G"):
                        g=word[1]
                        valg=float(g)	
                        #print(valg)
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
                            #print(x)
                    elif(word[0] == "Y"):
                        y=word[1:]
                        valynew=float(y)
                        if(valynew>ymax):
                            ymax=valynew
                        if(valynew<ymin):
                            ymin=valynew
                            #print(y)
                    elif(word[0]== "I"):
                        i=word[1:]
                        vali=float(i)
                        #print(vali)
                    elif(word[0]== "J"):
                        j=word[1:]
                        valj=float(j)
                        #print(valj)
			    
                #print("Vali={0}, Valj={1}\n".format(vali, valj))
                #print("Valxprev={0}, Valxnew={1}, Valyprev={2}, Valynew={3}, Xcentre={4}, Ycentre={5}, Flag={6}\n".format(valxprev ,valxnew, valyprev, valynew, valxprev+vali, valyprev+valj, flag)) 
                xMin, yMin, xMax, yMax = findMinMax(valxprev,valxnew, valyprev, valynew, valxprev + vali, valyprev + valj, flag)
                #xMin,yMin,xMax,yMax=findMinMax(valxprev ,valxnew, valyprev, valynew, valxprev + vali, valyprev + valj, flag)
                valxprev= valxnew
                valyprev= valynew
                vali=0
                valj=0
#print("xmax={0}, xMax={1} \n".format(xmax, float(xMax)))
#print("xmin={0}, xMin={1} \n".format(xmin, float(xMin)))
#print("ymax={0}, yMax={1} \n".format(ymax, float(yMax)))
#print("ymin={0}, yMin={1} \n".format(ymin, float(yMin)))	

        if(xmax<xMax):
            xmax=xMax
        if(xmin>xMin):
            xmin= xMin
        if(ymax<yMax):
            ymax=yMax
        if(ymin>yMin):
            ymin=yMin
        #print(xmax)
        #print(xmin)
        #print(ymax)
        #print(ymin)
    #elif(SelectedfileFlag==0):
    #   xmax,xmin,ymax,ymin=0.0,0.0,0.0,0.0
    plot()

def play():
    
    SelectedfileFlag=1
    global folder
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        BoundingBox(SelectedfileFlag, file_path)
    #t1.cancel()

def clear():
    boundingbox=w.create_rectangle(2,2, rectangle_width+2, rectangle_height+2, fill='white')
    w.tag_raise(boundingbox)

flag=0
prevx=0
prevy=0

global SetClear
SetClear=0

def Clear():
    w.delete("all")
    global a,b,c,d
    a,b,c,d=0,0,0,0
    SetClear=1
    boundingbox=w.create_rectangle(2,2, rectangle_width+2, rectangle_height+2, fill='white')
    w.tag_raise(boundingbox)

def move():
    global xmax, xmin, ymax, ymin
    if(int(movevar.get())==2):
        t2=threading.Timer(1.0, plot)
        t2.start()
    #elif(int(movevar.get())==1):

SpindleX=100
SpindleY=100

def plot():
    print("Plot Hua")
    global valuex, valuey,flag1, prevx,prevy, xmax, xmin,ymax,ymin, SetClear
    t=threading.Timer(1.0, move)
    t.start()
    #clear()
    print(xmax, xmin, ymax, ymin, valuex, valuey)
    a=(valuex/6.0)+2
    b=408.4-(valuey/6.0)
    c=float((xmax-xmin+valuex)/6.0+2)
    d=float(408.4-(ymax-ymin+valuey)/6.0)
    print(a, b, c, d)
    
    if(SetClear==1):
        a,b,c,d, valuex, valuey, xmin, xmax, ymin, ymax=0,0,0,0, 0, 0, 0, 0, 0, 0
    if(valuex!=prevx or valuey!=prevy):
        flag1=0

    if(a>=2 and b<=408.4 and c<=rectangle_width+2 and d>=2):
        clear()
        print("Bounding Box Banega CNC Bed pe")
        if(SetClear==0):
            boundingbox=w.create_rectangle(a, b, c, d, fill = 'red')
            w.tag_raise(boundingbox)
            flag1=0
    elif(flag1==0):
        top = Toplevel()
        top.title('Error')
        Message(top, text="Crossed CNC Bed").grid(row=0, column=1)
        top.after(1000, top.destroy)
        flag1=1	
    prevx=valuex
    prevy=valuey
    global SpindleX, SpindleY
    spindle=w.create_oval((SpindleX-30)/6.0, 408.4-(SpindleY-30)/6.0, (SpindleX+30)/6.0, 408.4- (SpindleY+30)/6.0, fill="green")
    w.tag_raise(spindle)
    #t.cancel()

initial=0
switch=True
def PlayFile(): 
    initial=time.time()
    def runn():
        global running, initial
        global s
        global folder, file
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
            if (totalCount>10 or i==len(d)-1):
                q={j:p}
                p=""
                dic.update(q)
                totalCount=0
                j+=1
            i+=1
        i=0
		
        while(i<len(dic)):
            print(running)
            if(running == False):  
                break 
            a=json.dumps({"index":i, "GCode":dic[i], "Hash_value":hashing(dic[i])})
            b=a.encode()
            s.send(b)
            c=s.recv(1)
            j=c.decode()
            print(j)
            flag=1;
            if(j=='Y'):
                i=i+1
                j=""
            elif(j=='N'):
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
        l='@'
        m=l.encode()
        s.sendall(m)
        data.close() 
    thread = threading.Thread(target=runn)  
    thread.start()  	

def Play():
    global running
    running = True
    PlayFile()

def Stop():
    global running, initial
    running = False
    final=time.time()
    print("Time:"+(final-initial))

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
    homeStr="$"+str(getGRBL.get())+"="+str(valueGRBL.get())
    print(homeStr)
    data={}
    data["GCode"]=homeStr
    d=json.dumps(data)
    b=d.encode()
    s.sendall(b)
    
    #c=s.recv(1)
    #j=c.decode()
    #print(j)

def Spindle_Position(text): 
    global SpindleX, SpindleY
    x1=text.find("W")
    b=text[x1+5:]

    data=b.split(",")

    SpindleX=data[0]
    SpindleY=data[1]


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

def incrementEntry():
    value=int(changeamountGRBL.get())
    value=value+1
    changeamountGRBL.delete(0, 'end')
    changeamountGRBL.insert(0, value)

def decrementEntry():
    value=int(changeamountGRBL.get())
    value=value-1
    changeamountGRBL.delete(0, 'end')
    changeamountGRBL.insert(0, value)

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
    c='G'
    e=c.encode()
    s.sendall(e)
    homeStr="$$"
    data={}
    data["GCode"]=homeStr
    d=json.dumps(data)
    b=d.encode()
    s.sendall(b)
    
    c1=s.recv(1024)
    L1=c1.decode()
    print("--------------------")
    L=(re.split('\n', L1))
    print("String From Arduino")
    #print("L1", L1)
    GRBL_code=[]
    GRBL_value=[]
    counter=0
    for x in L:
        print(counter, x)
        if(x.startswith('$')):
            x1=x.find(" ")
            #b=x[0:x1]
            #print(b)
            head, sep, tail=x.partition('=')
            GRBL_code.append(head)
            GRBL_value.append(tail)
            counter=counter+1
    x=0
    #print("Now Breaking")
    #print(GRBL_code, GRBL_value)
    #print("Fetching")
    x=GRBL_code.index("$100")
    print("Index=", x)
    print("----------------------")
    y=GRBL_value[x]
    #print("100=", y)
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
	
main=Tk()
main.title("CNC Control Box")
main.geometry('{}x{}'.format(500, 300))
noteb = ttk.Notebook(main)
noteb.grid(row=1, column=0, columnspan='50', rowspan='49')
window=ttk.Frame(noteb)
noteb.add(window, text='Home')
window2=ttk.Frame(noteb)
noteb.add(window2, text='Settings')
#main.configure(background="yellow")

############### Frames ##################

frame0=Frame(window)
#frame0.grid(row=0, column=0, padx=(60,140))
frame0.grid(row=0, column=0, sticky='N')

frame1=Frame(window)
#frame1.grid(row=1, column=0, padx=(0,125))
frame1.grid(row=1, column=0, sticky='N')

#frame2=Frame(window)
#frame2.grid(row=2, column=0, padx=(25,165), pady=5, sticky='w')

frame3=Frame(window)
#frame3.grid(row=2, column=0, padx=(0,110))
frame3.grid(row=2, column=0, sticky='N')

frame4=Frame(window)
#frame4.grid(row=3, column=0, padx=(0, 55))
frame4.grid(row=3, column=0)

frame5=Frame(window)
#frame5.grid(row=4, column=0, padx=(20,90), pady=(20,0))
frame5.grid(row=4, column=0)

frame6=Frame(window2)
frame6.grid(row=0, column=0, sticky='W')

frame7=Frame(window2)
frame7.grid(row=1, column=0, sticky='W', pady=20)

frame8=Frame(window2)
frame8.grid(row=2, column=0)

############### Labels ##################

currentX=Label(frame1, height='1', width='20')
currentX.grid(row=2, column=0)

zlabel=Label(frame3, text="Z", height='2', width='2')
#zlabel.grid(row=0, column=0, sticky=W+E+N+S, padx=70)
#zlabel.grid(row=0, column=0, padx=(60,80))
zlabel.grid(row=0, column=0)

ylabel=Label(frame3, text="Y")
#ylabel.grid(row=0, column=4)
ylabel.grid(row=0, column=3)

xlabel=Label(frame3, text="X", height='2', width='2')
xlabel.grid(row=2, column=1)
#xlabel.pack(padx=20, side=LEFT)

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

#CommandLine=Text(frame6, height=1, width=20)
#CommandLine.grid(row=9, column=0)

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

ipaddress = Label(frame1, height=2, width=25)
ipaddress.grid(row=0, column=0, sticky="e")

newfilename = Label(frame1, height=2, width=20)
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

homebutton= Button(frame3, text="O", height='2', width='2', command=home)
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

def sel():
   #selection = "Move " + str(movevar.get())
   #label.config(text = selection)
    global valuex, valuey

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

pausebutton=Button(frame4, text="||", height='2', width='3')
pausebutton.grid(row=0, column=2, padx=(0,10))

stopbutton=Button(frame4, text="[]", height='2', width='3', command=Stop)
stopbutton.grid(row=0, column=3)

############## CANVAS BEDSHEET ##################

w = Canvas(window, width=205, height=410)
w.grid(row=0, column=4, rowspan=5)

bedarea=w.create_rectangle(2, 2, rectangle_width+2, rectangle_height+2)
spindle=w.create_oval(valuex-1, valuey-1, valuex+1, valuey+1, fill="green")
w.tag_raise(spindle)

#scale1=int(var.get())
#scale1=changescale(val)
#print("h",scale1)
#checkered(w, 5)

#print(xmax, xmin, ymax, ymin)

############### Debugger Box ####################

debugSec=Text(window, width=25, height=25, fg="red")
debugSec.insert(1.0, "Debugger>>\n")
debugSec.grid(row=0, column=5, rowspan=5, sticky='N')

SettingSec=Text(frame6, width=45, height=12, fg="red")
SettingSec.insert(1.0, "Debugger>>\n")
SettingSec.grid(row=0, column=5, rowspan=30, padx=(10,0), pady=(1,0), sticky='N')

main.mainloop()
