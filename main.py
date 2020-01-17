import serial, time
import numpy as np
from data import Data
import pickle
from swipeGestureFunctions import *
from utils import *
from pose_classifier import PoseClassifier
from poses_fsm import *
import actions

from getGestures import *

LEFT_GLOVE_PORT = ''
RGHT_GLOVE_PORT = ''
KEYBOARD_PORT = '/dev/ttyTHS1'
BAUD = 9600

def main():
    left_ser = serial.Serial(LEFT_GLOVE_PORT, BAUD)
    rght_ser = serial.Serial(RGHT_GLOVE_PORT, BAUD)
    key_ser = serial.Serial(KEYBOARD_PORT, BAUD)

    clf = PoseClassifier()

    chrome_fsm = OpenChromeFSM()

    print("Starting...")
    time.sleep(2)

    count = 0
    tempcount = -100

    previous_r_action = None
    previous_l_action = None

    while True:
        if left_ser.inWaiting() and rght_ser.inWaiting():
            try:
                left_raw_data = left_ser.readline().decode('utf-8')
                rght_raw_data = rght_ser.readline().decode('utf-8')
            except:
                print("failed serial, ignoring")
                continue

            l_line = left_raw_data.replace("\r\n", "")
            left_data = list(map(int, l_line.split(' '))) + [2]
            r_line = left_raw_data.replace("\r\n", "")
            rght_data = list(map(int, r_line.split(' '))) + [2]

            if len(left_data) < 15 or len(rght_data) < 15:
                print("incorrect data, ignoring")
                continue

            left_data = Data(left_data)
            rght_data = Data(rght_data)

            if left_data.mode == 0 and rght_data.mode == 0:
                pass

            elif left_data.mode == 1 and rght_data.mode == 1:
                left_action = actions.call_left_action(left_data)
                rght_action = actions.call_right_action(rght_data)

                '''
                if previous_action != None and previous_action == right_action:
                    time.sleep(.3)
                    previous_action = None
                    continue
                if right_action != None:
                    print(right_action, chr(right_action))
                    print("Mode: ", right_glove.mode)
                key_ser.write(chr(right_action).encode())
                previous_action = right_action
                '''

            elif left_data.mode == 2 and rght_data.mode == 2:
                left_pose = clf.classify_pose(left_data, right=False)
                rght_pose = clf.classify_pose(rght_data, right=True)

                rght_swipeInfo = getSwipeInfo(rght_pose, rght_data, count, tempcount, rght_ser, clf)
                left_swipeInfo = getSwipeInfo(left_pose, left_data, count, tempcount, left_ser, clf)
                
                rhgt_swipeDir = rhgt_swipeInfo[0]
                rhgt_swipeDir = left_swipeInfo[0]
                
                if rght_swipeDir != None:
                    #serial send right hand gesture
                    if rght_swipeDir == "SWIPE UP":
                        key_ser.write(chr(3).encode())
                    elif rght_swipeDir == "SWIPE DOWN":
                        key_ser.write(chr(4).encode())
                    elif rght_swipeDir == "volume up":
                        key_ser.write(chr(133).encode())
                    elif rght_swipeDir == "volume down":
                        key_ser.write(chr(134).encode())
                    tempcount = rght_swipeInfo[1]
                elif left_swipeDir != None:
                    if left_swipeDir == "SWIPE UP":
                        key_ser.write(chr(3).encode())
                    elif left_swipeDir == "SWIPE DOWN":
                        key_ser.write(chr(4).encode())
                    elif left_swipeDir == "volume up":
                        key_ser.write(chr(133).encode())
                    elif left_swipeDir == "volume down":
                        key_ser.write(chr(134).encode())
                    #serial send left hand gesture
                    tempcount = left_swipeInfo[1]
                

                if OpenChromeFSM.update(left_data, left_pose, clf):
                    key_ser.write(chr(6).encode())
                elif CloseWindowFSM.update(left_data, left_pose, clf):
                    key_ser.write(chr(7).encode())
                elif MinimizeFSM.update(left_data, left_pose, clf):
                    key_ser.write(chr(2).encode())
                elif FaceTimeFSM.update(left_data, left_pose, clf):
                    key_ser.write(chr(130).encode())
                elif ITunesFSM.update(left_data, left_pose, clf):
                    key_ser.write(chr(131).encode())
                elif EnterFSM.update(left_data, left_pose, clf):
                    key_ser.write(chr(132).encode())
                elif ShowWindowsFSM.update(left_data,left_pose, clf):
                    key_ser.write(chr(129).encode())
                elif OpenChromeFSM.update(rght_data, rght_pose, clf):
                    key_ser.write(chr(6).encode())
                elif CloseWindowFSM.update(rght_data, rght_pose, clf):
                    key_ser.write(chr(7).encode())
                elif MinimizeFSM.update(rght_data, rght_pose, clf):
                    key_ser.write(chr(2).encode())
                elif FaceTimeFSM.update(rght_data, rght_pose, clf):
                    key_ser.write(chr(130).encode())
                elif ITunesFSM.update(rght_data, rght_pose, clf):
                    key_ser.write(chr(131).encode())
                elif EnterFSM.update(rght_data, rght_pose, clf):
                    key_ser.write(chr(132).encode())
                elif ShowWindowsFSM.update(rght_data,rght_pose, clf):
                    key_ser.write(chr(129).encode())


if __name__ == '__main__':
    main()
