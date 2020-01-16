import serial, time
import numpy as np
from data import Data

ser1 = serial.Serial('/dev/ttyACM2', 9600)
#ser2 = serial.Serial('/dev/ttyACM1', 9600)

OPEN = '0'
FIST = '1'


data_file = open("flex_data.txt", "a")

time.sleep(1)

for i in range(20):
    try:
        data1 = ser1.readline().decode('utf-8')
    except:
        print("failed serial")
        continue
    line = data1.replace("\r\n", "")
    #data = np.fromstring(line, dtype=int, sep=" ")
    print(line.split(" "))
    data = [int(s) for s in line.split(' ')]
    print(data)
    if len(data) < 14:
        print("no len")
        continue 
    flex_data = Data(list(data))
    #print(flex_data.flex_data())
    data_file.write(FIST + " " + " ".join([str(d) for d in flex_data.flex_data()]) + "\n")
    time.sleep(0.25)


