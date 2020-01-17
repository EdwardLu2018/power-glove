def detectSwipe(orient, velx, vely, velz, serial):
     #swipe down
    if (vely > 400): #and (orient == 0 or orient == 6) ):

        return "palm leftm DOWN"
    elif(vely < -1500): #and (orient == 1 or orient == 7)):

        return "palm right,UP "

def detectLRSwipe(orient, velx, vely, velz, serial):
    if (velz > 1500):

        return "palm up, RIGHT"

    elif (velz<-1500):
        return "palm down, LEFT"
