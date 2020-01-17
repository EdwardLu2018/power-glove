import data
import serial
import time
import actions
right_glove = data.Data()

right_serial = serial.Serial('/dev/ttyACM0', 9600)

time.sleep(3)
previous_action = None
while True:
    try:
        #read data from serial port
        right_serial_data = right_serial.readline().decode('utf-8')
        right_line = right_serial_data.replace("\n\r", "")
        right_data = list(map(int, right_line.split(' '))) + [1]
        #updating glove objects
        right_glove.update(right_data)
    except:
        continue

    #calling respective actions
    right_action = actions.call_right_action(right_glove)
    if previous_action != None and previous_action == right_action:
        time.sleep(.3)
        previous_action = None
        continue
    if right_action != None:
        print(right_action, chr(right_action)) 
        print("Mode: ", right_glove.mode)

    
    #sends actions to arduino (prioritizes left action)
        SendSerial = serial.Serial('/dev/ttyTHS1', 9600)
        SendSerial.write(chr(right_action).encode())
        previous_action = right_action

