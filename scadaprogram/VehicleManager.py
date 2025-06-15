import random
from MovingObject import MovingObject
from VehicleInfoWindow import VehicleInfoWindow

class VehicleManager:
    def __init__(self, canvas):
        self.vehicles = []
        self.canvas = canvas

    def create_vehicle(self, name, x, y, speed, color, route, pause_stations):
        """
        Create a MovingObject, set its route/pause stations, assign random passengers if needed,
        bind click → info window, and return the created vehicle.
        """
        vehicle = MovingObject(name, x, y, speed=speed, canvas=self.canvas, color=color)
        vehicle.set_route(route, is_fixed_route=True)
        vehicle.set_pause_stations(pause_stations)

        # All vehicles except Train 1 get random passengers by default.
        # (Train 1’s passenger count is updated via MQTT elsewhere.)
        if name != "Train 1":
            # Now that random is imported, this will work:
            vehicle.passengers = [f"Person {i+1}" for i in range(random.randint(0, 5))]
        else:
            vehicle.passengers = []  # Will be updated by TrainManager.updateTrainOccupancy()

        self.vehicles.append(vehicle)

        # Bind click → open VehicleInfoWindow
        self.canvas.tag_bind(
            vehicle.canvas_id,
            "<Button-1>",
            lambda event, v=vehicle: self.on_click(event, v)
        )

        return vehicle  # Return the created MovingObject

    def on_click(self, event, vehicle):
        """
        Opens (or lifts) the VehicleInfoWindow for this vehicle.
        """
        if hasattr(self, 'info_window') and self.info_window and self.info_window.window.winfo_exists():
            self.info_window.window.lift()
        else:
            self.info_window = VehicleInfoWindow(vehicle)
