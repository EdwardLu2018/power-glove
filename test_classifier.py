import serial, time
import numpy as np
from data import Data
import pickle

FILENAME = "left_flex_data.txt"

OPEN = '0'
FIST = '1'
ONE = '2'
TWO = '3'
THREE = '4'
FOUR = '5'
MIDDLE = '6'
OK = '7'
ROCK ='8'
NEUTRAL = '9'
CALI = '10'
THUMB = '11'
GUN = '12'

def str_to_list(string):
    return [int(s) for s in string.split(' ')]

def list_to_str(lst):
    return " ".join([str(elem) for elem in lst])

def main():
    ser1 = serial.Serial('/dev/ttyACM0', 9600)
    #ser2 = serial.Serial('/dev/ttyACM1', 9600)

    clf = pickle.open('left_glove_classifier.pkl')

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
            flex_data = data.flex_data()
            print(flex_data)

            print(clf.predict(flex_data))
        time.sleep(0.25)

if __name__ == '__main__':
    main()
