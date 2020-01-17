import serial, time
import numpy as np
from data import Data
import pickle
from swipeGestureFunctions import *
from utils import *
from pose_classifier import PoseClassifier
from spells_fsm import *


def main():
    ser1 = serial.Serial('/dev/cu.usbmodem14201', 9600)
    #ser2 = serial.Serial('/dev/ttyACM1', 9600)

    clf = PoseClassifier()

    chrome_fsm = OpenChromeFSM()

    time.sleep(1)

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

            pose = clf.classify_pose(data, right = False)

            if chrome_fsm.update(data, pose, clf):
                print("did it")

        # time.sleep(0.25)

if __name__ == '__main__':
    main()
