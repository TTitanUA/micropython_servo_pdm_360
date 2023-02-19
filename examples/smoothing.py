from machine import Pin, PWM
from micropython_servo_pdm_360 import ServoPDM360RP2Async
from smooth_servo import SmoothLinear, SmoothEaseIn, SmoothEaseOut, SmoothEaseInQuad, \
    SmoothEaseOutQuad, SmoothEaseInOutQuad, SmoothEaseInCubic, SmoothEaseOutCubic, SmoothEaseInOutCubic, \
    SmoothEaseInQuart, SmoothEaseOutQuart, SmoothEaseInOutQuart, SmoothEaseInQuint, SmoothEaseOutQuint, \
    SmoothEaseInOutQuint, SmoothEaseInExpo, SmoothEaseOutExpo, SmoothEaseInOutExpo, SmoothEaseInCirc, \
    SmoothEaseOutCirc, SmoothEaseInOutCirc, SmoothEaseInBack, SmoothEaseOutBack, SmoothEaseInOutBack, SmoothEaseInOut
import uasyncio as asyncio

servo_pwm = PWM(Pin(21))

# Set the parameters of the servo pulses, more details in the "Documentation" section
freq = 50
min_us = 400
max_us = 2550
dead_zone_us = 150

# create a servo object
servo = ServoPDM360RP2Async(pwm=servo_pwm, min_us=min_us, max_us=max_us, dead_zone_us=dead_zone_us, freq=freq)

# It is possible to use the following smooth variations:
smooth_variations = [
    SmoothLinear,
    SmoothEaseIn,
    SmoothEaseOut,
    SmoothEaseInOut,
    SmoothEaseInQuad,
    SmoothEaseOutQuad,
    SmoothEaseInOutQuad,
    SmoothEaseInCubic,
    SmoothEaseOutCubic,
    SmoothEaseInOutCubic,
    SmoothEaseInQuart,
    SmoothEaseOutQuart,
    SmoothEaseInOutQuart,
    SmoothEaseInQuint,
    SmoothEaseOutQuint,
    SmoothEaseInOutQuint,
    SmoothEaseInExpo,
    SmoothEaseOutExpo,
    SmoothEaseInOutExpo,
    SmoothEaseInCirc,
    SmoothEaseOutCirc,
    SmoothEaseInOutCirc,
    SmoothEaseInBack,
    SmoothEaseOutBack,
    SmoothEaseInOutBack,
]

force = 60
duration = 2000
start_smooth_duration = 2000
end_smooth_duration = 2000
sleep = 2000


async def main():
    for smooth in smooth_variations:
        print(
            f"Smooth: {smooth.__name__}, force: {force}, duration: {duration}, end_smooth_duration: {end_smooth_duration}, sleep: {sleep}")
        print(f"Starting. start_smooth_duration: {start_smooth_duration}, duration: {duration}")
        servo.turn_cv_ms(0, force, start_smoothing=smooth(100, start_smooth_duration))

        await asyncio.sleep_ms(duration + start_smooth_duration)

        print(f"Stop. end_smooth_duration: {end_smooth_duration}")
        servo.stop_smooth(end_smoothing=smooth(100, end_smooth_duration))

        await asyncio.sleep_ms(end_smooth_duration + sleep)
        print("")


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("KeyboardInterrupt")
finally:
    servo.stop()

