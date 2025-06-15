import math
import random

class StationManager:
    def __init__(self, stations, radius):
        # stations: dict of {station_name: (x,y)}
        self.stations = stations
        self.radius = radius

        # Detection sets per station
        self.detections = {name: set() for name in stations}

        # Holds the current (real) platform count per station
        # Glenferrie will be updated via MQTT; others will be randomly set in get_people_count()
        self.people_counts = {name: 0 for name in stations}

        # Holds the current (real) train occupancy per train name
        # Only “Train 1” is updated via MQTT; others will be random in get_train_count()
        self.train_counts = {}

    def check_detections(self, moving_objects):
        """
        Clear previous detections and re-populate according to moving_objects’ positions.
        """
        for name in self.detections:
            self.detections[name].clear()

        for obj in moving_objects:
            for station_name, (sx, sy) in self.stations.items():
                if self.is_within_radius(obj.x, obj.y, sx, sy):
                    self.detections[station_name].add(obj.name)

    def is_within_radius(self, x1, y1, x2, y2):
        return math.hypot(x1 - x2, y1 - y2) <= self.radius

    def updateStationPeopleCount(self, station_name, count):
        """
        Called by MainApp when a new MQTT message arrives for 'scada/platform_count'.
        Only Glenferrie should be updated this way. Others ignore.
        """
        if station_name in self.people_counts:
            self.people_counts[station_name] = count
            # Debug print (optional)
            print(f"[StationManager] {station_name} platform count updated: {count}")

    def updateTrainCount(self, train_name, count):
        """
        Called by MainApp when a new MQTT message arrives for 'scada/bus/occupancy/people_count'.
        Only 'Train 1' is expected. Others ignore.
        """
        if train_name == "Train 1":
            self.train_counts[train_name] = count
            # Debug print (optional)
            print(f"[StationManager] {train_name} passenger count updated: {count}")

    def get_status_lines(self):
        """
        Returns a list of status lines to display in the sidebar.
        - Each station: list detected objects (persons/buses/trains).
        - Glenferrie: display real platform count.
        - Other stations: random simulated platform count (0–3).
        - Train 1: display real passenger count.
        - Other trains (if any): random simulated passenger count (0–10).
        """
        lines = []

        # Stations:
        for station_name, objects in self.detections.items():
            # Show detected names first
            if objects:
                objs = ", ".join(sorted(objects))
                lines.append(f"{station_name} 📡 {objs}")
            else:
                # No detections → show placeholder people
                if station_name == "Glenferrie":
                    real_count = self.people_counts.get("Glenferrie", 0)
                    lines.append(f"{station_name} 📡 (Real Platform Count: {real_count})")
                else:
                    random_count = random.randint(0, 3)
                    lines.append(f"{station_name} 📡 (Simulated Platform: {random_count} people)")

        # Trains (we assume TrainManager has inserted train names into train_counts if Train 1)
        # First, list any detected train names in detections (handled above).
        # Now explicitly show Train 1’s count and random for Train 2, Train 3 if needed:
        # If Train 1 exists in train_counts, show real; otherwise simulated.
        if "Train 1" in self.train_counts:
            real_t1 = self.train_counts["Train 1"]
            ##lines.append(f"Train 1 🚆 (Real Passengers: {real_t1})")
        else:
            # If it hasn’t been set yet, still show placeholder:
            lines.append("Train 1 🚆 (Real Passengers: 0)")

        # Simulate other trains (if you have e.g. Train 2, Train 3 in your app):
        # In this example, we assume at most 2 trains exist from TrainManager:
        # So simulate “Train 2” if you want, or skip if you only built two.
        # We'll simulate up to Train 3 here (you can adjust as needed):
        for i in range(2, 4):
            train_name = f"Train {i}"
            if train_name in self.train_counts:
                # If somehow MQTT inserted a count (unlikely), show it:
                lines.append(f"{train_name} 🚆 (Real Passengers: {self.train_counts[train_name]})")
            else:
                random_count = random.randint(0, 10)
                lines.append(f"{train_name} 🚆 (Simulated Passengers: {random_count})")

        return lines

    def get_station_info(self, station_name):
        """
        Returns three lists: (people, buses, trains) that are currently within the detection radius.
        Used by StationInfoWindow to show which objects are present.
        """
        people_list = []
        bus_list = []
        train_list = []

        for obj_name in self.detections.get(station_name, []):
            if obj_name.startswith("Person"):
                people_list.append(obj_name)
            elif obj_name.startswith("Bus"):
                bus_list.append(obj_name)
            elif obj_name.startswith("Train"):
                train_list.append(obj_name)

        return people_list, bus_list, train_list

    def get_people_count(self, station_name):
        """
        Returns the people count for the station:
        - Glenferrie: return the real count from MQTT (people_counts["Glenferrie"]).
        - Others: return a random 0–3.
        Used by StationInfoWindow to show “People Count: X”.
        """
        if station_name == "Glenferrie":
            return self.people_counts.get("Glenferrie", 0)
        else:
            return random.randint(0, 3)

    def get_train_count(self, train_name):
        """
        Returns the passenger count for the train:
        - Train 1: return the real count from MQTT (train_counts["Train 1"]).
        - Others: return a random 0–10.
        Used by VehicleInfoWindow to show “Passenger Count: X”.
        """
        if train_name == "Train 1":
            return self.train_counts.get("Train 1", 0)
        else:
            return random.randint(0, 10)
