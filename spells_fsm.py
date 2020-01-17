import time

class OpenChromeFSM(object):
    def __init__(self):
        self.idle = 0
        self.ok = 1
        self.open = 2
        self.gun = 3
        self.curr_state = self.idle
        self.clk_ticks = time.clock()

    def update(self, data, pose, clf):
        print(pose, self.curr_state)
        if self.curr_state == self.idle:
            if pose == clf.OK:
                self.curr_state = self.ok
                self.clk_ticks = time.clock()
            elif time.clock() - self.clk_ticks > 5.0:
                self.curr_state = self.idle
            else:
                self.curr_state = self.idle
            return False

        elif self.curr_state == self.ok:
            if pose == clf.OPEN or pose == clf.FOUR or pose == clf.NEUTRAL:
                self.curr_state = self.open
            elif time.clock() - self.clk_ticks > 5.0:
                self.curr_state = self.idle
            elif pose == clf.OK:
                self.curr_state = self.ok
            else:
                self.curr_state = self.idle
            return False

        elif self.curr_state == self.open:
            if pose == clf.GUN:
                self.curr_state = self.gun
            elif time.clock() - self.clk_ticks > 1.0:
                self.curr_state = self.idle
            elif pose == clf.OPEN:
                self.curr_state = self.open
            else:
                self.curr_state = self.idle
            return False

        elif self.curr_state == self.gun:
            print(23467890986567)
            self.curr_state = self.idle
            return True
