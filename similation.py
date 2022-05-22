import math
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import PIL

class Object:
    def __init__(
            self,
            canvas,
            img,
            coordinates,
            rotation_angle,
            time
        ):
        self.canvas = canvas
        self.img = img
        self._img = img
        self.rotation_angle = rotation_angle
        self.new_coordinates = list()
        self.new_coordinates.append(coordinates[0])
        self.new_coordinates.append(coordinates[1])
        self.x_distance = 0
        self.y_distance = 0
        self.time = time
        self.start_angle = 0
        self.image = ImageTk.PhotoImage(self.img)
        self.canvas.images += [self.image]
        self.status = False
        self.canvas.create_image(
            coordinates,
            image=self.image,
            tag="resim"
        )
        self.canvas.bind_all(
            "<KeyPress-Left>",
            lambda event: self.start_left()
        )
        
        self.canvas.bind_all(
            "<KeyRelease-Left>",
            lambda event: self.stop_left()
        )
        self.canvas.bind_all(
            "<KeyPress-Right>",
            lambda event: self.start_right()
        )
        self.canvas.bind_all(
            "<KeyRelease-Right>",
            lambda event: self.stop_right()
        )
        self.canvas.bind_all(
            "<KeyPress-Up>",
            lambda event: self.start_up()
        )
        self.canvas.bind_all(
            "<KeyRelease-Up>",
            lambda event: self.stop_up()
        )
        
    def start_left(self):
        self.status = True
        self.rotate()

    def stop_left(self):
        self.status = False
        
    def start_right(self):
        self.status = True
        self.rotate()

    def stop_right(self):
        self.status = False
        
    def start_up(self):
        self.status = True
        self.rotate()
        
    def stop_up(self):
        self.status = False
        
    def rotate(self):
        if self.status:
            self.start_angle += self.rotation_angle
            self.img = self._img.rotate(self.start_angle)
            self.image = ImageTk.PhotoImage(self.img)
            self.canvas.itemconfig(tagOrId="img", image=self.image)
            self.canvas.move(
                "img",
                self.x_distance,
                self.y_distance
            )
            self.canvas.create_line(
                self.new_coordinates[0],
                self.new_coordinates[1],
                (self.new_coordinates[0]+self.x_distance),
                self.new_coordinates[1]+self.y_distance
            )
            self.new_coordinates[0] += self.x_distance
            self.new_coordinates[1] += self.y_distance
            
            self.canvas.after(self.time, self.rotate)

def main():
    root = tk.Tk()
    root.geometry("1250x700")
    w= 1250
    h= 700
    canvas = tk.Canvas(master=root, width=w, height=h)
    canvas.pack()
    canvas.images = []
    img = Image.open("image.png")
    img = img.rotate(-90, PIL.Image.NEAREST, expand = 1)
    Object(
        canvas=canvas,
        img=img,
        coordinates=(50, 50),
        rotation_angle=0,
        time=10
    )
    root.mainloop()
if __name__ == '__main__':
    main()