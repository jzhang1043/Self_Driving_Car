import picar_4wd as fc
import numpy as np
import time

class Picar():
    def __init__(self):
        self.power = 30 # car power
        self.size = 30 # car length and width (cm)
        self.position = (0,0) # car position

    # dir: 'l' for left, 'r' for right, 'f' for forward, 'b' for backward
    def move(self,dir):
        if dir == 'f':
            fc.forward(self.power)
        elif dir == 'b':
            fc.backward(self.power)
        elif dir == 'l':
            fc.turn_left(self.power)
            time.sleep(0.75)
            fc.stop()
        elif dir == 'r':
            fc.turn_right(self.power)
            time.sleep(0.75)
            fc.stop()
        else:
            fc.stop()

class Map():
    def __init__(self):
        self.map = np.zeros(shape=(600,600), dtype=int)



if __name__ == '__main__':
    try:
        mycar = Picar()
        mycar.move("")
    except KeyboardInterrupt:
        fc.stop()
        print('\n system stopped')
