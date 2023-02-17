from machine import PWM
from .smooth_servo_simple import ServoSmoothBase


class ServoPDM360:
    """Servo class for pulse density modulation continuous rotation servos"""
    DIRECTION_CCV = -1
    DIRECTION_CV = 1
    DIRECTION_STOP = 0

    def __init__(self, pwm: PWM, min_us=1000, max_us=9000, dead_zone_us=300, freq=50, invert=False):
        self.pwm = pwm
        self.pwm.freq(freq)
        self._low_duty_part = self.__get_low_duty_part(dead_zone_us, min_us, max_us)
        self._hi_duty_part = self.__get_hi_duty_part(dead_zone_us, min_us, max_us)
        self._invert = invert
        self._curr_duty = 0
        self._force = 100
        self._curr_dir = 0
        self._move_period_ms = 1000 // freq

    def __delete__(self, instance):
        self.deinit()

    def set_duty(self, duty: int):
        self._curr_duty = duty
        self.pwm.duty_u16(duty)

    def turn_ccv(self, force: int = None):
        self._curr_dir = self.DIRECTION_CCV
        if force is None:
            force = self._force
        else:
            force = self.__normalize_force(force)

        self._force = force

        if self._invert:
            self.set_duty(self.__get_duty(force, self._low_duty_part))
        else:
            self.set_duty(self.__get_duty(force, self._hi_duty_part))

    def turn_cv(self, force: int = None):
        self._curr_dir = self.DIRECTION_CV
        if force is None:
            force = self._force
        else:
            force = self.__normalize_force(force)

        self._force = force

        if self._invert:
            self.set_duty(self.__get_duty(force, self._hi_duty_part))
        else:
            self.set_duty(self.__get_duty(force, self._low_duty_part))

    def stop(self):
        self._stop()

    def deinit(self):
        self.pwm.deinit()

    def _stop(self):
        self._curr_dir = self.DIRECTION_STOP
        self.set_duty(0)

    async def _turn_gen(self, direction: int, time_ms: int = 0, force: int = None,
                        start_smoothing: ServoSmoothBase = None, end_smoothing: ServoSmoothBase = None):
        _move_period_ms = self._move_period_ms
        if start_smoothing is not None:
            self.validate_smooth(start_smoothing)
            if force is None:
                force = start_smoothing._value
            else:
                start_smoothing._value = force

        if force is None:
            force = 50

        if end_smoothing is not None:
            self.validate_smooth(end_smoothing)

        # start
        if direction != self.DIRECTION_STOP:
            _t_fn = self.turn_ccv if direction == self.DIRECTION_CCV else self.turn_cv
            if start_smoothing is not None:
                for force in start_smoothing.generate(_move_period_ms):
                    _t_fn(force)
                    yield _move_period_ms
            else:
                _t_fn(force)

        # move
        if time_ms <= 0 and direction != self.DIRECTION_STOP:
            # no need to stop
            return

        yield time_ms

        # stop
        if end_smoothing is not None:
            _de_func = self.turn_ccv if self._curr_dir == self.DIRECTION_CCV else self.turn_cv
            _init_force = self._force
            end_smoothing._value = _init_force
            for force in end_smoothing.generate(_move_period_ms):
                _de_func(_init_force - force)
                yield _move_period_ms

        self._stop()

    @staticmethod
    def validate_smooth(smooth: object):
        if not callable(getattr(smooth, 'generate')):
            raise TypeError('Smooth must have generate method')

    @staticmethod
    def __get_low_duty_part(ded_zone: int, min_duty: int, max_duty: int) -> (int, int):
        return int(min_duty + ((max_duty - min_duty) // 2) - (ded_zone // 2)), min_duty

    @staticmethod
    def __get_hi_duty_part(ded_zone: int, min_duty: int, max_duty: int) -> (int, int):
        return int(max_duty - ((max_duty - min_duty) // 2) + (ded_zone // 2)), max_duty

    @staticmethod
    def __get_duty(force: int, duty_part: (int, int)) -> int:
        if duty_part[1] > duty_part[0]:
            return int(duty_part[0] + (duty_part[1] - duty_part[0]) * (force / 100))
        else:
            return int(duty_part[0] - (duty_part[0] - duty_part[1]) * (force / 100))

    @staticmethod
    def __normalize_force(force: int) -> int:
        if force > 100:
            return 100
        if force < 0:
            return 0

        return int(force)

    @staticmethod
    def __normalize_duty(duty: int, min_duty: int, max_duty: int) -> int:
        if duty > max_duty:
            return max_duty
        if duty < min_duty:
            return min_duty
        return int(duty)
