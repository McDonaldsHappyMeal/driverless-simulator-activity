import math
from utils import CarState, Controls, clamp, wrap_angle

class VehicleModel():
    def __init__(self):
        self._state = CarState()
        self._steer_req = 0.0
        self._throttle_req = 0.0

        self._steer_angle = 0
        self._slip_angle = 0

        self._COG_front = 0.78
        self._COG_rear = 0.77

    def set_control_inputs(self, controls):
        self._steer_req = clamp(controls.steering, -1.0, 1.0)
        self._throttle_req = clamp(controls.throttle, -1.0, 1.0)
    
    def get_state(self, delta_time):
        if self._state.velocity < .0:
            self._state.accel = max(0, self._throttle_req * 5)
        else:
            self._state.accel = self._throttle_req * 4
        self._steer_angle = self._steer_req * 0.43 # map [-1, 1] to radians

        # Kinematic Bicycle Maths
        ratio = math.tan(self._steer_angle) * self._COG_rear / (self._COG_front + self._COG_rear)
        _slip_angle = math.atan(ratio)

        self._state.x_pos    += self._state.velocity * math.cos(_slip_angle + self._state.yaw) * delta_time
        self._state.y_pos    += self._state.velocity * math.sin(_slip_angle + self._state.yaw) * delta_time
        self._state.velocity += self._state.accel * delta_time
        self._state.velocity = max(self._state.velocity, .0)
        self._state.yaw      += (self._state.velocity / self._COG_rear) * math.sin(_slip_angle) * delta_time
        self._state.yaw      = wrap_angle(self._state.yaw)
        return self._state 