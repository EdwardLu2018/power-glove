import serial, time

# data = [left pinky, ..., left thumb, flex, touch, x, y, z, orientation]

class Data(object):
    def __init__(self, data=[0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 0]):
        self.data = data
        self.pinkyL = data[0]
        self.ringL = data[1]
        self.middleL = data[2]
        self.indexL = data[3]
        self.thumbL = data[4]
        self.thumbR = data[5]
        self.indexR = data[6]
        self.middleR = data[7]
        self.ringR = data[8]
        self.pinkyR = data[9]
        self.xL = data[10]
        self.yL = data[11]
        self.zL = data[12]
        self.xR = data[13]
        self.yR = data[14]
        self.zR = data[15]


    def __repr__(self):
        #res = "Left Pinky Resistance: " + self.pinkyL
        return str(self.data)


    def update(self, data):
        self.__init__(data)
