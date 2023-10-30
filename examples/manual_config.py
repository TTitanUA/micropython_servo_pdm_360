import utime
from machine import Pin, PWM
from micropython_servo_pdm_360 import ServoPDM360

# This is an example of finding pulse time settings for your servo on raspberry pi pico.
# Connect the servo signal wire to GPIO21 on the Pico.
# Connect pico to your computer via USB.
# Open the serial monitor in Thonny IDE.
# Create a new file and paste the code from this file to it.
# Set `freq` to the frequency of your servo.
# Run the code.
# Listen to the serial monitor. And record values when the servo starts to move, stop, start to move in the opposite direction and stop.
# You can change the `iteration_time_ms` to make the process faster or slower.
# By changing the values of `min_us`, `max_us` and `step_us` you can limit the search area and change the search step.



servo_pwm = PWM(Pin(21))
freq = 50
min_us = 0
max_us = int((1000 / freq) * 1000)
iteration_time_ms = 500
step_us = 50

# create a servo object
servo = ServoPDM360(pwm=servo_pwm, min_us=min_us, max_us=max_us, freq=freq)


def loop():
    print("The enumeration of pulse length values will now begin.")
    utime.sleep(1)
    for i in range(min_us, max_us, step_us):
        print('')
        print(f'duty: {i}')
        servo.set_duty(i)
        utime.sleep_ms(iteration_time_ms)


try:
    loop()
except KeyboardInterrupt:
    print("KeyboardInterrupt")
finally:
    servo.deinit()


