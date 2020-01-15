from data import Data
import serial
import numpy as np
import pickle
import time

LEFT_GLOVE_PORT = ""
RGHT_GLOVE_PORT = ""
BAUDRATE = 9600
TIMEOUT = 1

CLASS = 0

def read_flex_data(ser):
    line = ser.readline().replace("\n\r", "")
    data = list(np.fromstring(line, dtype=int, sep=" "))
    return data.flex

def main():
    left_glove_ser = serial.serial.Serial(port=LEFT_GLOVE_PORT, baudrate=BAUDRATE, timeout=TIMEOUT)
    # rght_glove_ser = serial.serial.Serial(port=RGHT_GLOVE_PORT, baudrate=BAUDRATE, timeout=TIMEOUT)
    data_file = open("left_flex_data.txt", "a")

    try:
        while True:
            left_data = read_flex_data(left_glove_ser)
            # rght_data = read_flex_data(rght_glove_ser)

            data_file.write(CLASS + " " + " ".join(left_data) + "\n")
    except KeyboardInterrupt:
        data_file.close()

if __name__ == "__main__":
    main()
