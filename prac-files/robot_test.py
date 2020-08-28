import brickpi3
import math
BP = brickpi3.BrickPi3()

try:
    while(True):
        BP.set_motor_dps(BP.PORT_B, 360)
        BP.set_motor_dps(BP.PORT_C, 360)

except KeyboardInterrupt:
    BP.reset_all()
