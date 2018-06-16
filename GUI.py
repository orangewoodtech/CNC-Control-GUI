#Tested Move GCode and Move CNC

from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import threading
from threading import Thread
import math, os, shutil, time
from numpy import *
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

folder="/home/pi/Desktop/Orangewood_gerber"

s = socket(AF_INET, SOCK_STREAM)
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
    clean()
    Connectbutton.configure(bg = "red")
    global s
    host = "192.168.43.147"
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
    #ipaddress.config(text="IP Address: "+ "192.168.121.0")
    os.system('./shell.sh')
    #print("Server Executed ")
    SelectedfileFlag=1
    rem()
    #print("Ab Play Chalega")
    
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
        c='G'
        e=c.encode()
        #print("wtf1")
        s.sendall(e)
        homeStr="G90G0X"+str(valuex)+"\nG90\n"
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
	
def xneg():
    value = entrybox.get()
    astring="Moving in X- \nG00 X-"
    debugSec.insert(INSERT, astring + value + "\n")
    global valuex, valuey, valuez, s
    valuex=valuex-int(value)
    selection = "X = " + str(valuex) + " Y = " + str(valuey) + " Z = " + str(valuez)
    currentX.config(text = selection)
    if(int(movevar.get())==1):
        c='G'
        e=c.encode()
        #print("wtf1")
        s.sendall(e)
        homeStr="G90G0X"+str(valuex)+"\nG90\n"
        data={}
        data["GCode"]=homeStr
        d=json.dumps(data)
        b=d.encode()
        s.sendall(b)
    
        c=s.recv(1)
        j=c.decode()

def ypos():
    value = entrybox.get()
    astring="Moving in Y \nG00 Y"
    debugSec.insert(INSERT, astring + value + "\n")
    global valuex, valuey, valuez, s
    valuey=valuey+int(value)
    selection = "X = " + str(valuex) + " Y = " + str(valuey) + " Z = " + str(valuez)
    currentX.config(text = selection)
    if(int(movevar.get())==1):
        c='G'
        e=c.encode()
        s.sendall(e)
        homeStr="G90G0Y"+str(valuey)+"\nG90\n"
        data={}
        data["GCode"]=homeStr
        d=json.dumps(data)
        b=d.encode()
        s.sendall(b)
    
        c=s.recv(1)
        j=c.decode()
	
def yneg():
    value = entrybox.get()
    astring="Moving in Y- \nG00 Y-"
    debugSec.insert(INSERT, astring + value + "\n")
    global valuex, valuey, valuez, s
    valuey=valuey-int(value)
    selection = "X = " + str(valuex) + " Y = " + str(valuey) + " Z = " + str(valuez)
    currentX.config(text = selection)
    if(int(movevar.get())==1):
        c='G'
        e=c.encode()
        s.sendall(e)
        homeStr="G90G0Y"+str(valuey)+"\nG90\n"
        data={}
        data["GCode"]=homeStr
        d=json.dumps(data)
        b=d.encode()
        s.sendall(b)
    
        c=s.recv(1)
        j=c.decode()

def zpos():
    value = entrybox.get()
    astring="Moving in Z \nG00 Z"
    debugSec.insert(INSERT, astring + value + "\n")
    global valuex, valuey, valuez, s
    valuez=valuez+int(value)
    selection = "X = " + str(valuex) + " Y = " + str(valuey) + " Z = " + str(valuez)
    currentX.config(text = selection)
    if(int(movevar.get())==1):
        c='G'
        e=c.encode()
        s.sendall(e)
        homeStr="G90G0Z"+str(valuez)+"\nG90\n"
        data={}
        data["GCode"]=homeStr
        d=json.dumps(data)
        b=d.encode()
        s.sendall(b)
    
        c=s.recv(1)
        j=c.decode()
	
def zneg():
    value = entrybox.get()
    astring="Moving in Z- \nG00 Z-"
    debugSec.insert(INSERT, astring + value + "\n")
    global valuex, valuey, valuez, s
    valuez=valuez-int(value)
    selection = "X = " + str(valuex) + " Y = " + str(valuey) + " Z = " + str(valuez)
    currentX.config(text = selection)
    if(int(movevar.get())==1):
        c='G'
        e=c.encode()
        s.sendall(e)
        homeStr="G90G0Z"+str(valuez)+"\nG90\n"
        data={}
        data["GCode"]=homeStr
        d=json.dumps(data)
        b=d.encode()
        s.sendall(b)
    
        c=s.recv(1)
        j=c.decode()
	
def home():
    print("Moving to Home")
    global valuex, valuey, s
    if(int(movevar.get())==1):
        c='G'
        e=c.encode()
        s.sendall(e)
        homeStr="G90G0X"+str(valuex)+"Y"+str(valuey)+"\nG90\n"
        data={}
        data["GCode"]=homeStr
        d=json.dumps(data)
        b=d.encode()
        s.sendall(b)
    
        c=s.recv(1)
        j=c.decode()

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
        c='G'
        e=c.encode()
        s.sendall(e)
        homeStr="G90G0X"+str(valuex)+"Y"+str(valuey)+"\nG90\n"
        data={}
        data["GCode"]=homeStr
        d=json.dumps(data)
        b=d.encode()
        s.sendall(b)
    
        c=s.recv(1)
        j=c.decode()
	
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
        c='G'
        e=c.encode()
        s.sendall(e)
        homeStr="G90G0X"+str(valuex)+"Y"+str(valuey)+"\nG90\n"
        data={}
        data["GCode"]=homeStr
        d=json.dumps(data)
        b=d.encode()
        s.sendall(b)
    
        c=s.recv(1)
        j=c.decode()
	
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
        c='G'
        e=c.encode()
        s.sendall(e)
        homeStr="G90G0X"+str(valuex)+"Y"+str(valuey)+"\nG90\n"
        data={}
        data["GCode"]=homeStr
        d=json.dumps(data)
        b=d.encode()
        s.sendall(b)
    
        c=s.recv(1)
        j=c.decode()
	
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
        c='G'
        e=c.encode()
        s.sendall(e)
        homeStr="G90G0X"+str(valuex)+"Y"+str(valuey)+"\nG90\n"
        data={}
        data["GCode"]=homeStr
        d=json.dumps(data)
        b=d.encode()
        s.sendall(b)
    
        c=s.recv(1)
        j=c.decode()

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
    filename = filedialog.askopenfilename()
    SelectedfileFlag=1
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

def move():
    global xmax, xmin, ymax, ymin
    if(int(movevar.get())==2):
        t2=threading.Timer(1.0, plot)
        t2.start()
    #elif(int(movevar.get())==1):

def plot():
    print("Plot Hua")
    global valuex, valuey,flag1, prevx,prevy, xmax, xmin,ymax,ymin
    t=threading.Timer(1.0, move)
    t.start()
    #clear()
    print(xmax, xmin, ymax, ymin, valuex, valuey)
    a=(valuex/6.0)+2
    b=408.4-(valuey/6.0)
    c=float((xmax-xmin+valuex)/6.0+2)
    d=float(408.4-(ymax-ymin+valuey)/6.0)
    print(a, b, c, d)

    if(valuex!=prevx or valuey!=prevy):
        flag1=0

    if(a>=2 and b<=408.4 and c<=rectangle_width+2 and d>=2):
        clear()
        print("Bounding Box Banega CNC Bed pe")
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
    #t.cancel()

switch=True
def PlayFile(): 
    def runn():
        global running
        global s
        global folder
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
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
    global running
    running = False

# Input Parameters:
# (x1, y1) first point on arc
# (x2, y2) second point on arc
# (xc, yc) center point of circle
# direction : 1 ( clockwise ) , 0 ( anticlockwise )
	  
########## CNC Control Window ###########
	
window=Tk()
window.title("CNC Control Box")
window.geometry('{}x{}'.format(500, 300))
#window.configure(background="yellow")

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

frame6=Frame(window)
frame6.grid(row=5, column=0)

frame7=Frame(window)
frame7.grid(row=6, column=0)

frame8=Frame(window)
frame8.grid(row=8, column=0)

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

#scalelabel=Label(frame6, text="SCALE:", height='2', width='8')
#scalelabel.grid(row=5, column=0)

############### Manual Control Panel ##################

Connectbutton=Button(frame0, text="Connect", height='2', width='8', command = colorChange)
Connectbutton.grid(row=0, column=0, padx=(0, 2))

SetHomebutton=Button(frame0, text="Set Home", height='2', width='8', command=sethome)
SetHomebutton.grid(row=0, column=3, padx=(0, 2))

clearbutton=Button(frame0, text="Clear", height='2', width='8', command = clear)
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

#importbutton=Button(frame4, text="U", height='2', width='4', command=UploadAction)
#importbutton.grid(row=0, column=0, )

playbutton=Button(frame4, text="|>", height='2', width='4', command=Play)
playbutton.grid(row=0, column=0, padx=(0,10))

pausebutton=Button(frame4, text="||", height='2', width='4')
pausebutton.grid(row=0, column=1, padx=(0,10))

stopbutton=Button(frame4, text="[]", height='2', width='4', command=Stop)
stopbutton.grid(row=0, column=2)

############## CANVAS BEDSHEET ##################

w = Canvas(window, width=205, height=410)
w.grid(row=0, column=4, rowspan=5)

bedarea=w.create_rectangle(2, 2, rectangle_width+2, rectangle_height+2)

#scale1=int(var.get())
#scale1=changescale(val)
#print("h",scale1)
#checkered(w, 5)

#print(xmax, xmin, ymax, ymin)

############### Debugger Box ####################

debugSec=Text(window, width=25, height=25, fg="red")
debugSec.insert(1.0, "Debugger>>\n")
debugSec.grid(row=0, column=5, rowspan=5, sticky='N')

window.mainloop()
