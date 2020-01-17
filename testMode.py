import data
import serial
import time
import actions
import Jetson.GPIO as GPIO

right_glove = data.Data()
left_glove = data.Data()

right_serial = serial.Serial('/dev/ttyACM0', 9600)
left_serial = serial.Serial('/dev/ttyACM1', 9600)
time.sleep(3)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)
GPIO.output(31, GPIO.LOW)
GPIO.output(32, GPIO.LOW)
time.sleep(.5)


previous_action = None
counter = 0
mode = 0

while True:
    if counter > 0:
        counter += 1
        right_serial_data = right_serial.readline().decode('utf-8')
        right_line = right_serial_data.replace("\n\r", "")
        right_data = list(map(int, right_line.split(' '))) + [mode]
        left_serial_data = left_serial.readline().decode('utf-8')
        left_line = left_serial_data.replace("\n\r", "")
        left_data = list(map(int, left_line.split(' '))) + [mode]
        right_glove.update(right_data)
        left_glove.update(left_data)
        if counter == 10:
            counter = 0
            right_action = None
        continue
    try:

        #read data from serial port
        right_serial_data = right_serial.readline().decode('utf-8')
        right_line = right_serial_data.replace("\n\r", "")
        right_data = list(map(int, right_line.split(' '))) + [mode]
        left_serial_data = left_serial.readline().decode('utf-8')
        left_line = left_serial_data.replace("\n\r", "")
        left_data = list(map(int, left_line.split(' '))) + [mode]
        
        #updating glove objects
        right_glove.update(right_data)
        left_glove.update(left_data)
    except:
        continue

    #calling respective actions
    right_action = actions.call_right_action(right_glove)
    left_action = actions.call_left_action(left_glove)

    if previous_action != None and previous_action == right_action:
        counter = 1
        previous_action = None
        right_action = None
        continue
    elif right_action != None:
        if right_action == 100:     # changes mode
            print("CHANGED MODE", right_glove.mode)
            if right_glove.mode == 0:
                mode = 0
                print("Mouse Mode!")
                GPIO.output(32, GPIO.HIGH)
            elif right_glove.mode != 0:
                mode = right_glove.mode
                print("Not mouse mode")
                GPIO.output(32, GPIO.LOW)
            previous_action = 100
            continue 
        else:
            print(right_action)
            SendSerial = serial.Serial('/dev/ttyTHS1', 9600)
            SendSerial.write(chr(right_action).encode())
            previous_action = right_action

