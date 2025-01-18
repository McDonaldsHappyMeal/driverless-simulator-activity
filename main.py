import time
import sys
from pathlib import Path

from trackmap_gui import TrackMapGUI
from vehicle_model import VehicleModel
from path_planning import PathPlanner
from motion_controller import MotionController
from keyboard_controller import KeyboardController

rate = 50.0

def main(keyboard=False):
    track_csv = Path("./FSG2019.csv")
    track_ref_csv = Path("./FSG2019_ref.csv")
    gui = TrackMapGUI(track_csv)
    vehicle = VehicleModel()
    planner = PathPlanner(track_ref_csv)
    if keyboard:
        controller = KeyboardController()
    else:
        controller = MotionController()
    gimped_start = (7.882057046,  2.01424213)
    gimped_end   = (7.760777519, -1.320944855)
    midpoint = ((gimped_start[0] + gimped_end[0]) / 2.0,
                (gimped_start[1] + gimped_end[1]) / 2.0)
    threshold = 0.5
    needed_time = 15.0
    lap_start_time = None
    lap_time = 0.0
    has_finished = False
    state = 0
    while True:
        if not has_finished:
            car = vehicle.get_state(1.0 / rate)
            next_reference = planner.get_next_reference(car)
            next_controls = controller.get_controls(car, next_reference)
            vehicle.set_control_inputs(next_controls)
            dist_to_mid = distance(car.x_pos, car.y_pos, midpoint[0], midpoint[1])
            if state == 0:
                if dist_to_mid > threshold:
                    lap_start_time = time.time()
                    state = 1
                    lap_time = 0.0
            elif state == 1:
                if dist_to_mid < threshold:
                    elapsed = time.time() - lap_start_time
                    if elapsed >= needed_time:
                        lap_time = elapsed
                        has_finished = True
                        state = 2
            gui.update_lap_time(lap_time)
            gui.update_vehicle(car)
            gui.update_reference(next_reference)
        else:
            gui.update_lap_time(lap_time)
        gui.event_loop()
        time.sleep(1.0 / rate)

def distance(x1, y1, x2, y2):
    """Euclidean distance helper."""
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

if __name__ == "__main__":
    keyboard = len(sys.argv) > 1 and sys.argv[1] == "keyboard"
    main(keyboard)
