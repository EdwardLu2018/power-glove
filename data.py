import serial, time

# data = [left pinky, ..., left thumb, flex, touch, x, y, z, orientation]

class Data(object):
    def __init__(self, data=[0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0, 0]):
        self.data = data
        #flex
        self.pinky = data[0]
        self.ring = data[1]
        self.middle = data[2]
        self.index = data[3]
        self.thumb = data[4]
        #touch
        self.pinkyTouch = data[5]
        self.ringTouch = data[6]
        self.middleTouch = data[7]
        self.indexTouch = data[8]
        self.thumbTouch = data[9]
        #orientation
        self.x = data[10]
        self.y = data[11]
        self.z = data[12]
        self.orientation = data[13]
        self.mode = data[14]    #0 = mouse mode, 1 = keyboard, 2 = gestures


    def __repr__(self):
        #res = "Left Pinky Resistance: " + self.pinkyL
        return str(self.data)

    
    def flex_data(self):
        return self.data[:5]

    def update(self, data):
        self.__init__(data)

