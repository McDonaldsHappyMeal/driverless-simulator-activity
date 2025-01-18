from utils import RefPoint, Point, norm

class PathPlanner():
    def __init__(self, csv_reference, num_refs = 5):
        self._reference = self._load_reference_csv(csv_reference)
        self._num_refs = num_refs

    def get_next_reference(self, car_state):
        car_pos = Point(car_state.x_pos, car_state.y_pos)
        closest_dist = 2**16
        closest_idx = 0
        for idx, ref in enumerate(self._reference):
            curr_dist = norm(car_pos, ref)
            if curr_dist < closest_dist:
                closest_dist = curr_dist
                closest_idx = idx
        refs = [self._reference[x % len(self._reference)] for x in range(closest_idx, closest_idx+self._num_refs)]
        return refs 

    def _load_reference_csv(self, csv_reference):
        track = []
        with open(csv_reference, 'r') as track_file:
            for line in track_file.readlines():
                x, y, vel = line.strip().split(",")
                track.append(RefPoint(float(x), float(y), float(vel)*1.5))
        return track
