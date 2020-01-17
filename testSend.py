import data
import serial
import time
import actions
right_glove = data.Data()

right_serial = serial.Serial('/dev/ttyACM0', 9600)

time.sleep(3)
previous_action = None
counter = 0
while True:
    if counter > 0:
        counter += 1
        right_serial_data = right_serial.readline().decode('utf-8')
        right_line = right_serial_data.replace("\n\r", "")
        right_data = list(map(int, right_line.split(' '))) + [1]
        right_glove.update(right_data)
        if counter == 10:
            counter = 0
            right_action = None
        continue
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
        counter = 1
        previous_action = None
        right_action = None
        continue
    elif right_action != None:
        print(right_action, chr(right_action)) 
        print("Mode: ", right_glove.mode)

    
    #sends actions to arduino (prioritizes left action)
        SendSerial = serial.Serial('/dev/ttyTHS1', 9600)
        SendSerial.write(chr(right_action).encode())
        previous_action = right_action

