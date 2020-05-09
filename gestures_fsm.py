import time

class Gesture(object):
    def __init__ (self):
        self.idle = True
        self.state1 = False
        self.statefinal = False
    def update (self, data):
        pass
        
class Swiperight (Gesture):
    def __init__ (self):
        #three states going left
        super().__init__(self)
        self.state2 = False
    def update (self, data):
        if (idle):
            if ('up'):
                idle = False
                state1 = True
        if (state1 and 'right'):
                

velx = 0;
vely = 0;
velz = 0'

if velx && vely:
    print("Swipe Left");
elif velx && vely:
    print("Swipe Right");
elif velx && vely:
    print("Scroll Up");
elif velx && vely:
    print("Scroll Down");


        
        