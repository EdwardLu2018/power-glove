import serial, time
from data import Data
from util import *
from spells_fsm import *
import actions
from pose_classifier import PoseClassifier
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

                # swipeInfo = getSwipeInfo(pose, data, count, tempcount, ser1, clf)
                # swipeDir = swipeInfo[0]
                # tempcount = swipeInfo[1]

                if chrome_fsm.update(left_data, left_pose, clf):
                    key_ser.write(chr("INSERT SOMETHING HERE").encode())


if __name__ == '__main__':
    main()
