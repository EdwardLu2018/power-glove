import serial, time
import numpy as np
from data import Data
import pickle
from swipeGestureFunctions import *
from utils import *
from pose_classifier import PoseClassifier
from getGestures import *
from poses_fsm import *
import actions


OPEN = 0
FIST = 1
ONE = 2
TWO = 3
THREE = 4
FOUR = 5
MIDDLE = 6
OK = 7
ROCK =8
NEUTRAL = 9
CALI = 10
THUMB = 11
GUN = 12



def main():
    ser1 = serial.Serial('/dev/ttyACM0', 9600)
    ser2 = serial.Serial('/dev/ttyACM1', 9600)
    key_ser = serial.Serial('/dev/ttyTHS1', 9600)

    clf = PoseClassifier()

    chrome_fsm = OpenChromeFSM()
    closeWin_fsm = CloseWindowFSM()
    minim_fsm = MinimizeFSM()
    ft_fsm = FacetimeFSM()
    it_fsm = ITunesFSM()
    ent_fsm = EnterFSM()
    showAllWin_fsm = ShowWindowsFSM()

    chrome_fsm1 = OpenChromeFSM()
    closeWin_fsm1 = CloseWindowFSM()
    minim_fsm1 = MinimizeFSM()
    ft_fsm1 = FacetimeFSM()
    it_fsm1 = ITunesFSM()
    ent_fsm1 = EnterFSM()
    showAllWin_fsm1 = ShowWindowsFSM()

    time.sleep(1)
    count = 0
    tempcount = -100

    previous_r_action = None
    previous_l_action = None
    mode = 2

    while True:
        if ser1.inWaiting() > 0 and ser2.inWaiting() > 0:
            try:
                raw_data = ser1.readline().decode('utf-8')
                raw_data2 = ser2.readline().decode('utf-8')
                line = raw_data.replace("\r\n", "")
                line2 = raw_data2.replace("\r\n", "")
                # print(line.split(" "))
                data = str_to_list(line) + [mode]
                data2 = str_to_list(line2) + [mode]
                #print(data)

            except:
                print("failed serial, ignoring")
                continue


            # data = np.fromstring(line, dtype=int, sep=" ")

            if len(data) < 15 or len(data2) < 15:
                print("incorrect data, ignoring")
                continue

            data = Data(data)
            data2 = Data(data2)
            flex_data = data.flex_data()
            flex_data2 = data2.flex_data()

            data.mode = mode
            data2.mode = mode
            left_action = actions.call_left_action(data)
            rght_action = actions.call_right_action(data2)
            #print(left_action, rght_action)
            action = left_action if rght_action == None else rght_action
            # checks mode switch
            if action == 100:
                mode = data2.mode
                print("New Mode: ", mode)
                data.mode = mode
                continue
            elif mode == 0:
                pass
            elif mode == 1:
                if action != None:
                    key_ser.write(chr(action).encode())
                continue
            elif mode == 2:

                count+=1

                pose = clf.classify_pose(data, right = False)
                pose2 = clf.classify_pose(data2, right= True)

                left_swipeDir, tempcount = getSwipeInfo(pose, data, count, tempcount, ser1, clf, False)
                rght_swipeDir, tempcount = getSwipeInfo(pose2, data2, count, tempcount, ser1, clf, True)

                if pose)== OPEN:
                    print("left hand open")
                elif pose)== NEUTRAL:
                    print("left hand in neutral position")
                elif pose)== FIST:
                    print("left hand fist")
                elif pose)== ONE:
                    print("left hand one")
                elif pose)== TWO:
                    print("left hand two")
                elif pose)== THREE:
                    print("left hand three")
                elif pose)== FOUR:
                    print("left hand four")
                elif pose)== MIDDLE:
                    print("left hand middle finger")
                elif pose)== ROCK:
                    print("left hand rock and roll")
                elif pose)== CALI:
                    print("left hand surfs up")
                elif pose)== THUMB:
                    print("left hand thumbs up")
                elif pose)== GUN:
                    print("left hand pew pew")

                if pose2 == OPEN:
                    print("right hand open")
                elif pose2 == NEUTRAL:
                    print("right hand in neutral position")
                elif pose2 == FIST:
                    print("right hand fist")
                elif pose2 == ONE:
                    print("right hand one")
                elif pose2 == TWO:
                    print("right hand two")
                elif pose2 == THREE:
                    print("right hand three")
                elif pose2 == FOUR:
                    print("right hand four")
                elif pose2 == MIDDLE:
                    print("right hand middle finger")
                elif pose2 == ROCK:
                    print("right hand rock and roll")
                elif pose2 == CALI:
                    print("right hand surfs up")
                elif pose2 == THUMB:
                    print("right hand thumbs up")
                elif pose2 == GUN:
                    print("right hand pew pew")

                #print(left_swipeDir, rght_swipeDir)
                if rght_swipeDir != None:
                    #print("right ges")
                    #serial send right hand gesture
                    if rght_swipeDir == "SWIPE UP":
                        key_ser.write(chr(3).encode())
                    elif rght_swipeDir == "SWIPE DOWN":
                        key_ser.write(chr(4).encode())
                    elif rght_swipeDir == "SWIPE RIGHT":
                        key_ser.write(chr(0).encode())
                    elif rght_swipeDir == "SWIPE LEFT":
                        key_ser.write(chr(1).encode())
                    elif rght_swipeDir == "volume up":
                        key_ser.write(chr(133).encode())
                    elif rght_swipeDir == "volume down":
                        key_ser.write(chr(134).encode())
                elif left_swipeDir != None:
                    #print("left ges")
                    if left_swipeDir == "SWIPE UP":
                        key_ser.write(chr(3).encode())
                    elif left_swipeDir == "SWIPE DOWN":
                        key_ser.write(chr(4).encode())
                    elif rght_swipeDir == "SWIPE RIGHT":
                        key_ser.write(chr(0).encode())
                    elif rght_swipeDir == "SWIPE LEFT":
                        key_ser.write(chr(1).encode())
                    elif left_swipeDir == "volume up":
                        key_ser.write(chr(133).encode())
                    elif left_swipeDir == "volume down":
                        key_ser.write(chr(134).encode())
                    #serial send left hand gesture
            # time.sleep(0.25)
                left_pose = pose
                right_pose = pose2
                print(pose, pose2)
                if chrome_fsm.update(data, left_pose, clf):
                    key_ser.write(chr(6).encode())
                elif closeWin_fsm.update(data, left_pose, clf):
                    key_ser.write(chr(7).encode())
                elif minim_fsm.update(data, left_pose, clf):
                    key_ser.write(chr(2).encode())
                elif ft_fsm.update(data, left_pose, clf):
                    key_ser.write(chr(130).encode())
                elif it_fsm.update(data, left_pose, clf):
                    key_ser.write(chr(131).encode())
                elif ent_fsm.update(data, left_pose, clf):
                    key_ser.write(chr(132).encode())
                elif showAllWin_fsm.update(data,left_pose, clf):
                    key_ser.write(chr(129).encode())

                if chrome_fsm1.update(data2, left_pose, clf):
                    key_ser.write(chr(6).encode())
                elif closeWin_fsm1.update(data2, left_pose, clf):
                    key_ser.write(chr(7).encode())
                elif minim_fsm1.update(data2, left_pose, clf):
                    key_ser.write(chr(2).encode())
                elif ft_fsm1.update(data2, left_pose, clf):
                    key_ser.write(chr(130).encode())
                elif it_fsm1.update(data2, left_pose, clf):
                    key_ser.write(chr(131).encode())
                elif ent_fsm1.update(data2, left_pose, clf):
                    key_ser.write(chr(132).encode())
                elif showAllWin_fsm1.update(data2,left_pose, clf):
                    key_ser.write(chr(129).encode())

if __name__ == '__main__':
    main()
