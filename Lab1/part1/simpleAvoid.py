import picar_4wd as fc
import random
import time


power = 30

def main():
    while True:
        scan = fc.scan_step(30)
        if not scan:
            continue
        # status is 108 degree in front of the car
        status = scan[2:8]
        # print(status)  
        if status != [2,2,2,2,2,2]:
            fc.backward(power)
            fc.get_distance_at(0)
            time.sleep(0.3)
            
            k = random.randint(0, 1)
            if k == 0:
                fc.turn_left(power)           
            else:
                fc.turn_right(power)
        else:
            fc.forward(power)
        

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        fc.stop()
        print(" ----quit")