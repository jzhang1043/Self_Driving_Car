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
        self.map = Map()

    
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
            self.map.updateCarDir('l')
        elif dir == 'r':
            fc.turn_right(self.power)
            time.sleep(0.75) # 90 degrees right
            fc.stop()
            self.map.updateCarDir('r')
        else:
            fc.stop()
        return
    
    def start_speed_timer(self):
        # start speed timer
        fc.start_speed_thread()
        return

    def end_speed_timer(self):
        # end speed timer
        fc.end_speed_thread()
        return

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
        self.map = np.ones(shape=(40,40), dtype=int) # init map
        self.mapLen = len(self.map) # map length
        self.carLocation = (20,20) # car location (ultrasonic sensor location)
        self.carDir = 'N' # car direction

    def getCarLocation(self):
        # get car position
        return self.carLocation
    
    def setCarLocation(self, p):
        # set car position
        self.carLocation = p
        return

    def updateCarDir(self,turn):
        if turn == 'l':
            if self.carDir == 'N':
                self.carDir = 'W'
            elif self.carDir == 'W':
                self.carDir = 'S'
            elif self.carDir == 'S':
                self.carDir == 'E'
            elif self.carDir == 'E':
                self.carDir == 'N'
        elif turn == 'r':
            if self.carDir == 'N':
                self.carDir = 'E'
            elif self.carDir == 'E':
                self.carDir = 'S'
            elif self.carDir == 'S':
                self.carDir == 'W'
            elif self.carDir == 'W':
                self.carDir == 'N'
                

    def updateMap(self,coor,tag):
        # update the map 
        # coor: coordiante to be updated
        # tag: the place holder, int
        x,y = coor
        if x < 0 or y < 0 or x >= self.mapLen or y >= self.mapLen:
            return -1
        if self.map[self.mapLen - 1 - y][x] != 0:
            self.map[self.mapLen - 1 - y][x] = tag
        return

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

    def drawmap(self):
        with open("map.csv",'w') as file:
            for i in self.map:
                for j in i:
                    file.write(str(j) + " ")
                file.write('\n')
        return

###################################################
def main():
    # init
    mymap.setCarDir("N")
    mycar.start_speed_timer()

    # test
    # mymap.updateMap(mymap.getCarLocation(),5)
    # distList = mycar.object_dist_list()
    # rastP = mymap.rasterization(mymap.getObjPoints(distList))
    # for p in rastP:
    #     mymap.updateMap(p,0)
    # print(distList)
    # mymap.drawmap()

    # mycar.move('f')
    # timeout = 1 # sec
    # timeout_start = time.time()
    # while time.time() < timeout_start + timeout:
    #     print(mycar.getSpeed())
    #     print(time.time() - timeout_start) 
    #     time.sleep(0.1)
    # mycar.move('')

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
