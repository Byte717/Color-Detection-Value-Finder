import cv2
import sys

# cam = cv2.Videocapture(0)
lowColor = (100,161,115)
highColor = (136,211,153)




def main():
    while True:
        frame = cv2.imread("C:\\Users\\dhair\\PycharmProjects\\ComputerVision\\Screenshot(17).png",1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv,lowColor,highColor)
        cv2.imshow(mask)




if __name__ == '__main__':
    main()