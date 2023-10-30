[![pypi version shield](https://img.shields.io/pypi/v/micropython-servo-pdm-360)](https://pypi.org/project/micropython-servo-pdm-360/) 
[![pypi downloads per month shield](https://img.shields.io/pypi/dm/micropython-servo-pdm-360?color=brightgreen)](https://pypi.org/project/micropython-servo-pdm-360/)
# Servo PDM Continuous
Библиотека для управления сервоприводами постоянного вращения через интерфейс PWM микроконтроллера Raspberry Pi Pico на языке MicroPython.

Возможности библиотеки:
- Вращение с заданным усилием и направлением
- Вращение в течении указанного времени
- Возможность плавного старта и остановки 
- Возможность использования библиотеки [smooth-servo](https://pypi.org/project/smooth-servo/) для изменения алгоритма плавного старта и остановки
- Вся отложенная работа происходит в фоновом режиме, с двумя вариантами обработки:
    - С помощью задачи asyncio (рекомендуется)
    - Таймером прерывания

Если вам не нужен весь перечисленный выше функционал, то вам стоит глянуть на библиотеку [micropython-servo](https://pypi.org/project/micropython-servo/).
Она гораздо меньше и для простых задач подходит лучше.

При разработке библиотеки использовались следующие материалы:
- Материал [Принцип работы сервоприводов постоянного вращения](http://wiki.amperka.ru/articles:servo-pdm-continuous-rotation), автор amperka.ru
- Материал [Servo Motor with Raspberry Pi Pico using MicroPython](https://microcontrollerslab.com/servo-motor-raspberry-pi-pico-micropython/), автор microcontrollerslab.com
- Материал [Hobby Servo Tutorial](https://learn.sparkfun.com/tutorials/hobby-servo-tutorial?_ga=2.2724022.723022425.1676642363-1173110823.1674579241), автор MIKEGRUSIN and BYRON J. (sparkfun.com)

### Совместимость
- MicroPython 1.19.1
- Raspberry Pi Pico

На представленном выше оборудовании библиотека была протестирована и работает корректно.
Но с не большими костылями она может работать и на другом оборудовании.

### ВНИМАНИЕ
Вы используете данный модуль на свой страх и риск. 
Я новичок в программировании на MicroPython. Так что могут быть нюансы, которые я не учел.
Если вы заметили ошибку или у вас есть предложения по улучшению, то пишите в Issues.

## Содержание
- [Установка](https://github.com/TTitanUA/micropython_servo_pdm_360#install)
- [Инициализация](https://github.com/TTitanUA/micropython_servo_pdm_360#init)
- [Документация](https://github.com/TTitanUA/micropython_servo_pdm_360#doc)
- [Примеры](https://github.com/TTitanUA/micropython_servo_pdm_360/tree/main/examples)
- [Баги и обратная связь](https://github.com/TTitanUA/micropython_servo_pdm_360#feedback)

<a id="install"></a>
## Установка
- Библиотеку установить через pip (Thonny -> Manage Packages) по названию **micropython-servo-pdm-360** 
- Или ручная установка:
  - [Скачать библиотеку с GitHub](https://github.com/TTitanUA/micropython_servo_pdm_360) 
  - забрать папку **micropython_servo_pdm_continuous** из архива.
  - загрузить в корень микроконтроллера или в папку **lib**.

Если хотите поиграться с логикой библиотеки, то 2й вариант установки предпочтительнее. :)

<a id="init"></a>
## Инициализация
### Инициализация базовой библиотеки
```python
from machine import Pin, PWM
from micropython_servo_pdm_360 import ServoPDM360

# создаем PWM контроллер сервопривода (21 - пин Pico)
servo_pwm = PWM(Pin(21))

# Задаем параметры импульсов сервопривода, подробнее в секции "Документация"
freq = 50
min_us = 400
max_us = 2550
dead_zone_us = 150

# создаем объект сервопривода
servo = ServoPDM360(pwm=servo_pwm, min_us=min_us, max_us=max_us, dead_zone_us=dead_zone_us, freq=freq)
```
После этого вам будут доступны [базовые методы](https://github.com/TTitanUA/micropython_servo_pdm_360#doc_base) управления сервоприводом, которые не требуют отложенных задач.

Для доступа к дополнительным методам, которые требуют отложенного выполнения, вам нужно инициализировать один из дочерних классов. 
В зависимости от того какой из способов обработки отложенных задач вы предпочитаете:

#### С помощью библиотеки uasyncio
Это оптимальный вариант для большинства проектов.
```python
from machine import Pin, PWM
from micropython_servo_pdm_360 import ServoPDM360RP2Async

# создаем PWM контроллер сервопривода (21 - пин Pico)
servo_pwm = PWM(Pin(21))

# Задаем параметры импульсов сервопривода, подробнее в секции "Документация"
freq = 50
min_us = 400
max_us = 2550
dead_zone_us = 150

# создаем объект сервопривода
servo = ServoPDM360RP2Async(pwm=servo_pwm, min_us=min_us, max_us=max_us, dead_zone_us=dead_zone_us, freq=freq)
```

#### С помощью прерываний по таймеру
Подробнее про таймеры можно почитать [здесь](https://docs.micropython.org/en/latest/library/machine.Timer.html)
Для Raspberry Pi Pico [здесь](https://docs.micropython.org/en/latest/rp2/quickref.html#timers)
Будьте внимательны, хоть это и самый простой вариант, но он не оптимален.
Так как обработка событий сервопривода происходит в прерывании по таймеру, другие прерывания будут отложены.
```python
from machine import Pin, PWM
from micropython_servo_pdm_360 import ServoPDM360RP2Irq

# создаем PWM контроллер сервопривода (21 - пин Pico)
servo_pwm = PWM(Pin(21))

# Задаем параметры импульсов сервопривода, подробнее в секции "Документация"
freq = 50
min_us = 400
max_us = 2550
dead_zone_us = 150

# создаем объект сервопривода
servo = ServoPDM360RP2Irq(pwm=servo_pwm, min_us=min_us, max_us=max_us, dead_zone_us=dead_zone_us, freq=freq)
```

<a id="doc"></a>
## Документация
<a id="doc_pdm"></a>
### Немного о PDM
PDM(pulse-duration modulation) - это процесс управления мощностью методом пульсирующего включения и выключения потребителя энергии. By Wikipedia®
В нашем случае она используется для управления сервоприводом. По времени импульса можно задать усилие и направление вращения сервопривода.
**ВНИМАНИЕ:** В отличие от PWM, управление происходит не по частоте, а по длительности импульса. 
Подробнее можно прочитать тут (с картинками): [wiki.amperka.ru](http://wiki.amperka.ru/articles:servo-pdm-continuous-rotation#%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D1%84%D0%B5%D0%B9%D1%81_%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F)

Для корректной работы сервопривода, нам необходимо задать следующие параметры:
- **freq** - частота импульсов, для аналоговых сервоприводов 50 Гц. Для цифровых 300 Гц и более.
- **min_us** - минимальное время импульса, при котором сервопривод начинает вращаться в одну сторону.
- **max_us** - максимальное время импульса, при котором сервопривод прекращает вращение в другую сторону.
- **dead_zone_us** - длительность центральной зоны, в которой сервопривод не вращается. Это переходная зона между двумя направлениями вращения.

Ниже я попытался графически представить эти параметры для аналогового сервопривода MG995_360:

![pdm configure](pdm_configure.png)

Как мы видим на рисунке, сервопривод начинает вращаться при длительности импульса 400 мкс, а прекращает вращение при 2600 мкс.
Таким образом мы получаем параметры `min_us=400` и `max_us=2550` (2600 - 50, так как при 2600 привод уже остановился). Теперь нам надо найти длительность центральной зоны.
На рисунке видно, что при длине импульса 1450 мкс сервопривод прекращает вращение по часовой стрелке и останавливается. 
Далее при длине импульса 1600 мкс начинается вращение в обратную сторону. Таким образом параметр `dead_zone_us=150` (1600-1450).

Где взять эти параметры для конкретного сервопривода? Все зависит от производителя. Но в большинстве случаев они указаны в документации.
Если нет, мо подбираем их вручную используя метод `set_duty` и задавая разные значения от 0 до 3000 мкс, с шагом в 50 мкс.
Пример такой конфигурации можно посмотреть в папке примерах файл [manual_config.py](https://github.com/TTitanUA/micropython_servo_pdm_360/tree/main/examples/manual_config.py).

#### Список параметров для сервоприводов:
- **MG995_360** - `min_us=400`, `max_us=2550`, `dead_zone_us=150`, `freq=50`
- **[Com-Motor05(joy it FS90R)](https://joy-it.net/en/products/COM-Motor05)** - `min_us=700`, `max_us=2300`, `dead_zone_us=90`, `freq=50` - By [@philsuess](https://github.com/philsuess)


**ПРОСЬБА:** Если вы нашли параметры для сервопривода, которых нет в списке, пожалуйста отправьте мне их через [issue](https://github.com/TTitanUA/micropython_servo_pdm_360/issues).

### Параметры конструктора ServoPDM360
**ServoPDM360RP2Async** и **ServoPDM360RP2Irq** его наследуют и имеют те же параметры

| Параметр     | Тип  | По умолчанию | Описание                      |
|--------------|------|--------------|-------------------------------|
| pwm          | PWM  | None         | PWM контроллер                |
| min_us       | int  | 500          | Минимальное время импульса    |
| max_us       | int  | 3000         | Максимальное время импульса   |
| dead_zone_us | int  | 150          | Длительность центральной зоны |
| freq         | int  | 50           | Частота импульсов             |
| invert       | bool | False        | Инверсия направления          |

- `pwm` - объект [PWM](https://docs.micropython.org/en/latest/library/machine.PWM.html) контроллера.
- `min_us` - Минимальное время импульса (скважность) [Подробнее](https://github.com/TTitanUA/micropython_servo_pdm_360#doc_pdm).
- `max_us` - Максимальное время импульса (скважность) [Подробнее](https://github.com/TTitanUA/micropython_servo_pdm_360#doc_pdm)
- `dead_zone_us` - Длительность центральной зоны [Подробнее](https://github.com/TTitanUA/micropython_servo_pdm_360#doc_pdm)
- `freq` - Частота импульсов, для аналоговых приводов это 50. Цифровые обычно 300 и более.
- `invert` - Инверсия направления (возможно потребуется для некоторых приводов, а может и нет :) )

<a id="doc_base"></a>
### Методы базового класса ServoPDM360
- `set_duty(duty: int)` - Устанавливает произвольное значение скважности в диапазоне от 0 до 65000.
Данный метод предназначен для ручного поиска минимального и максимального значения скважности. [Подробнее](https://github.com/TTitanUA/micropython_servo_pdm_360#doc_pdm)
- `turn_cv(force: int)` - Начинает вращение привода по часовой стрелке с заданным ускорением.
- `turn_ccv(force: int)` - Начинает вращение привода против часовой стрелки с заданным ускорением.
- `stop()` - Останавливает вращение привода.
- `deinit()` - Отключает PWM генерацию.

### Методы класса ServoPDM360RP2Async и ServoPDM360RP2Irq
- `turn_cv_ms(...)` - Вращает привод по часовой стрелке с указанием разных параметров.
- `turn_сcv_ms(...)` - Вращает привод против часовой стрелки с указанием разных параметров.

| Параметр        | Тип             | По умолчанию | Описание                                                                                                     |
|-----------------|-----------------|--------------|--------------------------------------------------------------------------------------------------------------|
| time_ms         | Int             | 0            | Время вращение (0 - Бесконечно)                                                                              |
| force           | Int             | None         | Усилие, если не указанно берется из `start_smoothing`                                                        |
| start_smoothing | ServoSmoothBase | None         | Стартовое замедление, если не указан старт будет мгновенный                                                  |
| end_smoothing   | ServoSmoothBase | None         | Замедление остановки, если не указан остановка будет мгновенная                                              |
| callback        | callable        | None         | Функция которая будет вызвана после окончания работы команды. Если `time_ms` == 0 то после окончания разгона |

- `stop_smooth` - Плавная остановка привода.

| Параметр      | Тип             | По умолчанию | Описание                                                      |
|---------------|-----------------|--------------|---------------------------------------------------------------|
| end_smoothing | ServoSmoothBase | None         | Замедление остановки                                          |
| callback      | callable        | None         | Функция которая будет вызвана после окончания работы команды. |

### Замедления
Для управления замедлениями можно использовать классы `ServoSmoothBase` и его наследников.
В данной библиотеке есть только линейное замедление `SmoothLinear`, если вам требуется больше, установите библиотеку [smooth-servo](https://pypi.org/project/smooth-servo/).
Пример использования встроенного замедления:
```python
from machine import Pin, PWM
from micropython_servo_pdm_360 import ServoPDM360RP2Async, SmoothLinear

# создаем PWD контроллер сервопривода (21 - пин Pico)
servo_pwm = PWM(Pin(21))

# Задаем параметры импульсов сервопривода, подробнее в секции "Документация"
freq = 50
min_us = 400
max_us = 2550
dead_zone_us = 150

# создаем объект сервопривода
servo = ServoPDM360RP2Async(pwm=servo_pwm, min_us=min_us, max_us=max_us, dead_zone_us=dead_zone_us, freq=freq)

# Повернуть привод по часовой стрелке в течении двух секунд с усилием 50 и замедлением в начале. После вывести в консоль "callback cv"
servo.turn_cv_ms(2000, 50, start_smoothing=SmoothLinear(50, 1000),  callback=lambda: print("callback cv"))
```
Подробно про параметры и типы замедлений можно прочитать в [документации к smooth_servo](https://github.com/TTitanUA/smooth_servo#doc).


## Примеры
Примеры использования можно найти в папке [examples](https://github.com/TTitanUA/micropython_servo_pdm_360/tree/main/examples).

<a id="feedback"></a>
## Баги и обратная связь
При нахождении багов создавайте [issue](https://github.com/TTitanUA/micropython_servo_pdm_360/issues)
Библиотека открыта для доработки и ваших [pull запросов](https://github.com/TTitanUA/micropython_servo_pdm_360/pulls)!
