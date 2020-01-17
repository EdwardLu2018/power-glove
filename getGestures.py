from swipeGestureFunctions import *

def getSwipeInfo(pose, data, count, tempcount, ser1, clf):
    velx_data = data.x
    vely_data = data.y
    velz_data = data.z
    orientation = data.orientation
    swipeType = detectSwipe(orientation, velx_data, vely_data, velz_data, ser1)
    swipevert = (detectSwipe(orientation, velx_data, vely_data, velz_data, ser1) != None)
    swipeside = (detectLRSwipe(orientation, velx_data, vely_data, velz_data, ser1) != None )
    if (tempcount < count - 10):
        #print((velx_data,vely_data, velz_data, orientation, detectSwipe(orientation, velx_data, vely_data, velz_data, ser1), detectLRSwipe(orientation, velx_data, vely_data, velz_data, ser1)))
        if (swipeside or swipevert) and not (swipeside and swipevert) and (pose == clf.NEUTRAL or pose == clf.OPEN):
            if (swipevert):
                print(detectSwipe(orientation, velx_data, vely_data, velz_data, ser1))
                swipeType = detectSwipe(orientation, velx_data, vely_data, velz_data, ser1)
            else:
                print(detectLRSwipe(orientation, velx_data, vely_data, velz_data, ser1))
                swipeType = detectLRSwipe(orientation, velx_data, vely_data, velz_data, ser1)
            tempcount = count

    return (swipeType, tempcount)

