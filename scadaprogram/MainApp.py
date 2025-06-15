import tkinter as tk
import paho.mqtt.client as mqtt
from StationManager import StationManager
from StationInfoWindow import StationInfoWindow
from AppHomeManager import AppHomeManager
from TrainManager import TrainManager
from MovingObject import MovingObject
from GridRoadMap import GridRoadMap
from BusManager import BusManager
from AppAgentManager import AppAgentManager

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SCADA Simulation - Grid Based Movement")
        self.root.geometry("1200x750")

        self.canvas = tk.Canvas(root, width=1000, height=750, bg="green")
        self.canvas.pack(side="left", padx=10, pady=10)

        self.info_frame = tk.Frame(root, bg="black")
        self.info_frame.pack(side="right", fill="both", padx=10)

        self.status_label = tk.Label(
            self.info_frame,
            text="Status: Initializing...",
            font=("Consolas", 14),
            fg="cyan",
            bg="black",
            wraplength=500,
            justify="left"
        )
        self.status_label.pack(pady=10)

        self.is_paused = False
        self.pause_button = tk.Button(
            self.info_frame,
            text="Pause Simulation",
            font=("Consolas", 12),
            command=self.toggle_pause
        )
        self.pause_button.pack(pady=10)

        self.end_button = tk.Button(
            self.info_frame,
            text="End Simulation",
            font=("Consolas", 12),
            command=self.end_simulation
        )
        self.end_button.pack(pady=10)

        self.objects = []
        self.university_location = (150, 600)
        self.stations = {
            "Richmond": (900, 500),
            "Flagstaff": (450, 100),
            "Dandenong": (50, 300),
            "Glenferrie": (250, 550),
            "Flinders": (250, 700),
        }

        self.grid = GridRoadMap(self.canvas, width=1000, height=750, spacing=50)
        self.grid.draw()

        self.station_manager = StationManager(self.stations, radius=30)
        self.train_manager = TrainManager(self.canvas, self.stations)

        # MQTT Setup
        def on_connect(client, userdata, flags, rc):
            print("Connected to MQTT Broker with result code " + str(rc))
            client.subscribe("scada/platform_count")
            client.subscribe("scada/bus/occupancy/people_count")

        def on_message(client, userdata, msg):
            try:
                payload = msg.payload.decode().strip()
                if not payload.isdigit():
                    print(f"[MQTT Error] Non-numeric payload: {payload}")
                    return

                count = int(payload)
                if msg.topic == "scada/platform_count":
                    self.station_manager.updateStationPeopleCount("Glenferrie", count)
                elif msg.topic == "scada/bus/occupancy/people_count":
                    self.train_manager.updateTrainOccupancy("Train 1", count)

            except Exception as e:
                print(f"[MQTT Error] {e}")

        mqtt_client = mqtt.Client()
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message
        mqtt_client.connect("localhost", 1883, 60)
        mqtt_client.loop_start()

        self.setup_scene()
        self.root.after_idle(self.update_simulation)

    def setup_scene(self):
        self.highlight_university()
        self.draw_stations()

        app_homes = [(900, 300), (750, 200), (450, 300), (200, 100)]
        AppHomeManager(app_homes, self.canvas).draw_homes()

        self.bus_manager = BusManager(self.canvas, self.grid, app_homes, self.stations)
        self.app_agent_manager = AppAgentManager(app_homes, self.canvas, self.university_location, self.bus_manager.vehicles, self.train_manager.vehicles)

        self.objects.extend(self.bus_manager.vehicles + self.train_manager.vehicles + self.app_agent_manager.agents)

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.pause_button.config(text="Resume Simulation" if self.is_paused else "Pause Simulation")

    def end_simulation(self):
        self.root.destroy()

    def update_simulation(self):
        if not self.is_paused:
            self.draw_all_routes()
            for obj in self.objects:
                obj.update_position()
            self.station_manager.check_detections([obj for obj in self.objects if isinstance(obj, MovingObject)])
            self.status_label.config(text="\n".join(self.station_manager.get_status_lines()))
        self.root.after(50, self.update_simulation)

    def highlight_university(self):
        ux, uy = self.university_location
        self.fill_grid_cell(ux, uy, color="brown")
        self.canvas.create_text(ux, uy - 15, text="University", font=("Arial", 12), fill="white")

    def fill_grid_cell(self, x, y, color="lightblue"):
        self.canvas.create_rectangle(x - 35, y - 35, x + 35, y + 35, outline=color, width=2, fill=color)

    def draw_stations(self):
        for name, (x, y) in self.stations.items():
            station_id = self.canvas.create_oval(x - 9, y - 9, x + 8, y + 8, fill="orange", tags="station")
            self.canvas.create_text(x + 45, y - 35, text=name, font=("Arial", 12), fill="orange")
            self.canvas.tag_bind(station_id, "<Button-1>", lambda event, station=name: self.on_station_click(event, station))

    def on_station_click(self, event, station_name):
        StationInfoWindow(station_name, self.station_manager, self.station_manager.radius)

    def draw_routes(self, vehicles, color):
        for vehicle in vehicles:
            if len(vehicle.route) > 1:
                points = [coord for point in vehicle.route for coord in point]
                self.canvas.create_line(*points, fill=color, width=3, dash=(5, 2), tags="paths")

    def draw_all_routes(self):
        self.canvas.delete("paths")
        self.draw_routes(self.bus_manager.vehicles, "yellow")
        self.draw_routes(self.train_manager.vehicles, "red")
