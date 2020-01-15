from data import Data
import serial
import numpy as np
import time

LEFT_GLOVE_PORT = ""
RGHT_GLOVE_PORT = ""
BAUDRATE = 9600
TIMEOUT = 1

OPEN = 0
FIST = 1
ONE = 2
TWO = 3
THREE = 4
FOUR = 5
THUMB = 6
OK = 7

def read_flex_data(ser):
    line = ser.readline().replace("\n\r", "")
    data = Data(list(np.fromstring(line, dtype=int, sep=" ")))
    return data.flex

def main():
    left_glove_ser = serial.serial.Serial(port=LEFT_GLOVE_PORT, baudrate=BAUDRATE, timeout=TIMEOUT)
    # rght_glove_ser = serial.serial.Serial(port=RGHT_GLOVE_PORT, baudrate=BAUDRATE, timeout=TIMEOUT)
    data_file = open("left_flex_data.txt", "w")

    try:
        while True:
            left_data = read_flex_data(left_glove_ser)
            # rght_data = read_flex_data(rght_glove_ser)
            data_file.write(OPEN + " " + " ".join(left_data) + "\n")
            time.sleep(0.25)

    except KeyboardInterrupt:
        data_file.close()

if __name__ == "__main__":
    main()
