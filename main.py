from tkinter import Tk, Label, Button, Entry, Toplevel
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askokcancel
from PIL import Image, ImageDraw, ImageTk
from pyautogui import position, size, sleep
from keyboard import is_pressed
from random import randint
from sys import path
import mouse
import yaml

#Load config
defaultconfig={
    'toggle window': {
        'location': 'TOP-LEFT',
        'size': [50, 50],
        'enabled': False
    },
    'main window': {
        'foreground':[0, 0, 0],
        'background':[255, 255, 255],
        'default location':"LOCAL"
    }}

try:
    with open("config.yml", "r") as f:
        conf=yaml.safe_load(f)
except:
    with open("config.yml", "w") as f:
        yaml.dump(defaultconfig, f)
        conf=defaultconfig

root = Tk()
root.title("Tracker")
bg="#"
for part in conf["main window"]["background"]:
    val=hex(part).split("x")[-1]
    if len(val)==2:
        bg+=val
    else:
        bg+="0"
        bg+=val
fg="#"
for part in conf["main window"]["foreground"]:
    val=hex(part).split("x")[-1]
    if len(val)==2:
        fg+=val
    else:
        fg+="0"
        fg+=val
root.configure(bg=bg)
stop=False
tracking=False
startTrack=False
endTrack=False
filename=""
colour=[0,0,0]
if conf["main window"]["default location"]=="LOCAL":
    filelocation=path[0]
else:
    filelocation=conf["main window"]["default location"]
    
#Create base blank image that is as big as the screen
def gen_image():
    img=Image.new("RGBA", size(), (255,255,255))
    return ImageDraw.Draw(img), img

#Add a point to an inputted image
def addPoint(drawable:ImageDraw.ImageDraw, colour:tuple, size:int):
    xy=position()
    x1=xy[0]+size
    x2=xy[0]-size
    y1=xy[1]+size
    y2=xy[1]-size
    drawable.rectangle([(x1, y1), (x2, y2)], colour, colour, 5)

#Create a (kinda) rainbow pattern
def iter_rainbow(colour:list):
    for i in range(len(colour)):
        colour[i]=randint(0, 255)
    return colour

#Remove non-allowed text
def sanitise(text:str):
    return "".join(char for char in text if not char in "\\/:*?<>|\".")

#Quit the session
def end():
    global stop
    if askokcancel("Quit?", "Are you sure you want to quit?"):
        root.destroy()
        stop=True

root.protocol("WM_DELETE_WINDOW", end)

#Turn on tracking if tracking is off, turn tracking off if tracking is on
def toggleTrack():
    global startTrack, endTrack, tracking
    if tracking:
        endTrack=True
    else:
        startTrack=True

enabled=conf["toggle window"]["enabled"]
if enabled:
    #Create window in top right to display on/off and allow easy toggling
    toggle=Toplevel(root)
    toggle.overrideredirect(True)
    x,y=conf["toggle window"]["size"]
    loclist=conf["toggle window"]["location"].split("-")
    if loclist[0]=="TOP":
        yloc="+"
    else:
        yloc="-"
    if loclist[1]=="LEFT":
        xloc="+"
    else:
        xloc="-"
    toggle.geometry(f"{x}x{y}{xloc}0{yloc}0")
    toggle.wm_attributes("-topmost", True)
    onImage=ImageTk.PhotoImage(Image.new("RGB", (50,50), (0,255,0)), master=toggle)
    on=Button(toggle, image=onImage, command=toggleTrack)
    offImage=ImageTk.PhotoImage(Image.new("RGB", (50,50), (255,0,0)), master=toggle)
    off=Button(toggle, image=offImage, command=toggleTrack)
    off.grid(column=0,row=0)

#Check for mouse clicks
def on_down():
    global down
    down=True

def on_up():
    global down
    down=False

mouse.on_button(on_down, buttons=(mouse.LEFT), types=(mouse.DOWN))
mouse.on_button(on_up, buttons=(mouse.LEFT), types=(mouse.UP))

down=False

#Define GUI parts
filelabel=Label(root, text="Enter filename", background=bg, foreground=fg)
filelabel.grid(column=0, row=0)
filebox=Entry(root, background=bg, foreground=fg)
filebox.grid(column=0, row=1)
toggleTrackButton=Button(root, text="Start/Stop tracking session", command=toggleTrack, background=bg, foreground=fg)
toggleTrackButton.grid(column=1, row=1)
def setfile():
    global filelocation
    filelocation=askdirectory()
filelabel=Button(root, text="Chose file location", command=setfile, background=bg, foreground=fg)
filelabel.grid(column=1, row=0)

#Loop until stop is True
while not stop:
    root.update()
    if not stop:
        if enabled:
            toggle.update()

        if tracking:
            colour=iter_rainbow(colour)
            if down:
                width=5
            else:
                width=1
            addPoint(draw, tuple(colour), width)
            if enabled:
                off.grid_forget()
                on.grid(column=0, row=0)
        else:
            if not stop and enabled:
                on.grid_forget()
                off.grid(column=0, row=0)
        if startTrack:
            filename=sanitise(filebox.get())
            if not filename=="":
                try:
                    open(f"{filename}.png").close()
                    i=0
                    while True:
                        i+=1
                        try:
                            open(f"{filename}{i}.png").close()
                        except:
                            filename=f"{filename}{i}"
                            break
                except FileNotFoundError:
                    filename=filename
                tracking=True
                draw, image = gen_image()
            startTrack=False
        if endTrack:
            tracking=False
            image.save(f"{filelocation}\\{filename}.png")
            endTrack=False
        if is_pressed("f1"):
            toggleTrack()
            sleep(5)