import cv2
import numpy
import os
import matplotlib.pyplot as plt
import argparse
from typing import *
import tkinter as tk

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
    def __init__(self, imageDir:str = None):
        super().__init__()
        self.title("RGB Value Tester")
        if imageDir is None:
            print("Image Not provided in arguments")
            raise
        else:
            self.dir = imageDir

        self.l1 = tk.Label(self,text="Low Red Value", fg='Red')
        self.l1.pack()
        self.LowRed = tk.Scale(self, from_= 0, to=255, orient=tk.HORIZONTAL)
        self.LowRed.pack()

        self.l2 = tk.Label(self, text="High Red Value",fg='Red')
        self.l2.pack()
        self.HighRed = tk.Scale(self, from_= 0, to=255, orient=tk.HORIZONTAL)
        self.HighRed.pack()

        self.l3 = tk.Label(self, text="Low Blue Value",fg='Blue')
        self.l3.pack()
        self.LowBlue = tk.Scale(self, from_= 0, to=255, orient=tk.HORIZONTAL)
        self.LowBlue.pack()


        self.l4 = tk.Label(self, text="High Blue Value",fg='Blue')
        self.l4.pack()
        self.HighBlue = tk.Scale(self, from_= 0, to=255, orient=tk.HORIZONTAL)
        self.HighBlue.pack()

        self.l5 = tk.Label(self, text="Low Green Value",fg='Green')
        self.l5.pack()
        self.LowGreen = tk.Scale(self, from_= 0, to=255, orient=tk.HORIZONTAL)
        self.LowGreen.pack()

        self.l6 = tk.Label(self, text="High Green Value",fg='Green')
        self.l6.pack()
        self.HighGreen = tk.Scale(self, from_= 0, to=255, orient=tk.HORIZONTAL)
        self.HighGreen.pack()

    def callback(self):
        pass

    def low(self) -> tuple:
        return (self.LowBlue.get(), self.LowGreen.get(), self.LowRed.get())

    def high(self) -> tuple:
        return (self.HighBlue.get(), self.HighGreen.get(), self.HighRed.get())



def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-dir", "--dir", help="Show Output")
    args = parser.parse_args()

    window = Window(args.dir)
    window.mainloop()
    return 0


if __name__ == '__main__':

    res : int = main()
    print("\n")
    print(bcolors.WARNING + "Code executed with exit code " + bcolors.ENDC, end='')
    print(bcolors.OKBLUE + str(res) + bcolors.ENDC)