
from MovingObject import MovingObject


class AppAgent(MovingObject):
    def __init__(self, name, x, y, university_location, buses, trains, speed=1, canvas=None):
        # Pass the canvas to the MovingObject
        super().__init__(name, x, y, speed, canvas=canvas, color="light blue") # Use a different color for the agent
        self.state = "waiting_for_bus"
        self.buses = buses
        self.trains = trains
        self.university_location = university_location
        self.home_location = (x, y) # Set home location at initialization
        self.current_bus = None
        self.current_train = None
        self.destination = self.university_location  # Set destination at initialization

    def calculate_route(self, start, end):
        route = []
        x, y = start
        dest_x, dest_y = end

        # Horizontal movement
        while x != dest_x:
            if dest_x > x:
                x = min(x + self.grid_spacing, dest_x)
            else:
                x = max(x - self.grid_spacing, dest_x)
            route.append((x, y))

        # Vertical movement
        while y != dest_y:
            if dest_y > y:
                y = min(y + self.grid_spacing, dest_y)
            else:
                y = max(y - self.grid_spacing, dest_y)
            route.append((x, y))
        print(f"Calculated route from {start} to {end}: {route}")
        return route

    def update_position(self):
        print(f"{self.name} | State: {self.state} | Position: ({self.x}, {self.y})")

        if self.state == "waiting_for_bus":
            for bus in self.buses:
                same_location = (round(bus.x), round(bus.y)) == (round(self.x), round(self.y))
                if same_location and bus.is_paused() and (round(bus.x), round(bus.y)) in bus.pause_stations:
                    print(f"{self.name} is boarding {bus.name}")
                    bus.passengers.append(self.name)  # Add app to bus passengers
                    self.set_route(bus.route[bus.route_index:], is_fixed_route=False)
                    self.current_bus = bus
                    self.state = "on_bus"
                    # Hide the app's canvas items
                    self.canvas.itemconfigure(self.canvas_id, state="hidden")
                    self.canvas.itemconfigure(self.text_id, state="hidden")
                    break

        elif self.state == "on_bus":
            if self.current_bus:
                self.x = self.current_bus.x
                self.y = self.current_bus.y
                current_position = (round(self.x), round(self.y))
                print(f"{self.name} is on {self.current_bus.name} at {current_position}")
                if current_position in self.current_bus.pause_stations and current_position in self.trains[0].route:
                    print(f"{self.name} is getting off {self.current_bus.name} to wait for a train")
                    self.current_bus.passengers.remove(self.name)  # Remove app from bus passengers
                    self.state = "waiting_for_train"
                    self.set_route([current_position], is_fixed_route=False)
                    self.current_bus = None
                    # Show the app's canvas items
                    self.canvas.itemconfigure(self.canvas_id, state="normal")
                    self.canvas.itemconfigure(self.text_id, state="normal")

        elif self.state == "waiting_for_train":
            for train in self.trains:
                same_location = (round(train.x), round(train.y)) == (round(self.x), round(self.y))
                if same_location and train.is_paused():
                    print(f"{self.name} is boarding {train.name}")
                    train.passengers.append(self.name) # Add app to train passengers
                    self.set_route(train.route[train.route_index:], is_fixed_route=False)
                    self.current_train = train
                    self.state = "on_train"
                    # Hide the app's canvas items
                    self.canvas.itemconfigure(self.canvas_id, state="hidden")
                    self.canvas.itemconfigure(self.text_id, state="hidden")
                    break

        elif self.state == "on_train":
            if self.current_train:
                self.x = self.current_train.x
                self.y = self.current_train.y
                current_position = (round(self.x), round(self.y))
                print(f"{self.name} is on {self.current_train.name} at {current_position}")
                station_near_uni = (250, 550)
                if current_position == station_near_uni:
                    print(f"{self.name} is getting off {self.current_train.name} to walk to the university")
                    self.current_train.passengers.remove(self.name) # Remove app from train passengers
                    self.state = "walking"
                    route = self.calculate_route((self.x, self.y), self.university_location)
                    print(f"Walking route: {route}")
                    self.set_route(route, is_fixed_route=False)
                    self.current_train = None
                    # Show the app's canvas items
                    self.canvas.itemconfigure(self.canvas_id, state="normal")
                    self.canvas.itemconfigure(self.text_id, state="normal")

        elif self.state == "walking":
            if (round(self.x), round(self.y)) == self.university_location:
                print(f"{self.name} has arrived at the university!")
                self.state = "walking_station"
                station_after_uni_station = (250, 700)
                route = self.calculate_route((self.x, self.y), station_after_uni_station)
                print(f"{self.name} is walking to the station near the university: {route}")
                self.set_route(route, is_fixed_route=False)

        elif self.state == "walking_station":
            station_after_uni_station = (250, 700)
            if (round(self.x), round(self.y)) == station_after_uni_station:
                print(f"{self.name} is at the station near the university")
                self.state = "waiting_for_home_train"
                self.set_route([station_after_uni_station], is_fixed_route=False)

        elif self.state == "waiting_for_home_train":
            for train in self.trains:
                same_location = (round(train.x), round(train.y)) == (round(self.x), round(self.y))
                if same_location and train.is_paused():
                    print(f"{self.name} is boarding {train.name} to go home")
                    train.passengers.append(self.name)  # Add app to train passengers
                    self.set_route(train.route[train.route_index:], is_fixed_route=False)
                    self.current_train = train
                    self.state = "on_home_train"
                    # Hide the app's canvas items
                    self.canvas.itemconfigure(self.canvas_id, state="hidden")
                    self.canvas.itemconfigure(self.text_id, state="hidden")
                    break

        elif self.state == "on_home_train":
            if self.current_train:
                self.x = self.current_train.x
                self.y = self.current_train.y
                current_position = (round(self.x), round(self.y))
                station_near_home = (450, 100)
                if current_position == station_near_home:
                    print(f"{self.name} is getting off {self.current_train.name} to walk home")
                    self.current_train.passengers.remove(self.name) # Remove app from train passengers
                    self.state = "walking_home"
                    route = self.calculate_route((self.x, self.y), self.home_location)
                    print(f"Walking home route: {route}")
                    self.set_route(route, is_fixed_route=False)
                    self.current_train = None
                    # Show the app's canvas items
                    self.canvas.itemconfigure(self.canvas_id, state="normal")
                    self.canvas.itemconfigure(self.text_id, state="normal")

        elif self.state == "walking_home":
            if (round(self.x), round(self.y)) == self.home_location:
                print(f"{self.name} has returned home!")
                self.state = "waiting_for_bus"
                self.set_route([], is_fixed_route=False)
                self.current_bus = None
                self.current_train = None

        if self.state in [
            "walking", "walking_home", "walking_station",
            "on_bus", "on_train", "waiting_for_train",
            "waiting_for_home_train", "on_home_train"
        ]:
            super().update_position()