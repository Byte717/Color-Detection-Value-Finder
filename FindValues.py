import cv2
import os
import argparse
import tkinter as tk
from typing import Any
import numpy as np
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
cam = None
class Window(tk.Tk):
    def __init__(self, imageDir:str = None,webcam: bool = False, showPath:bool = False) -> None:
        super().__init__()
        self.Font_tuple = ("Comic Sans MS", 18, "bold")
        self.Font_tuple2 = ("Comic Sans MS", 15, "bold")
        self.title("RGB Value Tester")
        self.config(bg="gray19")
        self.showPath = showPath
        self.protocol("WM_DELETE_WINDOW",self.onClose)
        # self.geometry("1920x1080")
        if imageDir is None and webcam == False:
            print("Source not provided in arguments")
            raise
        elif webcam:
            # self.cam = cv2.VideoCapture(0)
            self.img = np.zeros((200,400,3),dtype=np.uint8)
            pass

        elif os.path.exists(imageDir) == False:
            print(bcolors.FAIL + bcolors.UNDERLINE + "INVALID PATH" + bcolors.ENDC)
            raise
        else:
            self.dir = imageDir
            if os.path.isfile(imageDir):
                self.img = cv2.imread(self.dir)

            elif os.path.isdir(imageDir):
                self.imageIndex = 0
                self.paths = list(os.listdir(imageDir))
                self.n = len(self.paths)

                if self.showPath:
                    text = os.path.join(self.dir,self.paths[self.imageIndex])
                else:
                    text = self.paths[self.imageIndex]

                self.imageLabel = tk.Label(self,text=text, bg="gray25",fg="White",font=self.Font_tuple)
                self.imageLabel.grid(row=0,column=2)

                self.keyboardSetup()
                self.MultipleInit()
                self.img = cv2.imread(os.path.join(self.dir,self.paths[self.imageIndex]))


        imgtk = self.parse_image(self.img)
        self.original = tk.Label(self,image=imgtk)
        self.original.image = imgtk
        self.original.grid(row=1,column=1)

        self.display = tk.Label(self, image=imgtk)
        self.display.image = imgtk
        self.display.grid(row=1,column=3)


        self.l1 = tk.Label(self,text="Low Red Value", fg='Red',bg="gray19",font=self.Font_tuple2)
        self.l1.grid(row=2,column=1,sticky="NS")
        self.LowRed = tk.Scale(self, from_= 0, to=255, orient=tk.HORIZONTAL,command=self.callback, length=300,bg="gray35",fg="White")
        self.LowRed.grid(row =3,column=1,sticky="NS")

        self.l2 = tk.Label(self, text="High Red Value",fg='Red',bg="gray19",font=self.Font_tuple2)
        self.l2.grid(row=4,column=1,sticky="NS")
        self.HighRed = tk.Scale(self, from_= 0, to=255, orient=tk.HORIZONTAL,command=self.callback, length=300,bg="gray35",fg="White")
        self.HighRed.set(255)
        self.HighRed.grid(row=5,column=1,sticky="NS")

        self.l5 = tk.Label(self, text="Low Green Value",fg='lawn green',bg="gray19",font=self.Font_tuple2)
        self.l5.grid(row=2,column=2,sticky="NSEW")
        self.LowGreen = tk.Scale(self, from_= 0, to=255, orient=tk.HORIZONTAL,command=self.callback, length=300,bg="gray35",fg="White")
        self.LowGreen.grid(row=3,column=2,sticky="NS")

        self.l6 = tk.Label(self, text="High Green Value",fg='lawn Green',bg="gray19",font=self.Font_tuple2)
        self.l6.grid(row=4,column=2,sticky="NSEW")
        self.HighGreen = tk.Scale(self, from_= 0, to=255, orient=tk.HORIZONTAL,command=self.callback, length=300,bg="gray35",fg="White")
        self.HighGreen.set(255)
        self.HighGreen.grid(row=5,column=2,sticky="NS")

        self.l3 = tk.Label(self, text="Low Blue Value",fg='DodgerBlue',bg="gray19",font=self.Font_tuple2)
        self.l3.grid(row=2,column=3,sticky="NS")
        self.LowBlue = tk.Scale(self, from_= 0, to=255, orient=tk.HORIZONTAL,command=self.callback, length=300,bg="gray35",fg="White")
        self.LowBlue.grid(row=3,column=3,sticky="NS")


        self.l4 = tk.Label(self, text="High Blue Value",fg='DodgerBlue',bg="gray19",font=self.Font_tuple2)
        self.l4.grid(row=4,column=3,sticky="NS")
        self.HighBlue = tk.Scale(self, from_= 0, to=255, orient=tk.HORIZONTAL,command=self.callback, length=300,bg="gray35",fg="White")
        self.HighBlue.set(255)
        self.HighBlue.grid(row=5,column=3,sticky="NS")



    def keyboardSetup(self) -> None:
        self.bind('<Left>', self.leftPress)
        self.bind('<Right>',self.rightPress)

    def MultipleInit(self) -> None:
        self.leftButton = tk.Button(self, text="<<--", width=10,height=5, bg="gray25",fg="White",command=self.leftPress)
        self.leftButton.grid(row= 3,column=0)

        self.rightButton = tk.Button(self, text="-->>", width=10, height=5, bg="gray25", fg="White",command=self.rightPress)
        self.rightButton.grid(row =3, column=4)
        pass


    def changeCameraFrame(self) -> None:
        parsed = self.parse_image(self.img)
        self.original.configure(image=parsed)
        self.original.image = parsed
        self.callback()
    def changeImage(self, path = None, image = None) -> None:
        if path is None:
            print("NO PATH PROVIDED")
            raise
        else:
            if self.showPath:
                self.imageLabel.config(text=os.path.join(path,image))
            else:
                self.imageLabel.config(text=image)
            self.img = cv2.imread(os.path.join(path,image))
            parsed = self.parse_image(self.img)
            self.original.configure(image=parsed)
            self.original.image = parsed
            self.callback()


    def leftPress(self,event=None) -> None:
        if self.imageIndex == 0:
            return
        else:
            self.imageIndex -= 1
            self.changeImage(self.dir, self.paths[self.imageIndex])


    def rightPress(self, event=None) -> None:
        if self.imageIndex + 1 == self.n:
            return
        else:
            self.imageIndex += 1
            self.changeImage(self.dir, self.paths[self.imageIndex])

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
        print(self.too_big(self.img))


    def onClose(self) -> None:
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

    def too_big(self,img) -> bool:
        currentHeight, currentWidth = self.winfo_height(), self.winfo_width()
        imgHeight, imgWidth, _ = img.shape
        if imgHeight > currentHeight or imgWidth > currentWidth:
            return True
        else:
            if imgHeight > 0.4 * currentHeight or imgWidth > 0.4 * currentWidth:
                return True

        return False

    def resize_to_Scale(self) -> Any:

        pass

def main() -> int:
    global cam
    parser = argparse.ArgumentParser()
    parser.add_argument("-dir", "--dir", help="Use images")
    parser.add_argument("-webcam","--webcam",help="Use webcam",action="store_true")
    parser.add_argument("-absolutePath","--absolutePath",help="Show Entire paths",action="store_true")
    args = parser.parse_args()
    if args.webcam:
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    window = Window(args.dir,args.webcam,args.absolutePath)

    while not exit:
        if args.webcam:
            _,window.img = cam.read()
            window.changeCameraFrame()
        window.update_idletasks()
        window.update()
    return 0


if __name__ == '__main__':
    res : int = main()
    print("\n")
    print(bcolors.WARNING + "Code executed with exit code " + bcolors.ENDC, end='')
    print(bcolors.OKBLUE + str(res) + bcolors.ENDC)