import data
import serial
import actions
#left_glove = data.Data()
right_glove = data.Data()

#left_serial = serial.Serial('/dev/ttyACM0', 9600)
right_serial = serial.Serial('/dev/ttyACM1', 9600)


while True:
    try:
        right_serial_data = right_serial.readline().decode('utf-8')
        right_line = right_serial_data.replace("\n\r", "")
        right_data = list(map(int, right_line.split(' '))) + [1]
        right_glove.update(right_data)
    except:
        continue
    #updating glove objects


    #calling respective actions
    print(right_data)
    right_action = actions.call_right_action(right_glove)
    
    if right_action != None:    
        print(right_action, chr(right_action))
    #sends actions to arduino (prioritizes left action)
#    new_data = right_action if left_action == 0 else left_action
#    SendSerial = serial.Serial('/dev/ttyTHS1', 9600)
#    SendSerial.write(new_data.encode())
    

