from tkinter import *
from tkinter import filedialog
counter=0

############# Functions #################

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
	
def UploadAction(event=None):                             # Import File is getting selected and needs to be saved on RaspberryPi
    filename = filedialog.askopenfilename()
    print('Selected:', filename)
	
'''	
def decrement():
    entrybox.delete(0, END)
    entrybox.insert(0, int(entrybox.get() - 1)
'''
########## CNC Control Window ###########
	
window=Tk()
window.title("Control Box")
window.geometry('{}x{}'.format(500, 300))

############### Frames ##################

frame1=Frame(window)
frame1.pack(side=TOP)

frame2=Frame(window)
frame2.pack(side = TOP)

frame3=Frame(window)
frame3.pack(side=TOP)

frame4=Frame(window)
frame4.pack(side=TOP)

frame5=Frame(window)
frame5.pack(side=TOP)

############### Labels ##################

zlabel=Label(frame1, text="Z", height='5', width='5')
#zlabel.grid(row=0, column=0, sticky=W+E+N+S, padx=70)
zlabel.pack(padx=(0,5) , side=LEFT)

ylabel=Label(frame1, text="Y")
#ylabel.grid(row=0, column=4)
ylabel.pack(padx=(65,90), side=LEFT)

xlabel=Label(frame3, text="X", height='2', width='2')
xlabel.grid(row=3, column=2, padx=(55,5))
#xlabel.pack(padx=20, side=LEFT)

############### Manual Control Panel ##################

zpbutton=Button(frame2, text="+", height='2', width='2')
zpbutton.grid(row=2, column=0, padx=(20,10))
#zpbutton.pack(padx=100, side=LEFT)

xnypbutton= Button(frame2, height='2', width='2')
xnypbutton.grid(row=2, column=3, padx=(40,0))
#xnypbutton.pack(padx=0, side=LEFT)

ypbutton= Button(frame2, text="+", height='2', width='2')
ypbutton.grid(row=2, column=4)
#ypbutton.pack(padx=0, side=LEFT)

xpypbutton= Button(frame2, height='2', width='2')
xpypbutton.grid(row=2, column=5)
#xpypbutton.pack(padx=0, side=LEFT)

mulbutton= Button(frame2, text="x10", height='1', width='2', command=multiplyTen)
mulbutton.grid(row=2, column=7, padx=(20,0))
#mulbutton.pack(padx=20, side=LEFT)

addbutton= Button(frame2, text="+", height='1', width='2', command=increment)
addbutton.grid(row=2, column=8, padx=(10,0))
#addbutton.pack(padx=20, side=LEFT)

xnbutton= Button(frame3, text="-", height='2', width='2')
xnbutton.grid(row=3, column=3, padx=(12,0))
#xnbutton.pack(padx=0, side=LEFT)

homebutton= Button(frame3, text="O", height='2', width='2')
homebutton.grid(row=3, column=4)
#xoyobutton.pack(padx=0, side=LEFT)

xpbutton= Button(frame3, text="+", height='2', width='2')
xpbutton.grid(row=3, column=5, padx=(0,25))
#xpbutton.pack(padx=0, side=LEFT)

v=StringVar(window, value="20")
entrybox=Entry(frame3, width='7', textvariable=v)
entrybox.grid(row=3, column=8, columnspan=2, padx=(0,5))
#spinbox.pack(padx=20, side=LEFT)

znbutton=Button(frame4, text="-", height='2', width='2')
znbutton.grid(row=4, column=1, padx=(20,20))
#znbutton.pack()

xnynbutton= Button(frame4, height='2', width='2')
xnynbutton.grid(row=4, column=3, padx=(30,0))
#xnynbutton.pack()

ynbutton= Button(frame4, text="-", height='2', width='2')
ynbutton.grid(row=4, column=4)
#ynbutton.pack()

xpynbutton= Button(frame4, height='2', width='2')
xpynbutton.grid(row=4, column=5)
#xpynbutton.pack()

divbutton= Button(frame4, text="/10", height='1', width='2', command=divideTen)
divbutton.grid(row=4, column=7, padx=(20,0))
#divbutton.pack()

subbutton= Button(frame4, text="-", height='1', width='2', command=decrement)
subbutton.grid(row=4, column=8, padx=(10,0))
#subbutton.pack()


############## FILE CONTROL PANEL ################

importbutton=Button(frame5, text="U", height='2', width='4', command=UploadAction)
importbutton.grid(row=5, column=1, pady="40", padx=(20,10))

playbutton=Button(frame5, text="|>", height='2', width='4')
playbutton.grid(row=5, column=2, pady="40", padx="10")

pausebutton=Button(frame5, text="||", height='2', width='4')
pausebutton.grid(row=5, column=3, pady="40", padx="10")

stopbutton=Button(frame5, text="[]", height='2', width='4')
stopbutton.grid(row=5, column=4, pady="40", padx="10")

window.mainloop()