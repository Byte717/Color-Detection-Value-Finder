import cv2
import os
import argparse
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
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

exit = False

class Window(tk.Tk):
    def __init__(self, imageDir:str = None,webcam: bool = False) -> None:
        super().__init__()
        self.webcam = webcam
        self.Font_tuple = ("Comic Sans MS", 20, "bold")
        self.Font_tuple2 = ("Comic Sans MS", 10, "bold")
        self.title("RGB Value Tester")
        self.config(bg="gray19")
        self.protocol("WM_DELETE_WINDOW",self.onClose)
        # self.geometry("1920x1080")
        if imageDir is None and webcam == False:
            print("Source not provided in arguments")
            raise
        elif webcam:
            self.cam = cv2.VideoCapture(0)
            self.img = self.cam.read()

        elif os.path.exists(imageDir) == False:
            print(bcolors.FAIL + bcolors.UNDERLINE + "INVALID PATH" + bcolors.ENDC)
            exit()
        else:
            self.dir = imageDir
            if os.path.isfile(imageDir):
                self.img = cv2.imread(self.dir)

            elif os.path.isdir(imageDir):
                self.imageIndex = 0
                self.paths = list(os.listdir(imageDir))
                self.n = len(self.paths)


                self.imageLabel = tk.Label(self,text=os.path.join(self.dir,self.paths[self.imageIndex]), bg="gray25",fg="White",font=self.Font_tuple)
                self.imageLabel.pack(side=tk.TOP)

                self.keyboardSetup()
                self.MultipleInit()
                self.img = cv2.imread(os.path.join(self.dir,self.paths[self.imageIndex]))


        imgtk = self.parse_image(self.img)
        self.original = tk.Label(self,image=imgtk)
        self.original.image = imgtk
        self.original.pack()

        self.display = tk.Label(self, image=imgtk)
        self.display.image = imgtk
        self.display.pack(side=tk.TOP)


        self.l1 = tk.Label(self,text="Low Red Value", fg='Red',bg="gray19",font=self.Font_tuple2)
        self.l1.pack()
        self.LowRed = tk.Scale(self, from_= 0, to=255, orient=tk.HORIZONTAL,command=self.callback, length=300,bg="gray35",fg="White")
        self.LowRed.pack()

        self.l2 = tk.Label(self, text="High Red Value",fg='Red',bg="gray19",font=self.Font_tuple2)
        self.l2.pack()
        self.HighRed = tk.Scale(self, from_= 0, to=255, orient=tk.HORIZONTAL,command=self.callback, length=300,bg="gray35",fg="White")
        self.HighRed.set(255)
        self.HighRed.pack()

        self.l3 = tk.Label(self, text="Low Blue Value",fg='DodgerBlue',bg="gray19",font=self.Font_tuple2)
        self.l3.pack()
        self.LowBlue = tk.Scale(self, from_= 0, to=255, orient=tk.HORIZONTAL,command=self.callback, length=300,bg="gray35",fg="White")
        self.LowBlue.pack()


        self.l4 = tk.Label(self, text="High Blue Value",fg='DodgerBlue',bg="gray19",font=self.Font_tuple2)
        self.l4.pack()
        self.HighBlue = tk.Scale(self, from_= 0, to=255, orient=tk.HORIZONTAL,command=self.callback, length=300,bg="gray35",fg="White")
        self.HighBlue.set(255)
        self.HighBlue.pack()

        self.l5 = tk.Label(self, text="Low Green Value",fg='lawn green',bg="gray19",font=self.Font_tuple2)
        self.l5.pack()
        self.LowGreen = tk.Scale(self, from_= 0, to=255, orient=tk.HORIZONTAL,command=self.callback, length=300,bg="gray35",fg="White")
        self.LowGreen.pack()

        self.l6 = tk.Label(self, text="High Green Value",fg='lawn Green',bg="gray19",font=self.Font_tuple2)
        self.l6.pack()
        self.HighGreen = tk.Scale(self, from_= 0, to=255, orient=tk.HORIZONTAL,command=self.callback, length=300,bg="gray35",fg="White")
        self.HighGreen.set(255)
        self.HighGreen.pack()


    def keyboardSetup(self):
        self.bind('<Left>', self.leftPress)
        self.bind('<Right>',self.rightPress)

    def MultipleInit(self) -> None:
        self.leftButton = tk.Button(self, text="<-", width=10,height=5, bg="gray25",fg="White",command=self.leftPress)
        self.leftButton.pack(side=tk.LEFT)

        self.rightButton = tk.Button(self, text="->", width=10, height=5, bg="gray25", fg="White",command=self.rightPress)
        self.rightButton.pack(side=tk.RIGHT)
        pass

    def changeImage(self, path = None):
        if path is None:
            print("NO PATH PROVIDED")
            raise
        else:
            self.imageLabel.config(text=path)
            self.img = cv2.imread(path)
            parsed = self.parse_image(self.img)
            self.original.configure(image=parsed)
            self.original.image = parsed
            self.callback()


    def leftPress(self,event=None):
        if self.imageIndex == 0:
            return
        else:
            self.imageIndex -= 1
            self.changeImage(os.path.join(self.dir, self.paths[self.imageIndex]))


    def rightPress(self, event=None):
        if self.imageIndex + 1 == self.n:
            return
        else:
            self.imageIndex += 1
            self.changeImage(os.path.join(self.dir, self.paths[self.imageIndex]))
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


    def onClose(self):
        global exit
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            print(f"Lower values BGR: {self.low()}")
            print(f"Higher values BGR: {self.high()}")
            exit = True
            self.destroy()

    def low(self) -> tuple:
        return (self.LowBlue.get(), self.LowGreen.get(), self.LowRed.get())

    def high(self) -> tuple:
        return (self.HighBlue.get(), self.HighGreen.get(), self.HighRed.get())



def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-dir", "--dir", help="Use images")
    parser.add_argument("-webcam","--webcam",help="Use webcam",action="store_true")
    args = parser.parse_args()
    window = Window(args.dir,args.webcam)

    while not exit:
        if window.webcam:
            window.img = window.cam.read()
        window.update_idletasks()
        window.update()
    return 0


if __name__ == '__main__':

    res : int = main()
    print("\n")
    print(bcolors.WARNING + "Code executed with exit code " + bcolors.ENDC, end='')
    print(bcolors.OKBLUE + str(res) + bcolors.ENDC)