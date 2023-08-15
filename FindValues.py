import cv2
import numpy
import os
import matplotlib.pyplot as plt
import argparse
from typing import *
import tkinter as tk
from PIL import Image, ImageTk
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Window(tk.Tk):
    def __init__(self, imageDir:str = None) -> None:
        super().__init__()
        self.title("RGB Value Tester")
        self.config(bg="gray19")
        if imageDir is None:
            print("Image Not provided in arguments")
            raise
        else:
            self.dir = imageDir
            self.img = cv2.imread(self.dir)
            # cv2.imshow("DHJK",self.img)

        imgtk = self.parse_image(self.img)
        self.original = tk.Label(self,image=imgtk)
        self.original.image = imgtk
        self.original.pack()

        self.display = tk.Label(self, image=imgtk)
        self.display.image = imgtk
        self.display.pack(side=tk.TOP)


        self.l1 = tk.Label(self,text="Low Red Value", fg='Red',bg="gray19")
        self.l1.pack()
        self.LowRed = tk.Scale(self, from_= 0, to=255, orient=tk.HORIZONTAL,command=self.callback, length=300,bg="gray19",fg="White")
        self.LowRed.pack()

        self.l2 = tk.Label(self, text="High Red Value",fg='Red',bg="gray19")
        self.l2.pack()
        self.HighRed = tk.Scale(self, from_= 0, to=255, orient=tk.HORIZONTAL,command=self.callback, length=300,bg="gray19",fg="White")
        self.HighRed.set(255)
        self.HighRed.pack()

        self.l3 = tk.Label(self, text="Low Blue Value",fg='Blue',bg="gray19")
        self.l3.pack()
        self.LowBlue = tk.Scale(self, from_= 0, to=255, orient=tk.HORIZONTAL,command=self.callback, length=300,bg="gray19",fg="White")
        self.LowBlue.pack()


        self.l4 = tk.Label(self, text="High Blue Value",fg='Blue',bg="gray19")
        self.l4.pack()
        self.HighBlue = tk.Scale(self, from_= 0, to=255, orient=tk.HORIZONTAL,command=self.callback, length=300,bg="gray19",fg="White")
        self.HighBlue.set(255)
        self.HighBlue.pack()

        self.l5 = tk.Label(self, text="Low Green Value",fg='Green',bg="gray19")
        self.l5.pack()
        self.LowGreen = tk.Scale(self, from_= 0, to=255, orient=tk.HORIZONTAL,command=self.callback, length=300,bg="gray19",fg="White")
        self.LowGreen.pack()

        self.l6 = tk.Label(self, text="High Green Value",fg='Green',bg="gray19")
        self.l6.pack()
        self.HighGreen = tk.Scale(self, from_= 0, to=255, orient=tk.HORIZONTAL,command=self.callback, length=300,bg="gray19",fg="White")
        self.HighGreen.set(255)
        self.HighGreen.pack()

    def parse_image(self,img) -> ImageTk.PhotoImage:
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(img2)
        imgtk = ImageTk.PhotoImage(image=im)
        return imgtk

    def callback(self,*args, **kwargs) -> None:
        lower, higher  = self.low(), self.high()
        mask = cv2.inRange(self.img, lower,higher)
        imgtk = self.parse_image(mask)
        self.display.configure(image=imgtk)
        self.display.image = imgtk
        pass

    def low(self) -> tuple:
        return (self.LowBlue.get(), self.LowGreen.get(), self.LowRed.get())

    def high(self) -> tuple:
        return (self.HighBlue.get(), self.HighGreen.get(), self.HighRed.get())



def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-dir", "--dir", help="Show Output")
    args = parser.parse_args()
    print(args.dir)
    window = Window(args.dir)
    window.mainloop()
    return 0


if __name__ == '__main__':

    res : int = main()
    print("\n")
    print(bcolors.WARNING + "Code executed with exit code " + bcolors.ENDC, end='')
    print(bcolors.OKBLUE + str(res) + bcolors.ENDC)