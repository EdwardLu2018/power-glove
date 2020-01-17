
def detectSwipe(orient, velx, vely, velz, serial, right):
    if not right:
         #swipe down
        if (vely > 400): #and (orient == 0 or orient == 6) ):
            return "SWIPE DOWN"
        elif(vely < -1500): #and (orient == 1 or orient == 7)):
            return "SWIPE UP"
    else:
        #swipe down
        if (vely < -400): #and (orient == 0 or orient == 6) ):
            return "SWIPE DOWN"
        elif(vely > 1500): #and (orient == 1 or orient == 7)):
            return "SWIPE UP"

def detectLRSwipe(orient, velx, vely, velz, serial):
    if (velz > 1500):
        return "SWIPE RIGHT"
    elif (velz < -1500):
        return "SWIPE LEFT"
