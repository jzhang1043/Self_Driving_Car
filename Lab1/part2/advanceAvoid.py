import picar_4wd as fc
import numpy as np
import operator as op
from bresenham import bresenham
import time

class Picar():
    def __init__(self):
        self.power = 1 # car power
        self.size = 30 # car length and width (cm)
        self.distance = 0 # relative car travelled distance in cm

    
    def move(self,dir):
        # car moving function
        if dir == 'f':
            fc.forward(self.power)
        elif dir == 'b':
            fc.backward(self.power)
        elif dir == 'l': 
            fc.turn_left(self.power)
            time.sleep(0.75) # 90 degrees left
            fc.stop()
        elif dir == 'r':
            fc.turn_right(self.power)
            time.sleep(0.75) # 90 degrees right
            fc.stop()
        else:
            fc.stop()
    
    def start_speed_timer(self):
        # start speed timer
        fc.start_speed_thread()

    def end_speed_timer(self):
        # end speed timer
        fc.end_speed_thread()

    def getSpeed(self):
        # get car speed in (cm/s)
        return fc.speed_val()

    def getDistance(self,time,speed):
        # get car travelled distance
        self.distance = time * speed
        return self.distance
    
    def object_dist_list(self):
        # get distance of objects using ultrasonic sensor for 180 degree
        ret = []
        fc.servo.set_angle(90)
        time.sleep(0.8)
        for i in range(180,-1, -10):
            ret += [round(fc.get_distance_at(i-90))]
            time.sleep(0.02)
        return ret
    

class Map():
    def __init__(self):
        self.map = np.zeros(shape=(20,20), dtype=int) # init map
        self.mapLen = len(self.map) # map length
        self.carLocation = (9,9) # car location (ultrasonic sensor location)
        self.carDir = 'N' # car direction

    def getCarLocation(self):
        # get car position
        return self.carLocation
    
    def setCarLocation(self, p):
        # set car position
        self.carLocation = p

    def setCarDir(self,dir):
        self.carDir = dir

    def updateMap(self,coor,tag):
        # update the map 
        # coor: coordiante to be updated
        # tag: the place holder, int
        x,y = coor
        if x < 0 or y < 0 or x >= self.mapLen or y >= self.mapLen:
            return -1
        else:
            self.map[self.mapLen - 1 - y][x] = tag

    def getObjPoints(self, distlist):
        # get object's location using list of distance from Picar().object_dist_list()
        upperThreshold = 35
        lowerThreshold = 0
        stepangle = np.pi / 18
        currangle = np.pi
        ret = []
        for i in range(len(distlist)):
            dist = distlist[i]
            if dist < lowerThreshold or dist > upperThreshold:
                continue
            else:
                dx = round(np.cos(currangle - i * stepangle) * dist)
                dy = round(np.sin(currangle - i * stepangle) * dist)
                if self.carDir == 'N':
                    ret += [tuple(map(op.add, self.carLocation, (dx,dy)))]
                elif self.carDir == 'S':
                    ret += [tuple(map(op.add, self.carLocation, (-dx,-dy)))]
                elif self.carDir == 'W':
                    ret += [tuple(map(op.add, self.carLocation, (-dy,dx)))]
                elif self.carDir == 'E':
                    ret += [tuple(map(op.add, self.carLocation, (dy,-dx)))]
        return ret

    def rasterization(self,points):
        # rasterize two adjcent points and return a list of rasterized points.
        ret = []
        x0,y0 = points[0]
        for i in range(1,len(points)):
            x1,y1 = points[i]
            ret += list(bresenham(x0, y0, x1, y1))
            x0,y0 = points[i]
        return ret


###################################################
def main():
    mymap.setCarDir("N")
    mycar.start_speed_timer()
    mymap.updateMap(mymap.getCarLocation(),6)

    distList = mycar.object_dist_list()
    points = mymap.getObjPoints(distList)
    newpoints = mymap.rasterization(points)
    for ele in newpoints:
        mymap.updateMap(ele,2)
    print(mymap.map)
    

    print(distList)
    # print(mymap.map)


    # while 1:
    #     continue

if __name__ == '__main__':
    try:
        mycar = Picar()
        mymap = Map()
        main()
        mycar.end_speed_timer()

    except KeyboardInterrupt:
        mycar.end_speed_timer()
        fc.stop()
        
        print(' ---quit')
