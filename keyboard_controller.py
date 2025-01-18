import math
from pynput import keyboard
from utils import Controls

ACCEL_SCALE = 1.0
ACCEL_MAX = 2.25
BRAKE_SCALE = 4.0
BRAKE_MAX = -10.0
STEER_SCALE = 0.04
STEER_MAX = 1.0

class Car():
    def __init__(self):
        self.acceleration = 0
        self.steerAngle = 0

class KeyboardController():
    def __init__(self):
        self.car = Car()
        self.left = False
        self.right = False
        self.up = False
        self.down = False

        # Asynchronous
        listener = keyboard.Listener(
            on_press = self._on_press_key,
            on_release = self._on_release_key)
        listener.start()

    def _on_press_key(self, key):
        if key.char in('w' or 'up'):
            self.up = True
        elif key.char in('s' or 'down'):
            self.down = True
        elif key.char in('a' or 'left'):
            self.left = True
        elif key.char in('d' or 'right'):
            self.right = True

    def _on_release_key(self, key):
        if key.char in('w' or 'up'):
            self.up = False
        elif key.char in('s' or 'down'):
            self.down = False
        elif key.char in('a' or 'left'):
            self.left = False
        elif key.char in('d' or 'right'):
            self.right = False

    def get_controls(self, car_state, path_reference):
        if self.left or self.right:
            if not self.right and self.car.steerAngle < 0 or \
             not self.left and self.car.steerAngle > 0:
                self.car.steerAngle = 0
            
            if self.left and self.car.steerAngle <= STEER_MAX:
                self.car.steerAngle += 1.0 * STEER_SCALE
            
            if self.right and self.car.steerAngle >= -STEER_MAX:
                self.car.steerAngle += -1.0 * STEER_SCALE
        else:
            self.car.steerAngle = 0
        
        if self.down or self.up:
            if self.up:
                if self.car.acceleration < 0:
                    self.car.acceleration = 0
                if self.car.acceleration < ACCEL_MAX:
                    self.car.acceleration += 1.0 * ACCEL_SCALE
            if self.down:
                if self.car.acceleration > 0:
                    self.car.acceleration = 0
                if self.car.acceleration > BRAKE_MAX:
                    self.car.acceleration += -1.0 * BRAKE_SCALE
        else:
            self.car.acceleration = 0

        return Controls(self.car.steerAngle/STEER_MAX, self.car.acceleration)
