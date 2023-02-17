from machine import Pin, PWM
from micropython_servo_pdm_360 import ServoPDM360RP2Irq, SmoothLinear
import utime


servo_pwm = PWM(Pin(21))

# create a servo object
servo = ServoPDM360RP2Irq(pwm=servo_pwm, min_us=1350, max_us=8450, freq=50)


def main():
    # turn clockwise with a force of 30 for 2 seconds
    servo.turn_cv_ms(2000, 30)

    # wait 3 seconds
    utime.sleep(3)

    # turn clockwise with a force of 50 with a smoothing at the beginning 2 seconds
    servo.turn_cv_ms(force=50, start_smoothing=SmoothLinear(50, 2000))

    # wait 5 seconds
    utime.sleep(5)

    # smoothly stop the servo
    servo.stop_smooth(end_smoothing=SmoothLinear(50, 500))

    # wait 3 seconds
    utime.sleep(3)

    # turn counter-clockwise with a force of 100 for 2 seconds with a smoothing at the start and at the end
    servo.turn_ccv_ms(2000, 100, start_smoothing=SmoothLinear(50, 1000), end_smoothing=SmoothLinear(50, 500))

    # wait 5 seconds
    utime.sleep(5)


try:
    main()
except KeyboardInterrupt:
    print("KeyboardInterrupt")
finally:
    servo.deinit()
