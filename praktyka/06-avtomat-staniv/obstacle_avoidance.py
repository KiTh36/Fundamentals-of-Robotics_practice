import time
from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B
from ev3dev2.sensor import INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor

# Датчик препятствий
ultrasonic = UltrasonicSensor(INPUT_3)

# Моторы
tank = MoveTank(OUTPUT_A, OUTPUT_B)

# Настройки движения
SPEED = 35
REVERSE_SPEED = -12
OBSTACLE_DISTANCE = 25  # см


def stop():
    tank.off()


def avoid_obstacle():
    """Отъехать от препятствия, повернуть и продолжить поиск пути."""
    stop()
    time.sleep(0.2)

    # Отъехать назад
    tank.on_for_seconds(REVERSE_SPEED, REVERSE_SPEED, 0.4)

    # Повернуть на месте
    tank.on_for_rotations(15, -15, 0.65)


try:
    while True:
        distance = ultrasonic.distance_centimeters

        if distance <= OBSTACLE_DISTANCE:
            print("Препятствие обнаружено. Выполняю объезд.")
            avoid_obstacle()
            continue

        # Если путь свободен, продолжить движение вперёд
        tank.on(SPEED, SPEED)
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Программа остановлена.")

finally:
    stop()
