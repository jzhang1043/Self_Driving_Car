import picar_4wd as fc
import random
import time

# power of the car
power = 30

def main():
    # While the script is running, auto detect objects in front, move forward or
    # randomly pick a left/right direction to move forward.
    
    while True:
        # scan_step max angle is set to 150 degree;
        # send ultrasonic wave every 30 degree and return 0, 1, or 2 after a 150 degree scan
        # if 150 degree scan is not finished, return false
        scan = fc.scan_step(30)
        if not scan:
            continue

        # object is not detected if scan contains only 2s.
        if scan != [2,2,2,2,2]:
            # move backward for 0.2 second
            fc.backward(power)
            time.sleep(0.2)

            # randomly change direction until object is not detected.
            n = random.randint(0, 1)
            fc.turn_left(power) if n == 0 else fc.turn_right(power)

        else:
            # move forward
            fc.forward(power)
        

# execute when simpleAvoid.py is called.
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        fc.stop()
        print(" ----quit")