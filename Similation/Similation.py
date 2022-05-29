import math
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import PIL
import serial
import time

start_angle = 0

# It is the starting coordinate of the robot.
start_coordinates = [600, 300]
# "COM5" is the communication port between the robot and the computer.
arduino = serial.Serial(port='COM5', baudrate=9600, timeout=.1)


img = Image.open("robot_image.png")
root = tk.Tk()
root.geometry("1250x700")
w = 1250
h = 700
canvas = tk.Canvas(master=root, width=w, height=h)
canvas.pack()
canvas.images = []
data = {}
frame_rate = 100
radius = 0.2 # radius of wheel is 20 cm
motion =""

# Calculates the instantaneous linear velocity of the robot.
def get_v():
    global motion
    if motion == "F" or motion == "B":
        v0 = (radius*2.0*math.pi*float(data["L"]))/60.0
        v1 = (radius*2.0*math.pi*float(data["R"]))/60.0
        return (v0+v1)/2
    else:
        return 0

# Calculates the new coordinate with instantaneous velocity and angle.
def get_new_coordinate():
    global canvas,img
    r = 700*get_v()
    
    y = -math.sin(start_angle*0.017453292519943295)*r
    x = math.cos(start_angle*0.017453292519943295)*r
    if motion == "B":
        x = -x
        y = -y
    
    canvas.create_line(start_coordinates[0], start_coordinates[1],
                       (start_coordinates[0]+x), start_coordinates[1]+y)
    start_coordinates[0] += x
    start_coordinates[1] += y
    canvas.after(frame_rate,get_new_coordinate)

# It sends data to the serial port of the Arduino.
def write_data(x):
    arduino.write(bytes(x, 'utf-8'))

# It organizes the data coming from the communication port and saves it in the data.
def read_data():
    global canvas,data
    value = arduino.readline()
    print(value)
    value = str(value).replace('b', '')
    value = value.replace("'", '')
    if value != "":
        value = value.strip()
        
        value = value.split()
        for temp in value:
            t = temp.split(":")
            data[t[0]] = t[1]
        
    canvas.after(10,read_data)

# Sets the instant position of the robot.
def set_position():
    global canvas,img
    put_robot(canvas, img, start_coordinates, data["Z"])
    canvas.after(frame_rate,set_position)

# The motion functions of the robot.
def front():
    global motion
    write_data("0")
    motion = "F"

def back():
    global motion
    write_data("1")
    motion = "B"
    
def left():
    global motion
    write_data("2")
    motion = "L"

def right():
    global motion
    write_data("3")
    motion = "R"
    
def stop():
    global motion
    write_data("4")
    motion = "S"

# It places the robot in that position according to the calculated coordinate and angle values.
def put_robot(canvas, img, coordinates, new_angle):
    global start_angle

    start_angle = int(new_angle)
    if start_angle > 180:
        start_angle -= 360
    elif start_angle < -180:
       start_angle += 360
    canvas.delete("image")
    img = img.rotate(start_angle, PIL.Image.NEAREST, expand=1)
    image = ImageTk.PhotoImage(img)
    canvas.images += [image]
    canvas.create_image(
        coordinates,
        image=image,
        tag="image"
    )


def main():
    global img,root,canvas
    img = img.rotate(-90, PIL.Image.NEAREST, expand=1)
    image = ImageTk.PhotoImage(img)
    canvas.images.append([image])
    canvas.create_image(
        (50, 50),
        image=image,
        tag="image"
    )
    time.sleep(5)
    read_data()
    get_new_coordinate()
    set_position()
    

    # It transfers the direction information received from the keyboard to the robot.
    root.bind_all("<KeyPress-Left>", lambda event: left())
    root.bind_all("<KeyRelease-Left>", lambda event: stop())

    root.bind_all("<KeyPress-Right>", lambda event: right())
    root.bind_all("<KeyRelease-Right>", lambda event: stop())

    root.bind_all("<KeyPress-Up>", lambda event: front())
    root.bind_all("<KeyRelease-Up>", lambda event: stop())

    root.bind_all("<KeyPress-Down>", lambda event: back())
    root.bind_all("<KeyRelease-Down>", lambda event: stop())
    root.mainloop()


if __name__ == '__main__':
    main()
