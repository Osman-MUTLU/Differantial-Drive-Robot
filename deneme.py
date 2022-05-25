import math
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import PIL
import serial
import time

start_angle = 0
start_coordinates = [50,50]

arduino = serial.Serial(port='COM4', baudrate=9600, timeout=.1)

def write_data(x):
    arduino.write(bytes(x, 'utf-8'))
    
def read_data():
    data = arduino.readline()
    return data

def left(canvas,img):
    put_robot(canvas,img,start_coordinates,5)
def right(canvas,img):
    put_robot(canvas,img,start_coordinates,-5)
def up(canvas,img):
    r = 10
    y = -math.sin(start_angle*0.017453292519943295)*r
    x = math.cos(start_angle*0.017453292519943295)*r
    print("dx={} , dy = {}".format(x,y))
    canvas.create_line(start_coordinates[0],start_coordinates[1],(start_coordinates[0]+x),start_coordinates[1]+y)
    start_coordinates[0]+=x
    start_coordinates[1]+=y
    print("x={} , y = {}".format(start_coordinates[0],start_coordinates[1]))
    put_robot(canvas,img,start_coordinates,0)
    
def put_robot(canvas,img,coordinates,rotation_angle):
    global start_angle
    print(start_angle)
    start_angle += rotation_angle
    if start_angle>180 : start_angle -=360
    elif start_angle<-180 : start_angle +=360
    canvas.delete("image")
    img = img.rotate(start_angle, PIL.Image.NEAREST, expand = 1)
    image = ImageTk.PhotoImage(img)
    canvas.images += [image]
    canvas.create_image(
            coordinates,
            image=image,
            tag="image"
        )
def main():
    img = Image.open("image.png")
    root = tk.Tk()
    root.geometry("1250x700")
    w= 1250
    h= 700
    canvas = tk.Canvas(master=root, width=w, height=h)
    canvas.pack()
    canvas.images = []
    img = img.rotate(-90, PIL.Image.NEAREST, expand = 1)
    image = ImageTk.PhotoImage(img)
    canvas.images.append([image])
    canvas.create_image(
            (50,50),
            image=image,
            tag="image"
        )
    root.bind_all("<KeyPress-Left>",lambda event:left(canvas,img))
    root.bind_all("<KeyPress-Right>",lambda event:right(canvas,img))
    root.bind_all("<KeyPress-Up>",lambda event:up(canvas,img))
    root.mainloop()
   
if __name__ == '__main__':
    main()    