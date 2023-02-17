from machine import PWM, Timer
from .smooth_servo_simple import ServoSmoothBase
from .servo_pdm_360 import ServoPDM360
import uasyncio as asyncio
import utime


class ServoPDM360RP2Async(ServoPDM360):
    """Wrapper for ServoPDM360 to add some async functionality to it, based on asyncio"""

    def __init__(self, pwm: PWM, min_us=1000, max_us=9000, dead_zone_us=300, freq=50, invert=False):
        super().__init__(pwm, min_us, max_us, dead_zone_us, freq, invert)
        self._task = None

    def turn_ccv_ms(self, time_ms: int = 0, force: int = None, start_smoothing: ServoSmoothBase = None, end_smoothing: ServoSmoothBase = None, callback: callable = None):
        if self._task is not None and not self._task.done():
            self._task.cancel()

        try:
            self._task = asyncio.create_task(
                self._turn_task(
                    self._turn_gen(self.DIRECTION_CCV, time_ms, force, start_smoothing, end_smoothing),
                    callback
                )
            )
        except asyncio.CancelledError:
            pass

    def turn_cv_ms(self, time_ms: int = 0, force: int = None, start_smoothing: ServoSmoothBase = None, end_smoothing: ServoSmoothBase = None, callback: callable = None):
        if self._task is not None and not self._task.done():
            self._task.cancel()

        try:
            self._task = asyncio.create_task(
                self._turn_task(
                    self._turn_gen(self.DIRECTION_CV, time_ms, force, start_smoothing, end_smoothing),
                    callback
                )
            )
        except asyncio.CancelledError:
            pass

    def stop_smooth(self, end_smoothing: ServoSmoothBase = None, callback: callable = None):
        if self._task is not None and not self._task.done():
            self._task.cancel()

        try:
            self._task = asyncio.create_task(
                self._turn_task(
                    self._turn_gen(self.DIRECTION_STOP, 0, None, None, end_smoothing),
                    callback
                )
            )
        except asyncio.CancelledError:
            pass

    def stop(self):
        if self._task is not None and not self._task.done():
            self._task.cancel()

        self._stop()

    async def _turn_task(self, generator, callback: callable = None):
        for sleep in generator:
            await asyncio.sleep_ms(sleep)

        self.__call_callback(callback)
        self._task = None

    def _stop(self):
        super()._stop()

    @staticmethod
    def __call_callback(callback: callable = None):
        if callback is not None and callable(callback):
            try:
                callback()
            except Exception as e:
                print('ServoPDM360RP2Irq error in callback', e)

    @staticmethod
    def __normalize_time(time):
        if time < 0:
            return 0
        return int(time)


class ServoPDM360RP2Irq(ServoPDM360):
    """Wrapper for ServoPDM360 to add some async functionality to it, based on irq timer"""

    __tick_execution_time = 0
    """ This is a crunch.  Without it, the acceleration and deceleration phase will take longer than indicated."""

    def __init__(self, pwm: PWM, min_us=1000, max_us=9000, dead_zone_us=300, freq=50, invert=False):
        super().__init__(pwm, min_us, max_us, dead_zone_us, freq, invert)
        __move_time = 1000 // freq
        self._continue_action_at = 0
        self._last_action_generator = None
        self._timer_period = __move_time
        self._timer = Timer(-1, mode=Timer.PERIODIC, period=__move_time, callback=self.__timer_tick)
        self.__tick_execution_time = __move_time
        self.__last_callback = None

    def turn_ccv_ms(self, time_ms: int = 0, force: int = None, start_smoothing: ServoSmoothBase = None, end_smoothing: ServoSmoothBase = None, callback: callable = None):
        self.__last_callback = callback
        self.__run_generator(self._turn_gen(self.DIRECTION_CCV, time_ms, force, start_smoothing, end_smoothing))

    def turn_cv_ms(self, time_ms: int = 0, force: int = None, start_smoothing: ServoSmoothBase = None, end_smoothing: ServoSmoothBase = None, callback: callable = None):
        self.__last_callback = callback
        self.__run_generator(self._turn_gen(self.DIRECTION_CV, time_ms, force, start_smoothing, end_smoothing))

    def stop_smooth(self, end_smoothing: ServoSmoothBase = None, callback: callable = None):
        self.__last_callback = callback
        self.__run_generator(self._turn_gen(self.DIRECTION_STOP, 0, None, None, end_smoothing))

    def stop(self):
        self._stop()

    def _stop(self):
        self._continue_action_at = 0
        self._last_action_generator = None
        super()._stop()

    def __run_generator(self, generator):
        self._last_action_generator = generator
        try:
            self._continue_action_at = next(self._last_action_generator) + utime.ticks_ms()
        except StopIteration:
            self._last_action_generator = None
            self.__call_callback()
        except Exception as e:
            print('ServoPDM360RP2Irq error in __run_generator', e)
            self.stop()

    def __call_callback(self):
        if self.__last_callback is not None and callable(self.__last_callback):
            _callback = self.__last_callback
            self.__last_callback = None
            try:
                _callback()
            except Exception as e:
                print('ServoPDM360RP2Irq error in callback', e)

    def __timer_tick(self, *args):
        if self._continue_action_at != 0:
            if utime.ticks_ms() >= self._continue_action_at:
                try:
                    if self._last_action_generator is not None:
                        self._continue_action_at = next(self._last_action_generator) - self.__tick_execution_time + utime.ticks_ms()
                except StopIteration:
                    self._last_action_generator = None
                    self.__call_callback()
                except Exception as e:
                    print('ServoPDM360RP2Irq error in timer tick', e)
                    self.stop()