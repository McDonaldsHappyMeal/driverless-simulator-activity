# Simple Project
Self contained python codebase, acting as a platform to experiment with motion control implementations. This aims to have as few dependencies as possible and be compatible with Linux, Windows and Mac. To run, change the directory to where this codebase is located in your device with `cd folder_to_your_path`, and then run `python main.py` into the command line.

## Requirements
 - python
 - pygame
 - numpy
 - pynput

## Coordinate System
This uses standard SI units, so radians, m/s and m/s^2

Normal maths like coordinate system is used:
The x-axis is positive to the right and the y-axis is positive upwards.
Angles are positive anticlockwise.

## Get started
1. If you don't have Python installed, [install Python 3.11.1 here](https://www.python.org/downloads/release/python-3111/)
2. Download the repository by clicking the green "Code" button on the top of the page, then "Download Zip"
3. Extract the Zip file
4. Open command prompt or terminal, and navigate to your newly extracted folder with `cd path/to/your/folder`
5. Install necessary dependencies using `pip install -r requirements.txt`. If prompted to install with y/n, type y then enter
6. Run `python3 main.py` (or `python main.py`) and it should come up with errors saying that you need to fill in some code in `motion_controller.py`.
If you have trouble or have unexpected errors with anything, please don't hesitate to ask a senior for help! :D

## Classes

#### Motion Controller
**Your task is to finish the implementation of this class, so that the car can successfully go around the track**

A class that the user should extend and implement their own functions into in order to make everything work.
You should take in the car's position and reference waypoints, and then output steering & throttle controls to follow the waypoints.

The only implementations to complete are in `motion_controller.py`. Read the comments to help guide you through three main tasks you need to achieve a working autonomous simulator!

Ideas of types of controllers to look at for inspiration:
 - Pure Pursuit
 - Stanley
 - Model Predictive Control

*Note: The vehicle model here is very simplified, so much of what you see online may be overly complicated*

The framework for this has already been implemented for you, but feel free to extend it as you wish. The only thing you need to do is to complete the get_controls() function that's in the MotionController class. That function also contains some additional comments to explain what the *car's position* and *reference waypoints* actually are.

#### Kinematic Vehicle Model
Implements a kinematic bicycle model that takes in a throttle and steering input between [-1, 1].
There is nothing implementing drag, so this will go infinitely fast if you hold down the throttle.

#### Path Planner
Takes in the cars current state and gives a list of waypoints in the form [x, y, target_velocity]. The waypoints have been precomputed for simplicity.

#### Trackmap GUI
Visualizes the cones on the track, the car's current position, and the reference waypoints.

#### Keyboard Controller
Overrides the Motion Controller, and allows the user to control the vehicle model with the keyboard. Use WASD or Arrows.
To use this, type `python main.py keyboard` into the command line.

