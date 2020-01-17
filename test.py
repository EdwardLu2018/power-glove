import serial, time
import numpy as np
from data import Data
import pickle
from swipeGestureFunctions import *
from utils import *
from pose_classifier import PoseClassifier
from getGestures import *


def main():
    ser1 = serial.Serial('/dev/ttyACM0', 9600)
    ser2 = serial.Serial('/dev/ttyACM1', 9600)
    key_ser = serial.Serial('/dev/ttyTHS1', 9600)

    clf = PoseClassifier()

    time.sleep(1)
    count = 0
    tempcount = -100
    while True:
        if ser1.inWaiting() > 0 and ser2.inWaiting() > 0:
            try:
                raw_data = ser1.readline().decode('utf-8')
                raw_data2 = ser2.readline().decode('utf-8')
                line = raw_data.replace("\r\n", "")
                line2 = raw_data2.replace("\r\n", "")
                # print(line.split(" "))
                data = str_to_list(line) + [1]
                data2 = str_to_list(line2) + [1]
                # print(data)

            except:
                print("failed serial, ignoring")
                continue


            # data = np.fromstring(line, dtype=int, sep=" ")

            if len(data) < 15 or len(data2) < 15:
                print("incorrect data, ignoring")
                continue

            data = Data(list(data))
            data2 = Data(data2)
            flex_data = data.flex_data()
            flex_data2 = data2.flex_data()

            count+=1

            pose = clf.classify_pose(data, right = False)
            pose2 = clf.classify_pose(data2, right= True)

            left_swipeDir, tempcount = getSwipeInfo(pose, data, count, tempcount, ser1, clf, False)
            rght_swipeDir, tempcount = getSwipeInfo(pose2, data2, count, tempcount, ser1, clf, True)


            #print(left_swipeDir, rght_swipeDir)
            if rght_swipeDir != None:
                print("right ges")
                #serial send right hand gesture
                if rght_swipeDir == "SWIPE UP":
                    key_ser.write(chr(3).encode())
                elif rght_swipeDir == "SWIPE DOWN":
                    key_ser.write(chr(4).encode())
                elif rght_swipeDir == "SWIPE RIGHT":
                    key_ser.write(chr(1).encode())
                elif rght_swipeDir == "SWIPE LEFT":
                    key_ser.write(chr(0).encode())
                elif rght_swipeDir == "volume up":
                    key_ser.write(chr(133).encode())
                elif rght_swipeDir == "volume down":
                    key_ser.write(chr(134).encode())
            elif left_swipeDir != None:
                print("left ges")
                if left_swipeDir == "SWIPE UP":
                    key_ser.write(chr(3).encode())
                elif left_swipeDir == "SWIPE DOWN":
                    key_ser.write(chr(4).encode())
                elif rght_swipeDir == "SWIPE RIGHT":
                    key_ser.write(chr(1).encode())
                elif rght_swipeDir == "SWIPE LEFT":
                    key_ser.write(chr(0).encode())
                elif left_swipeDir == "volume up":
                    key_ser.write(chr(133).encode())
                elif left_swipeDir == "volume down":
                    key_ser.write(chr(134).encode())
                #serial send left hand gesture
        # time.sleep(0.25)

if __name__ == '__main__':
    main()
