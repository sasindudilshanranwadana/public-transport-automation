import math
import time

class MovingObject:
    def __init__(self, name, x, y, speed=2, grid_spacing=50, canvas=None, color="blue"):
        self.name = name
        self.x = x
        self.y = y
        self.speed = speed
        self.route = []
        self.route_index = 0
        self.is_fixed_route = False
        self.grid_spacing = grid_spacing
        self.canvas_id = None
        self.text_id = None
        self.canvas = canvas
        self.last_stop_time = None
        self.pause_duration = 5
        self.pause_highlight_id = None
        self.pause_stations = []
        self.color = color
        self.passengers = []

        if self.canvas:
            self.create_canvas_item()

    def create_canvas_item(self):
        self.canvas_id = self.canvas.create_oval(self.x - 5, self.y - 5, self.x + 5, self.y + 5, fill=self.color, tags="moving")
        self.text_id = self.canvas.create_text(self.x, self.y - 10, text=self.name, font=("Arial", 6), tags="moving")

    def set_route(self, route, is_fixed_route=False):
        if not all(isinstance(point, tuple) and len(point) == 2 for point in route):
            raise ValueError("Route must be a list of (x, y) tuples")
        self.route = [self.snap_to_grid(x, y) for x, y in route]
        self.route_index = 0
        self.is_fixed_route = is_fixed_route
        self.last_stop_time = None

    def snap_to_grid(self, x, y):
        snapped_x = round(x / self.grid_spacing) * self.grid_spacing
        snapped_y = round(y / self.grid_spacing) * self.grid_spacing
        return snapped_x, snapped_y

    def update_position(self):
        if self.is_paused():
            if self.pause_highlight_id is None:
                self.pause_highlight_id = self.canvas.create_oval(
                    self.x - 10, self.y - 10, self.x + 10, self.y + 10,
                    outline="white", width=2, tags="pause"
                )
            return

        if self.pause_highlight_id is not None:
            self.canvas.delete(self.pause_highlight_id)
            self.pause_highlight_id = None

        if self.route and self.route_index < len(self.route):
            target_x, target_y = self.route[self.route_index]
            dx, dy = target_x - self.x, target_y - self.y
            distance = math.hypot(dx, dy)

            if distance < self.speed:
                self.x, self.y = target_x, target_y
                self.route_index += 1
                self.check_pause()
            else:
                scale = self.speed / distance
                self.x += dx * scale
                self.y += dy * scale

            if self.canvas:
                self.canvas.coords(self.canvas_id, self.x - 5, self.y - 5, self.x + 5, self.y + 5)
                self.canvas.coords(self.text_id, self.x, self.y - 10)

            # ✅ Log current position to console
            if self.name.startswith("Person"):
                print(f"[LOG] {self.name} location → X: {int(self.x)}, Y: {int(self.y)}")

        if self.route_index >= len(self.route):
            self.route_index = 0

    def is_paused(self):
        return self.last_stop_time and time.time() - self.last_stop_time < self.pause_duration

    def set_pause_stations(self, stations):
        self.pause_stations = [self.snap_to_grid(x, y) for x, y in stations]

    def check_pause(self):
        if (self.x, self.y) in self.pause_stations:
            self.last_stop_time = time.time()
