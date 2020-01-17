def detectSwipe(orient, velx, vely, velz, serial):
     #swipe down
    if (velz > 1500 and vely > -50 and vely <50 and velx > -50 and velx <50 ): #and (orient == 0 or orient == 6) ):

        return "palm leftm DOWN"
    elif(velz < -400 and vely > -50 and vely <50 and velx > -50 and velx <50 ): #and (orient == 1 or orient == 7)):

        return "palm right,UP "

def detectLRSwipe(orient, velx, vely, velz, serial):
    if (velz > 1500 and vely < - 900):
      
        return "palm up, RIGHT"
        
    elif (velz<-1500 and vely < -900 ):
        return "palm down, LEFT"