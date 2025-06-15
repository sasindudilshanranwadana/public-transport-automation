from VehicleManager import VehicleManager
import random

class TrainManager(VehicleManager):
    def __init__(self, canvas, stations):
        super().__init__(canvas)
        self.station_positions = list(stations.values())
        self.create_trains()

    def create_trains(self):
        """
        Create two trains (Train 1 and Train 2) along the first two station positions.
        Train 1: will have real-time occupancy updated via MQTT.
        Train 2: will use a random occupancy.
        """
        for i, (x, y) in enumerate(self.station_positions[:2]):
            route = self.station_positions[i:] + [self.station_positions[0]]
            vehicle = self.create_vehicle(
                name=f"Train {i + 1}",
                x=x,
                y=y,
                speed=2,
                color="gray" if i % 2 == 0 else "pink",
                route=route,
                pause_stations=self.station_positions
            )

            # Initialize occupancy:
            if vehicle.name == "Train 1":
                vehicle.current_occupancy = 0
            else:
                vehicle.current_occupancy = random.randint(0, 10)

    def updateTrainOccupancy(self, train_name, count):
        """
        Called by MainApp when an MQTT message arrives for 'scada/bus/occupancy/people_count'.
        Only "Train 1" will be updated.
        """
        for vehicle in self.vehicles:
            if vehicle.name == train_name:
                vehicle.current_occupancy = count
                print(f"[TrainManager] {train_name} occupancy updated: {count}")
                break
