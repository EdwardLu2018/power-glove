import serial, time
import numpy as np
from data import Data
import pickle
from swipeGestureFunctions import *
from utils import *
from pose_classifier import PoseClassifier


def main():
    ser1 = serial.Serial('/dev/cu.usbmodem14201', 9600)
    #ser2 = serial.Serial('/dev/ttyACM1', 9600)

    clf = PoseClassifier()

    time.sleep(1)
    count = 0
    tempcount = -100
    while True:
        if ser1.inWaiting() > 0:
            try:
                raw_data = ser1.readline().decode('utf-8')
            except:
                print("failed serial, ignoring")
                continue

            line = raw_data.replace("\r\n", "")
            # data = np.fromstring(line, dtype=int, sep=" ")

            # print(line.split(" "))
            data = str_to_list(line)
            # print(data)

            if len(data) < 15:
                print("incorrect data, ignoring")
                continue

            data = Data(list(data))
            flex_data = [data.flex_data()]
            flex_data = data.flex_data()
            velx_data = data.x
            vely_data = data.y
            velz_data = data.z
            orientation = data.orientation
            count+=1

            pose = clf.classify_pose(data, right = False)

            swipevert = (detectSwipe(orientation, velx_data, vely_data, velz_data, ser1) != None)
            swipeside = (detectLRSwipe(orientation, velx_data, vely_data, velz_data, ser1) != None )
            if (tempcount < count - 10):
                #print((velx_data,vely_data, velz_data, orientation, detectSwipe(orientation, velx_data, vely_data, velz_data, ser1), detectLRSwipe(orientation, velx_data, vely_data, velz_data, ser1)))
                if (swipeside or swipevert) and not (swipeside and swipevert) and (pose == clf.NEUTRAL or pose == clf.OPEN):
                    if (swipevert):
                        print(detectSwipe(orientation, velx_data, vely_data, velz_data, ser1))
                    else:
                        print(detectLRSwipe(orientation, velx_data, vely_data, velz_data, ser1))
                    tempcount = count

        # time.sleep(0.25)

if __name__ == '__main__':
    main()
