import serial, time
import numpy as np
from data import Data

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
    ser1 = serial.Serial('/dev/cu.usbmodem142201', 9600)
    #ser2 = serial.Serial('/dev/ttyACM1', 9600)

    data_file = open(FILENAME, "a")
    time.sleep(1)

    for i in range(20):
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

            data_file.write(TWO + " " + list_to_str(flex_data) + "\n")
        time.sleep(0.1)

if __name__ == '__main__':
    main()
