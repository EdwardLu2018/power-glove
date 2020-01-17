import time

class OpenChromeFSM(object):
    def __init__(self):
        self.idle = 0
        self.ok = 1
        self.curr_state = 0

    def update(self, data, pose, clf):
        print(pose, self.curr_state)
        if self.curr_state == self.idle:
            if pose == clf.OK:
                self.curr_state = self.ok
                return True
            else:
                self.curr_state = self.idle
                return False
        elif self.curr_state == self.ok:
            if pose == clf.OK:
                self.curr_state = self.ok
            else:
                self.curr_state = self.idle
            return False

class CloseWindowFSM(object):
    def __init__(self):
        self.idle = 0
        self.gun = 1
        self.curr_state = 0

    def update(self, data, pose, clf):
        print(pose, self.curr_state)
        if self.curr_state == self.idle:
            if pose == clf.GUN:
                self.curr_state = self.gun
                return True
            else:
                self.curr_state = self.idle
                return False
        elif self.curr_state == self.gun:
            if pose == clf.GUN:
                self.curr_state = self.gun
            else:
                self.curr_state = self.idle
            return False

class MinimizeFSM(object):
    def __init__(self):
        self.idle = 0
        self.middle = 1
        self.curr_state = 0

    def update(self, data, pose, clf):
        print(pose, self.curr_state)
        if self.curr_state == self.idle:
            if pose == clf.MIDDLE:
                self.curr_state = self.middle
                return True
            else:
                self.curr_state = self.idle
                return False
        elif self.curr_state == self.middle:
            if pose == clf.MIDDLE:
                self.curr_state = self.middle
            else:
                self.curr_state = self.idle
            return False

class FacetimeFSM(object):
    def __init__(self):
        self.idle = 0
        self.cali = 1
        self.curr_state = 0

    def update(self, data, pose, clf):
        print(pose, self.curr_state)
        if self.curr_state == self.idle:
            if pose == clf.CALI:
                self.curr_state = self.cali
                return True
            else:
                self.curr_state = self.idle
                return False
        elif self.curr_state == self.cali:
            if pose == clf.CALI:
                self.curr_state = self.cali
            else:
                self.curr_state = self.idle
            return False

class ITunesFSM(object):
    def __init__(self):
        self.idle = 0
        self.rock = 1
        self.curr_state = 0

    def update(self, data, pose, clf):
        print(pose, self.curr_state)
        if self.curr_state == self.idle:
            if pose == clf.ROCK:
                self.curr_state = self.rock
                return True
            else:
                self.curr_state = self.idle
                return False
        elif self.curr_state == self.rock:
            if pose == clf.ROCK:
                self.curr_state = self.rock
            else:
                self.curr_state = self.idle
            return False

class EnterFSM(object):
    def __init__(self):
        self.idle = 0
        self.thumb = 1
        self.curr_state = 0

    def update(self, data, pose, clf):
        print(pose, self.curr_state)
        if self.curr_state == self.idle:
            if pose == clf.THUMB:
                self.curr_state = self.thumb
                return True
            else:
                self.curr_state = self.idle
                return False
        elif self.curr_state == self.thumb:
            if pose == clf.THUMB:
                self.curr_state = self.thumb
            else:
                self.curr_state = self.idle
            return False

