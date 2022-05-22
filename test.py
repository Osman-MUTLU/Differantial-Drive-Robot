import math
import tkinter as tk

from PIL import Image, ImageTk
import PIL

#https://stackoverflow.com/questions/23691966/how-to-keypress-the-keys-a-and-d-on-a-keyboard-in-python
#https://forum.yazbel.com/t/python-canvas-move-ve-rotate-yi-bir-arada-yapmak/10914/3
class Object:
    def __init__(
            self,
            master,
            img,
            coordinates,
            rotation_angle,
            x_distance,
            y_distance,
            time
    ):
        self.master = master
        self.img = img
        self._img = img
        self.rotation_angle = rotation_angle
        self.x_distance = x_distance
        self.y_distance = y_distance
        self.new_coordinates = list()
        self.new_coordinates.append(coordinates[0])
        self.new_coordinates.append(coordinates[1])
        self.time = time
        self.start_angle = 0
        self.image = ImageTk.PhotoImage(self.img)
        self.master.images += [self.image]
        self.status = False
        self.master.create_image(
            coordinates,
            image=self.image,
            tag="resim"
        )
        self.master.bind_all(
            "<KeyPress-Left>",
            lambda event: self.start_left()
        )
        self.master.bind_all(
            "<KeyRelease-Left>",
            lambda event: self.stop_left()
        )
        self.master.bind_all(
            "<KeyPress-Right>",
            lambda event: self.start_right()
        )
        self.master.bind_all(
            "<KeyRelease-Right>",
            lambda event: self.stop_right()
        )
        self.master.bind_all(
            "<KeyPress-Up>",
            lambda event: self.start_up()
        )
        self.master.bind_all(
            "<KeyRelease-Up>",
            lambda event: self.stop_up()
        )

    def start_left(self):
        self.status = True
        self.rotation_angle=10
        self.x_distance=0
        self.y_distance=0
        self.rotate()

    def stop_left(self):
        self.status = False
    def start_right(self):
        self.status = True
        self.rotation_angle=-10
        self.x_distance=0
        self.y_distance=0
        self.rotate()

    def stop_right(self):
        self.status = False
        
    def start_up(self):
        self.status = True
        self.rotation_angle=0
        angle = self.start_angle%360
        r=20
        x = math.sqrt(math.pow(r,2)/(1+math.pow(math.tan(angle*0.017453292519943295),2)))
        print(x)
        y = math.sqrt(math.pow(r,2)-math.pow(x,2))
        
        
        
        if angle>90 and angle<270:
            x = -int(x)
        else:
            x = int(x)
            
        if not (angle>180 and angle<360):
            y = -int(y)
        else:
            y = int(y)
        print("angle = {} , x= {}, y= {}".format(angle,x,y))
        self.x_distance=x
        self.y_distance=y
        
        self.rotate()

    def stop_up(self):
        self.status = False

    def rotate(self):
        if self.status:
            self.start_angle += self.rotation_angle
            self.img = self._img.rotate(self.start_angle)
            self.image = ImageTk.PhotoImage(self.img)
            self.master.itemconfig(tagOrId="resim", image=self.image)
            self.master.move("resim", self.x_distance, self.y_distance)
           
            self.master.create_line(self.new_coordinates[0],self.new_coordinates[1],(self.new_coordinates[0]+self.x_distance),self.new_coordinates[1]+self.y_distance)
            self.new_coordinates[0] += self.x_distance
            self.new_coordinates[1] += self.y_distance
            self.master.after(self.time, self.rotate)


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
        master=canvas,
        img=img,
        rotation_angle=0,
        x_distance=0,
        y_distance=0,
        time=10,
        coordinates=(50, 50)
    )
    
    root.mainloop()


if __name__ == "__main__":
    main()