import serial
from hid_codes import key_to_byte

class HID_BluePill(object):
    def __init__(self, port):
        self.port = port
        self.connect()

    def connect(self):
        self.ser = serial.Serial(self.port, 9600, timeout=0.5)

    def write(self, byte):
        if type(byte) == str:
            byte = byte.encode()
        self.ser.write(byte)

    def read(self):
        return self.ser.read().decode()

if __name__ == '__main__':
    hid = HID_BluePill("/dev/cu.HC-05-DevB")
    hid.write(key_to_byte(["KEY_H", "KEY_E", "KEY_L", "KEY_L", "KEY_O"]))
    hid.write(key_to_byte(["KEY_SPACE"]))
    hid.write(key_to_byte(["KEY_W", "KEY_O", "KEY_R", "KEY_L", "KEY_D"]))
    hid.write(key_to_byte(["MOVE_MOUSE_X_L"]))

