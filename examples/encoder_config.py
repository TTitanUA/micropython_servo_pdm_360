import uasyncio as asyncio
from micropython_rotary_encoder import RotaryEncoderRP2, RotaryEncoderEvent
from machine import Pin, PWM
from micropython_servo_pdm_360 import ServoPDM360

# This is an example of finding pulse time settings for your servo on raspberry pi pico using encoder.
# Connect the servo signal wire to GPIO21 on the Pico.
# Connect encoder contacts: clk - GPIO15, dt - GPIO9
# Connect pico to your computer via USB.
# Open the serial monitor in Thonny IDE.
# Create a new file and paste the code from this file to it.
# Set `freq` to the frequency of your servo.
# Run the code.
# Rotate the encoder. And record values when the servo starts to move, stop, start to move in the opposite direction and stop.



servo_pwm = PWM(Pin(21))
freq = 50
min_us = 0
max_us = (1000 / freq) * 1000
iteration_time_ms = 500
step_us = 50
duty = 0

# create a servo object
servo = ServoPDM360(pwm=servo_pwm, min_us=min_us, max_us=max_us, freq=freq)

# Create the encoder object
en_pin_clk = Pin(15, Pin.IN, Pin.PULL_UP)
en_pin_dt = Pin(9, Pin.IN, Pin.PULL_UP)

# Create the rotary encoder object
encoder = RotaryEncoderRP2(
    pin_clk=en_pin_clk,
    pin_dt=en_pin_dt,
)


def turn_left_listener(fast: bool = False):
    global duty
    duty -= step_us if not fast else step_us * 10
    print(f"duty: {duty}")
    servo.set_duty(duty)


def turn_right_listener(fast: bool = False):
    global duty
    duty += step_us if not fast else step_us * 10
    print(f"duty: {duty}")
    servo.set_duty(duty)


encoder.on(RotaryEncoderEvent.TURN_LEFT, lambda: turn_left_listener())
encoder.on(RotaryEncoderEvent.TURN_LEFT_FAST, lambda: turn_left_listener(True))

encoder.on(RotaryEncoderEvent.TURN_RIGHT, lambda: turn_right_listener())
encoder.on(RotaryEncoderEvent.TURN_RIGHT_FAST, lambda: turn_right_listener(True))

try:
    asyncio.run(encoder.async_tick())
except KeyboardInterrupt:
    print("KeyboardInterrupt")
finally:
    servo.deinit()

