#!/usr/bin/env python3
import time

from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B
from ev3dev2.sensor import INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor

# Initialize the drive motors and ultrasonic sensor.
tank = MoveTank(OUTPUT_A, OUTPUT_B)
ultrasonic = UltrasonicSensor(INPUT_3)

# Movement settings.
SPEED = 35
REVERSE_SPEED = -12
OBSTACLE_DISTANCE = 25  # Centimeters


def stop():
    """Stop both drive motors."""
    tank.off()


def avoid_obstacle():
    """Move away from an obstacle, turn, and resume the search."""
    stop()
    time.sleep(0.2)

    # Reverse to create distance from the obstacle.
    tank.on_for_seconds(REVERSE_SPEED, REVERSE_SPEED, 0.4)

    # Turn in place to choose a different direction.
    tank.on_for_rotations(15, -15, 0.65)


def main():
    print("Obstacle avoidance started.")

    try:
        while True:
            distance = ultrasonic.distance_centimeters

            if distance <= OBSTACLE_DISTANCE:
                print("Obstacle detected. Avoiding obstacle.")
                avoid_obstacle()
            else:
                # The path is clear, so keep moving forward.
                tank.on(SPEED, SPEED)

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("Program stopped by the user.")

    finally:
        stop()
        print("Motors stopped.")


if __name__ == "__main__":
    main()
