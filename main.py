from pyautogui import position
from PIL import Image, ImageDraw
import tkinter as tk

inw = input("Enter file name: ")

root = tk.Tk()

scrx = root.winfo_screenwidth()
scry = root.winfo_screenheight()
img=Image.new("RGBA", (scrx, scry), (255,255,255))
drawable=ImageDraw.Draw(img)
try:
    while True:
        for i1 in range(255):
            for i2 in range(255):
                for i3 in range(255):
                    xy=position()
                    x1=xy[0]+1
                    x2=xy[0]-1
                    y1=xy[1]+1
                    y2=xy[1]-1
                    drawable.rectangle([(x1, y1), (x2, y2)], (i1, i2, i3), (i1, i2, i3), 5)
except KeyboardInterrupt:
    img.save(f"{inw}.png")