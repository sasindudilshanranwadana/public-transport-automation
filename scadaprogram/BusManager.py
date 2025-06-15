
from VehicleManager import VehicleManager
from GridRoadMap import GridRoadMap



class BusManager(VehicleManager):
    def __init__(self, canvas, grid, app_homes, stations):
        super().__init__(canvas)
        self.grid = grid
        self.app_homes = app_homes
        self.stations = list(stations.values())
        self.create_buses()

    def create_buses(self):
        bus_starts = [(750, 100), (550, 300), (200, 100)]
        for i, start_pos in enumerate(bus_starts):
            target_station = self.stations[i % len(self.stations)]
            path_to = self.grid.generate_grid_route(start_pos, target_station)
            path_back = self.grid.generate_grid_route(target_station, start_pos)
            full_route = path_to + path_back
            self.create_vehicle(
                name=f"Bus {i + 1}",
                x=start_pos[0],
                y=start_pos[1],
                speed=1.5,
                color="yellow",
                route=full_route,
                pause_stations=self.stations + self.app_homes
            )
