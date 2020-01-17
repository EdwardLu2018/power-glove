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

LEFT_GLOVE_PORT = '/dev/ttyACM0'
RGHT_GLOVE_PORT = '/dev/ttyACM1'
KEYBOARD_PORT = '/dev/ttyTHS1'
BAUD = 9600

def main():
    left_ser = serial.Serial(LEFT_GLOVE_PORT, BAUD)
    rght_ser = serial.Serial(RGHT_GLOVE_PORT, BAUD)
    key_ser = serial.Serial(KEYBOARD_PORT, BAUD)

    clf = PoseClassifier()

    chrome_fsm = OpenChromeFSM()
    closeWin_fsm = CloseWindowFSM()
    minim_fsm = MinimizeFSM()
    ft_fsm = FacetimeFSM()
    it_fsm = ITunesFSM()
    ent_fsm = EnterFSM()
    showAllWin_fsm = ShowWindowsFSM() 


    print("Starting...")
    time.sleep(2)

    count = 0
    tempcount = -100

    previous_r_action = None
    previous_l_action = None
    mode = 2

    while True:
        if left_ser.inWaiting() and rght_ser.inWaiting():
            try:
                left_raw_data = left_ser.readline().decode('utf-8')
                rght_raw_data = rght_ser.readline().decode('utf-8')
            except:
                print("failed serial, ignoring")
                continue

            try:
                l_line = left_raw_data.replace("\r\n", "")
                left_data = list(map(int, l_line.split(' '))) + [mode]
                r_line = left_raw_data.replace("\r\n", "")
                rght_data = list(map(int, r_line.split(' '))) + [mode]
            except:
                continue

            if len(left_data) < 15 or len(rght_data) < 15:
                print("incorrect data, ignoring")
                continue
            
            #print(rght_data)
            left_data = Data(left_data)
            rght_data = Data(rght_data)
            left_data.mode = mode
            rght_data.mode = mode
            left_action = actions.call_left_action(left_data)
            rght_action = actions.call_right_action(rght_data)
            #print(left_action, rght_action) 
            action = left_action if rght_action == None else rght_action
            # checks mode switch
            if action == 100:
                mode = rght_data.mode
                print("New Mode: ", mode)
                left_data.mode = mode
                continue
            elif mode == 0:
                pass
            elif mode == 1:
                if action != None:
                    key_ser.write(chr(action).encode())
                continue
            elif mode == 2:

                
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

                left_pose = clf.classify_pose(left_data, right=False)
                rght_pose = clf.classify_pose(rght_data, right=True)
                #print(rght_data.x)
            
                rght_swipeInfo = getSwipeInfo(rght_pose, rght_data, count, tempcount, rght_ser, clf, True)
                left_swipeInfo = getSwipeInfo(left_pose, left_data, count, tempcount, left_ser, clf, False)

                rght_swipeDir = rght_swipeInfo[0]
                left_swipeDir = left_swipeInfo[0]

                #print(rght_swipeDir, left_swipeDir)
                
                if rght_swipeDir != None:
                    #serial send right hand gesture
                    if rght_swipeDir == "SWIPE UP":
                        key_ser.write(chr(3).encode())
                    elif rght_swipeDir == "SWIPE DOWN":
                        key_ser.write(chr(129).encode())
                    elif rght_swipeDir == "SWIPE RIGHT":
                        key_ser.write(chr(0).encode())
                    elif rght_swipeDir == "SWIPE LEFT":
                        key_ser.write(chr(1).encode())
                    elif rght_swipeDir == "volume up":
                        key_ser.write(chr(133).encode())
                    elif rght_swipeDir == "volume down":
                        key_ser.write(chr(134).encode())
                    tempcount = rght_swipeInfo[1]
                if left_swipeDir != None:
                    if left_swipeDir == "SWIPE UP":
                        key_ser.write(chr(3).encode())
                    elif left_swipeDir == "SWIPE DOWN":
                        key_ser.write(chr(129).encode())
                    elif rght_swipeDir == "SWIPE RIGHT":
                        key_ser.write(chr(0).encode())
                    elif rght_swipeDir == "SWIPE LEFT":
                        key_ser.write(chr(1).encode())
                    elif left_swipeDir == "volume up":
                        key_ser.write(chr(133).encode())
                    elif left_swipeDir == "volume down":
                        key_ser.write(chr(134).encode())
                    #serial send left hand gesture
                    tempcount = left_swipeInfo[1]
                
            
                if chrome_fsm.update(left_data, left_pose, clf):
                    key_ser.write(chr(6).encode())
                elif closeWin_fsm.update(left_data, left_pose, clf):
                    key_ser.write(chr(7).encode())
                elif minim_fsm.update(left_data, left_pose, clf):
                    key_ser.write(chr(2).encode())
                elif ft_fsm.update(left_data, left_pose, clf):
                    key_ser.write(chr(130).encode())
                elif it_fsm.update(left_data, left_pose, clf):
                    key_ser.write(chr(131).encode())
                elif ent_fsm.update(left_data, left_pose, clf):
                    key_ser.write(chr(132).encode())
                elif showAllWin_fsm.update(left_data,left_pose, clf):
                    key_ser.write(chr(129).encode())
                '''
                elif chrome_fsm.update(rght_data, rght_pose, clf):
                    key_ser.write(chr(6).encode())
                elif closeWin_fsm.update(rght_data, rght_pose, clf):
                    key_ser.write(chr(7).encode())
                elif minim_fsm.update(rght_data, rght_pose, clf):
                    key_ser.write(chr(2).encode())
                elif ft_fsm.update(rght_data, rght_pose, clf):
                    key_ser.write(chr(130).encode())
                elif it_fsm.update(rght_data, rght_pose, clf):
                    key_ser.write(chr(131).encode())
                elif ent_fsm.update(rght_data, rght_pose, clf):
                    key_ser.write(chr(132).encode())
                elif showAllWin_fsm.update(rght_data,rght_pose, clf):
                    key_ser.write(chr(129).encode())
'''

if __name__ == '__main__':
    main()
