
# This is a simple version of the smooth_servo module. It only contains the base class and the line transition.
try:
    from smooth_servo import ServoSmoothBase, SmoothLinear
except Exception as e:
    class ServoSmoothBase:
        def __init__(self, value: int, time_ms: int, start_value: int = 0):
            self._value = self.__normalize_value(value)
            self._time_ms = self.__normalize_time(time_ms)
            self._start_value = self.__normalize_start_value(value, start_value)

        def generate(self, tick_t_ms: int):
            yield 0

        @staticmethod
        def __normalize_start_value(value, s_v):
            return 0 if s_v < 0 or s_v > value else s_v

        @staticmethod
        def __normalize_value(value):
            if value <= 0:
                raise TypeError('Value must be greater than 0')
            return int(value)

        @staticmethod
        def __normalize_time(value):
            if value <= 0:
                raise TypeError('Time must be greater than 0')
            return int(value)


    class SmoothLinear(ServoSmoothBase):
        def generate(self, tick_t_ms: int):
            _t_ms = self._time_ms
            _s_v = self._start_value
            _v = self._value - _s_v
            _e_v = self._value

            _ss = (_t_ms // tick_t_ms)
            _s = _v / _ss

            for i in range(1, _ss):
                yield int(_s_v + _s * i)
            yield _e_v
