from tkinter import Tk, Label, Button, Entry
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askokcancel
from pyautogui import position, size
from PIL import Image, ImageDraw
from random import randint
from sys import path
import mouse

def gen_image():
    #Create base blank image that is as big as the screen.
    img=Image.new("RGBA", size(), (255,255,255))
    return ImageDraw.Draw(img), img

def addPoint(drawable:ImageDraw.ImageDraw, colour:tuple, size:int):
    #Add a point to an inputted image
    xy=position()
    x1=xy[0]+size
    x2=xy[0]-size
    y1=xy[1]+size
    y2=xy[1]-size
    drawable.rectangle([(x1, y1), (x2, y2)], colour, colour, 5)

def iter_rainbow(colour:list):
    #Create a (kinda) rainbow pattern
    for i in range(len(colour)):
        colour[i]=randint(0, 255)
    return colour

def sanitise(text:str):
    #Remove non-allowed text
    return "".join(char for char in text if not char in "\\/:*?<>|\".")


root = Tk()
root.title("Tracker")
stop=False
tracking=False
startTrack=False
endTrack=False
filename=""
colour=[0,0,0]
filelocation=path[0]

def end():
    #End the loop
    global stop
    if askokcancel("Quit?", "Are you sure you want to quit?"):
        root.destroy()
        stop=True

root.protocol("WM_DELETE_WINDOW", end)

def toggleTrack():
    #Turn on tracking if tracking is off, turn tracking off if tracking is on
    global startTrack, endTrack, tracking
    if tracking:
        endTrack=True
    else:
        startTrack=True

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

#Define root parts
filelabel=Label(root, text="Enter filename")
filelabel.grid(column=0, row=0)
filebox=Entry(root)
filebox.grid(column=0, row=1)
toggleTrackButton=Button(root, text="Start/Stop tracking session", command=toggleTrack)
toggleTrackButton.grid(column=1, row=1)
def setfile():
    global filelocation
    filelocation=askdirectory()
filelabel=Button(root, text="Chose file location", command=setfile)
filelabel.grid(column=1, row=0)

while not stop:
    root.update()
    
    if tracking:
        colour=iter_rainbow(colour)
        if down:
            width=5
        else:
            width=1
        addPoint(draw, tuple(colour), width)
    elif startTrack:
        filename=sanitise(filebox.get())
        if not filename=="":
            tracking=True
            draw, image = gen_image()
        startTrack=False
    if endTrack:
        tracking=False
        image.save(f"{filelocation}\\{filename}.png")
        endTrack=False