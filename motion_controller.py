import math
import numpy as np
from utils import Controls, Point, wrap_angle

class MotionController():
    def __init__(self):
        """
            The constructor function called when you make an object of type MotionController()
        """
        self.time = 0

    def get_controls(self, car_state, path_reference):
        """
        Input parameters:
            - car_state: An object of type CarState(), you can find the definition in utils.py
                         This is represented by the pink shape in the GUI
                         It has the attributes:
                         car_state.x_pos: x position of car in world frame
                         car_state.y_pos: x position of car in world frame
                         car_state.velocity: velocity of car in m/s
                         car_state.yaw: The yaw(heading) of the car in radians, +/- pi.


            - path_reference: A list of RefPoint() objects
                              This is represented by the green line in the GUI
                              path_reference[0] is the first object in the list, a Refpoint
                              
                              path_reference[0].vel is a number that is the target velocity at that waypoint
                              path_reference[0].x is a number that is the x coordinate of the point
                              path_reference[0].y is a number that is the y coordinate of the point

        """

        min_distance = distance(path_reference[0].x, path_reference[0].y, car_state.x_pos, car_state.y_pos)
        min_ind = 0
        for waypoint in path_reference:
            


######################## TODO: ADD YOUR CODE HERE ########################

            temp_distance = ??? # [1] Find the distance between the car and the waypoint
            
            if temp_distance < ???: # [2] Check if the distance we find is the smallest distance
                min_ind = path_reference.index(waypoint)
                min_distance = temp_distance
        

        lookahead_distance = 5      # [3] Tune! (Increments of 2 recommended) 
        k_steering = 0.95           # [3] Tune! (0.02 increments recommended)
        kp = 0.09                   # [3] Tune! (0.01 increments recommended)

#####################################################################

        goal_reference = path_reference[min_ind]
        for i in range(min_ind + 1, len(path_reference)):
            if distance(path_reference[i].x, path_reference[i].y, car_state.x_pos, car_state.y_pos) < lookahead_distance:
                goal_reference = path_reference[i]
        car_vec = np.array([car_state.x_pos, car_state.y_pos])
        goal_vec = np.array([goal_reference.x, goal_reference.y])
        car2goal_vec = goal_vec - car_vec
        car_y_vec = np.array([-math.sin(car_state.yaw), math.cos(car_state.yaw)])
        l = np.linalg.norm(car2goal_vec)
        y_offset = np.dot(car2goal_vec, car_y_vec)
        gamma = 2 * y_offset / math.pow(l, 2)
        steering = k_steering * gamma
        error = goal_reference.vel - car_state.velocity
        throttle = error * kp
        return Controls(steering, throttle)
    
def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)