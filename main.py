import data
import serial

left_glove = data.Data()
right_glove = data.Data()

left_serial = serial.Serial('/dev/ttyACM0', 9600)
right_serial = serial.Serial('/dev/ttyACM1', 9600)

previous_left_action = 0         #prevents rapid unwanted repeated action
previous_right_action = 0

while True:
    global previous_left_action
    global previous_right_action

    #read data from serial port
    left_serial_data = left_serial.readline().decode('utf-8')   
    right_serial_data = right_serial.readline().decode('utf-8')
    left_line = left_serial_data.replace("\n\r", "")
    right_line = right_serial_data.replace("\n\r", "")
    left_data = list(map(int, left_line.split(' ')))  #string to int list
    right_data = list(map(int, right_line.split(' ')))

    #updating glove objects
    left_glove.update(left_data)
    right_glove.updata(right_data)

    #calling respective actions
    left_action = data.call_left_action(left_glove)
    right_action = data.call_right_action(right_glove)
    
    #prevents unwanted rapid repeated action
    if previous_left_action != 0 and left_action == previous_left_action:
        time.sleep(.5)
        left_action = 0

    if previous_right_action != 0 AND right_action == previous_right_action:
        time.sleep(.5)
        right_action = 0
    
    #sends actions to arduino (prioritizes left action)
    new_data = right_action if left_action == None else left_action
    SendSerial = serial.Serial('/dev/ttyTHS1', 9600)
    SendSerial.write(new_data.encode())
    

