import pygame
import sys
import math

# MMS
from utils import load_track_cones, ConeTypes, Point, CarState, transform_vector

class TrackMapGUI():
    def __init__(self, csv_name):
        # -- Load track data
        self.track_name = csv_name.stem
        self._track = load_track_cones(csv_name)
        print(f"Loading track: \"{self.track_name}\" with {len(self._track)} cones")

        # -- Basic display settings
        self._canvas_width = 800
        self._canvas_height = 800
        self._background_color = (70, 70, 70)  # A darkish grey
        self._car_color = (255, 140, 0)      # Pinkish (R, G, B)

        # -- Initialize pygame
        pygame.init()
        pygame.display.set_caption('MMS Driverless Simulator Activity')
        self._screen = pygame.display.set_mode((self._canvas_width, self._canvas_height))
        self._clock = pygame.time.Clock()

        # -- Font for displaying lap time
        self._font = pygame.font.SysFont('Arial', 20)
        self._lap_time = 0.0  # we will update this from main.py

        # -- Track bounding box & scaling
        self._buffer = 10
        self._min_x, self._max_x, self._min_y, self._max_y = self._find_track_bounds()
        # To avoid divide-by-zero in trivial cases
        self._width = max(1, self._max_x - self._min_x)
        self._height = max(1, self._max_y - self._min_y)
        # Scale so the entire track fits in the 1000x1000 window
        self._scale = min(
            (self._canvas_width - 2 * self._buffer) / self._width,
            (self._canvas_height - 2 * self._buffer) / self._height
        )

        # -- Store references for drawing
        self._reference = []
        self._car_poly = ((-1.5, -0.7), (-1.5, 0.7), (1.5, 0.7), (2.2, 0), (1.5, -0.7))
        self._vehicle_state = CarState()  # will hold the car state each frame

        # -- Predefine colors for cones based on ConeTypes
        self._cone_colors = {
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
            "orange": (255, 165, 0)
        }

    def update_vehicle(self, car_state):
        """
        Called each iteration in main.py to store the updated car state.
        We'll draw it in event_loop().
        """
        self._vehicle_state = car_state

    def update_reference(self, reference):
        """
        Called each iteration in main.py to store the new reference waypoints.
        We'll draw them in event_loop().
        """
        self._reference = reference

    def update_lap_time(self, lap_time):
        """
        Called from main.py to update the displayed lap time.
        """
        self._lap_time = lap_time

    def event_loop(self):
        """
        Called each iteration in main.py.  
        1) Handles user events (like closing the window).  
        2) Draws everything to the screen.  
        3) Maintains the Pygame display loop.  
        """
        # -- Pygame event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # -- Clear screen
        self._screen.fill(self._background_color)

        # -- Draw track cones
        self._draw_cones()

        # -- Draw reference line
        self._draw_reference()

        # -- Draw vehicle
        self._draw_vehicle()

        # -- Draw lap time in top-left corner
        text_str = f"Lap time: {self._lap_time:.2f}s"
        textsurface = self._font.render(text_str, True, (255, 255, 255))
        self._screen.blit(textsurface, (10, 10))

        # -- Update display
        pygame.display.flip()

        # (Optional) limit to ~60 FPS so we don’t use 100% CPU
        self._clock.tick(60)

    # ------------------------------------------------------------------
    # Internal helper methods below
    # ------------------------------------------------------------------
    def _find_track_bounds(self):
        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0
        for cone in self._track:
            min_x = min(cone.x, min_x)
            max_x = max(cone.x, max_x)
            min_y = min(cone.y, min_y)
            max_y = max(cone.y, max_y)
        # Add a small buffer so edges aren’t right at the window border
        return min_x - self._buffer, max_x + self._buffer, min_y - self._buffer, max_y + self._buffer

    def _world_to_screen(self, x, y):
        """
        Convert world coordinates (x,y) -> screen coordinates (sx,sy).
        In Pygame, (0,0) is top-left, so we usually invert y.
        """
        sx = (x - self._min_x) * self._scale
        sy = (self._max_y - y) * self._scale
        return (sx, sy)

    def _draw_cones(self):
        for cone in self._track:
            screen_pos = self._world_to_screen(cone.x, cone.y)
            color_name = ConeTypes(cone.type).name

            if (cone.x, cone.y, cone.type) == (1.696801183, -1.502864145, 2):  # Gate Start
                pygame.draw.circle(self._screen, (255, 0, 0), (int(screen_pos[0]), int(screen_pos[1])), 8)  # Bright red
                self._draw_label(screen_pos, "Gate Start", (255, 0, 0))

            elif (cone.x, cone.y, cone.type) == (2, 2.56, 2):  # Gate End
                pygame.draw.circle(self._screen, (0, 255, 0), (int(screen_pos[0]), int(screen_pos[1])), 8)  # Bright green
                self._draw_label(screen_pos, "Gate End", (0, 255, 0))

            else:
                # Regular cones
                color = self._cone_colors.get(color_name, (255, 255, 255))  # Default to white if type unknown
                pygame.draw.circle(self._screen, color, (int(screen_pos[0]), int(screen_pos[1])), 3)

    def _draw_label(self, position, text, color):
        """
        Draw a text label next to a given position.
        """
        label_surface = self._font.render(text, True, color)
        self._screen.blit(label_surface, (position[0] + 10, position[1] - 10))


    def _draw_reference(self):
        # Draw line segments between consecutive ref points
        if len(self._reference) < 2:
            return
        for i in range(len(self._reference) - 1):
            p1 = self._world_to_screen(self._reference[i].x, self._reference[i].y)
            p2 = self._world_to_screen(self._reference[i+1].x, self._reference[i+1].y)
            pygame.draw.line(self._screen, (0, 255, 0), p1, p2, 3)

    def _draw_vehicle(self):
        # Rotate & transform the car polygon
        rotated_car_poly = []
        for pt in self._car_poly:
            # transform_vector from utils transforms a local point by x,y,yaw
            world_coord = transform_vector(pt, 
                                           self._vehicle_state.x_pos, 
                                           self._vehicle_state.y_pos, 
                                           self._vehicle_state.yaw)
            # Convert to screen
            rotated_car_poly.append(self._world_to_screen(world_coord[0], world_coord[1]))

        # Convert to int for pygame
        rotated_car_poly = [(int(x), int(y)) for (x, y) in rotated_car_poly]
        pygame.draw.polygon(self._screen, self._car_color, rotated_car_poly)
