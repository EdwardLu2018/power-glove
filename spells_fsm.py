import time

class OpenChromeFSM(object):
    def __init__():
        self.idle = 0
        self.ok = 1
        self.open = 2
        self.gun = 3
        self.curr_state = self.idle
        self.clk_ticks = time.clock()

    def update(self, data, pose, clf):
        print(self.curr_state)
        if self.curr_state == self.idle:
            if pose == clf.OK:
                self.curr_state = self.ok
            elif time.clock() - self.clk_ticks > 1.0:
                self.curr_state = self.idle
            else:
                self.curr_state = self.idle
            return False

        elif self.curr_state == self.ok:
            if pose == clf.OPEN:
                self.curr_state = self.gun
            elif time.clock() - self.clk_ticks > 1.0:
                self.curr_state = self.idle
            else:
                self.curr_state = self.idle
            return False

        elif self.curr_state == self.open:
            if pose == clf.OK:
                self.curr_state = self.ok
            elif time.clock() - self.clk_ticks > 1.0:
                self.curr_state = self.idle
            else:
                self.curr_state = self.idle
            return False

        elif self.curr_state == self.gun:
            self.curr_state = self.idle
            self.clk_ticks = time.clock()
            return True
