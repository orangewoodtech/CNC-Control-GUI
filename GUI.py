from tkinter import *
from tkinter import filedialog
from tkinter import ttk
global value
global i
########### Functions #################

def colorChange():
    """Changes the button's color"""
    Connectbutton.configure(bg = "red")

def xpos():

    #print("Moving in X+")
    value = entrybox.get()
    #print("G00 X" + value)
    
    #debugSec.delete('1.0', END)
    astring="Moving in X+ \nGOO X"
    debugSec.insert(INSERT, astring + value + "\n")
	
def xneg():
    print("Moving in X-")
    value = entrybox.get()
    print("G00 X-" + value)

def ypos():
    print("Moving in Y+")
    value = entrybox.get()
    print("G00 Y" + value)
def yneg():
    print("Moving in Y-")
    value = entrybox.get()
    print("G00 Y-" + value)

def zpos():
    print("Moving in Z+")
    value = entrybox.get()
    print("G00 Z" + value)
def zneg():
    print("Moving in Z-")
    value = entrybox.get()
    print("G00 Z-" + value)

def home():
    print("Moving to Home")

def diag1():
    print("Moving diagonally 1")
    value = entrybox.get()
    print("G00 X-"+value+" Y"+value)
def diag2():
    print("Moving diagonally 2")
    value = entrybox.get()
    print("G00 X"+value+" Y"+value)
def diag3():
    print("Moving diagonally 3")
    value = entrybox.get()
    print("G00 X-"+value+" Y-"+value)
def diag4():
    print("Moving diagonally 4")
    value = entrybox.get()
    print("G00 X"+value+" Y-"+value)

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
def UploadAction(event=None):                             # Import File is getting selected and needs to be saved on RaspberryPi
    filename = filedialog.askopenfilename()
    print('Selected:', filename)
	
xmin, xmax, ymin, ymax, valx, valy= 99999.0,0.0,99999.0,0.0,0.0,0.0
x=''
y=''
with open('GCode2.txt','r') as f:
 for line in f.readlines():
  for word in line.split():
   if(word[0] == "X"):
    x=word[1:]
    valx=float(x)
    if(valx>xmax):
     xmax=valx
    if(valx<xmin):
     xmin=valx

    #print(x)
   if(word[0] == "Y"):
    y=word[1:]
    valy=float(y)
    if(valy>ymax):
     ymax=valy
    if(valy<ymin):
     ymin=valy
    #print(y)
print(xmax)
print(xmin)
print(ymax)
print(ymin)

def checkered(canvas, line_distance):
   # vertical lines at an interval of "line_distance" pixel
   for x in range(line_distance,rectangle_width,line_distance):
      w.create_line(x+25, 25, x+25, rectangle_height+25, fill="#476042")
   # horizontal lines at an interval of "line_distance" pixel
   for y in range(line_distance,rectangle_height,line_distance):
      w.create_line(25, y+25, rectangle_width+25, y+25, fill="#476042")
	  
########## CNC Control Window ###########
	
window=Tk()
window.title("CNC Control Box")
window.geometry('{}x{}'.format(500, 300))

############### Frames ##################

frame0=Frame(window)
frame0.grid(row=0, column=0, pady=(25,0))

frame1=Frame(window)
frame1.grid(row=1, column =0, pady=(25,0))

frame2=Frame(window)
frame2.grid(row=2, column=0)

frame3=Frame(window)
frame3.grid(row=3, column=0)

frame4=Frame(window)
frame4.grid(row=4, column=0)

frame5=Frame(window)
frame5.grid(row=6, column=0, pady=20)

frame6=Frame(window)
frame6.grid(row=5, column=0, pady=10)

############### Labels ##################

zlabel=Label(frame1, text="Z", height='2', width='2')
#zlabel.grid(row=0, column=0, sticky=W+E+N+S, padx=70)
zlabel.pack(padx=(0,5) , side=LEFT)

ylabel=Label(frame1, text="Y")
#ylabel.grid(row=0, column=4)
ylabel.pack(padx=(65,90), side=LEFT)

xlabel=Label(frame3, text="X", height='2', width='2')
xlabel.grid(row=3, column=2, padx=(55,5))
#xlabel.pack(padx=20, side=LEFT)

scalelabel=Label(frame6, text="SCALE:", height='2', width='8')
scalelabel.grid(row=5, column=0)

############### Manual Control Panel ##################

Connectbutton=Button(frame0, text="Connect", height='2', width='8', command = colorChange)
Connectbutton.grid(row=0, column=0, padx=10)

SetHomebutton=Button(frame0, text="Set Home", height='2', width='8')
SetHomebutton.grid(row=0, column=1)

zpbutton=Button(frame2, text="+", height='2', width='2', command=zpos)
#balloon = tix.Balloon(window)
#balloon.bind_widget(zpbutton, balloonmsg="Click for moving in +ve Z axis")
zpbutton.grid(row=2, column=0, padx=(20,10))
#zpbutton.pack(padx=100, side=LEFT)

xnypbutton= Button(frame2, height='2', width='2', command= diag1)
xnypbutton.grid(row=2, column=3, padx=(40,0))
#xnypbutton.pack(padx=0, side=LEFT)

ypbutton= Button(frame2, text="+", height='2', width='2', command=ypos)
ypbutton.grid(row=2, column=4)
#ypbutton.pack(padx=0, side=LEFT)

xpypbutton= Button(frame2, height='2', width='2', command=diag2)
xpypbutton.grid(row=2, column=5)
#xpypbutton.pack(padx=0, side=LEFT)

mulbutton= Button(frame2, text="x10", height='1', width='2', command=multiplyTen)
mulbutton.grid(row=2, column=7, padx=(20,0))
#mulbutton.pack(padx=20, side=LEFT)

addbutton= Button(frame2, text="+", height='1', width='2', command=increment)
addbutton.grid(row=2, column=8, padx=(10,0))
#addbutton.pack(padx=20, side=LEFT)

xnbutton= Button(frame3, text="-", height='2', width='2', command=xneg)
xnbutton.grid(row=3, column=3, padx=(12,0))
#xnbutton.pack(padx=0, side=LEFT)

homebutton= Button(frame3, text="O", height='2', width='2', command=home)
homebutton.grid(row=3, column=4)
#xoyobutton.pack(padx=0, side=LEFT)

xpbutton= Button(frame3, text="+", height='2', width='2', command=xpos)
xpbutton.grid(row=3, column=5, padx=(0,25))
#xpbutton.pack(padx=0, side=LEFT)

v=StringVar(window, value="20")
entrybox=Entry(frame3, width='7', textvariable=v)
entrybox.grid(row=3, column=8, columnspan=2, padx=(0,5))
#spinbox.pack(padx=20, side=LEFT)

znbutton=Button(frame4, text="-", height='2', width='2', command=zneg)
znbutton.grid(row=4, column=1, padx=(20,20))
#znbutton.pack()

xnynbutton= Button(frame4, height='2', width='2', command=diag3)
xnynbutton.grid(row=4, column=3, padx=(30,0))
#xnynbutton.pack()

ynbutton= Button(frame4, text="-", height='2', width='2', command=yneg)
ynbutton.grid(row=4, column=4)
#ynbutton.pack()

xpynbutton= Button(frame4, height='2', width='2', command=diag4)
xpynbutton.grid(row=4, column=5)
#xpynbutton.pack()

divbutton= Button(frame4, text="/10", height='1', width='2', command=divideTen)
divbutton.grid(row=4, column=7, padx=(20,0))
#divbutton.pack()

subbutton= Button(frame4, text="-", height='1', width='2', command=decrement)
subbutton.grid(row=4, column=8, padx=(10,0))
#subbutton.pack()

scale=StringVar(window, value="20")
scaleBox=Entry(frame6, width='7', textvariable=scale)
scaleBox.grid(row=5, column=1, columnspan=2, padx=(0,5))

############## FILE CONTROL PANEL ################

importbutton=Button(frame5, text="U", height='2', width='4', command=UploadAction)
importbutton.grid(row=5, column=1, pady="40", padx=(20,10))

playbutton=Button(frame5, text="|>", height='2', width='4')
playbutton.grid(row=5, column=2, pady="40", padx="10")

pausebutton=Button(frame5, text="||", height='2', width='4')
pausebutton.grid(row=5, column=3, pady="40", padx="10")

stopbutton=Button(frame5, text="[]", height='2', width='4')
stopbutton.grid(row=5, column=4, pady="40", padx="10")

############## CANVAS BEDSHEET ##################

rectangle_width = 400
rectangle_height = 500

w = Canvas(window, width=450, height=540)
w.grid(row=1, column=100, rowspan=6)

bedarea=w.create_rectangle(25, 25, rectangle_width+25, rectangle_height+25)

#value1=int(scaleBox.get())

checkered(w,20)

boundingbox=w.create_rectangle(25, 25, xmax-xmin+25, ymax-ymin+25, fill = 'red')
w.tag_raise(boundingbox)

############### Debugger Box ####################

debugSec=Text(window, width=80, height=31, fg="red")
debugSec.insert(1.0, "Debugger>>\n")
debugSec.grid(row=1, column=200, rowspan=8)



window.mainloop()
