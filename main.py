# Importing Image module from PIL package
import tkinter
from tkinter import *
from PIL import Image, ImageTk
import PIL

# creating a image object (main image)
im1 = Image.open(r"image.png")

# rotating a image 90 deg counter clockwise
im1 = im1.rotate(0, PIL.Image.NEAREST, expand = 1)

# Create an instance of tkinter frame
root = Tk()

# Set the geometry of tkinter frame
root.geometry("1250x700")
w= 1250
h= 700
x= 20
y= 20
# Create a canvas widget
canvas= Canvas(root, width=w, height=h)
canvas.pack()

# Load an image
img=ImageTk.PhotoImage(im1)


# Add image to the Canvas Items
my_image = canvas.create_image(x, y, anchor=CENTER, image=img)


# Listening the keyboard events
def left(event):
    global x,y
    x_diff = -10
    y_diff = 0
    new_x = x + x_diff
    new_y = y + y_diff
    canvas.create_line(x,y,new_x,new_y)
    x=new_x
    y=new_y
    canvas.move(my_image,x_diff,y_diff)
    im1 = im1.rotate(90, PIL.Image.NEAREST, expand = 1)
    canvas.after(100,)

def right(event):
    global x,y
    x_diff = 10
    y_diff = 0
    new_x = x + x_diff
    new_y = y + y_diff
    canvas.create_line(x,y,new_x,new_y)
    x=new_x
    y=new_y
    canvas.move(my_image,x_diff,y_diff)

def up(event):
    global x,y
    x_diff = 0
    y_diff = -10
    new_x = x + x_diff
    new_y = y + y_diff
    canvas.create_line(x,y,new_x,new_y)
    x=new_x
    y=new_y
    canvas.move(my_image,x_diff,y_diff)

def down(event):
    global x,y
    x_diff = 0
    y_diff = 10
    new_x = x + x_diff
    new_y = y + y_diff
    canvas.create_line(x,y,new_x,new_y)
    x=new_x
    y=new_y
    canvas.move(my_image,x_diff,y_diff)
root.bind("<Left>",left)
root.bind("<Right>",right)
root.bind("<Up>",up)
root.bind("<Down>",down)

root.mainloop()