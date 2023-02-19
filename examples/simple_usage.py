import utime
from machine import Pin, PWM
from micropython_servo_pdm_360 import ServoPDM360


# create a PWM servo controller (21 - pin Pico)
servo_pwm = PWM(Pin(21))

# Set the parameters of the servo pulses, more details in the "Documentation" section
freq = 50
min_us = 400
max_us = 2550
dead_zone_us = 150

# create a servo object
servo = ServoPDM360(pwm=servo_pwm, min_us=min_us, max_us=max_us, dead_zone_us=dead_zone_us, freq=freq)

# turn clockwise with a force of 30
servo.turn_cv(30)
utime.sleep(2)

# turn counter-clockwise with a force of 50
servo.turn_ccv(50)
utime.sleep(2)

# stop the servo
servo.stop()


# manually set the servo duty time
servo.set_duty(1400)
utime.sleep(1)

# deinit the servo
servo.deinit()
