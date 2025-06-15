import tkinter as tk

class StationInfoWindow:
    def __init__(self, station_name, station_manager, station_radius):
        self.station_name = station_name
        self.station_manager = station_manager
        self.station_radius = station_radius

        self.window = tk.Toplevel()
        self.window.title(f"{station_name} Info")
        self.window.geometry("300x220")

        self.label_station = tk.Label(
            self.window,
            text=f"Station: {station_name}",
            font=("Consolas", 14)
        )
        self.label_station.pack(pady=5)

        self.label_persons = tk.Label(
            self.window,
            text="Persons: Loading...",
            font=("Consolas", 10)
        )
        self.label_persons.pack(pady=5)

        self.label_buses = tk.Label(
            self.window,
            text="Buses: Loading...",
            font=("Consolas", 10)
        )
        self.label_buses.pack(pady=5)

        self.label_trains = tk.Label(
            self.window,
            text="Trains: Loading...",
            font=("Consolas", 10)
        )
        self.label_trains.pack(pady=5)

        self.label_count = tk.Label(
            self.window,
            text="People Count: Loading...",
            font=("Consolas", 10)
        )
        self.label_count.pack(pady=5)

        self.close_btn = tk.Button(
            self.window,
            text="Close",
            command=self.window.destroy
        )
        self.close_btn.pack(pady=10)

        # Start the live update loop
        self.update_info()

    def update_info(self):
        if self.window.winfo_exists():
            people, buses, trains = self.station_manager.get_station_info(self.station_name)

            # Live people count (real for Glenferrie; random for others)
            count = self.station_manager.get_people_count(self.station_name)

            self.label_persons.config(
                text=f"Persons ({len(people)}): {', '.join(people) if people else 'None'}"
            )
            self.label_buses.config(
                text=f"Buses ({len(buses)}): {', '.join(buses) if buses else 'None'}"
            )
            self.label_trains.config(
                text=f"Trains ({len(trains)}): {', '.join(trains) if trains else 'None'}"
            )
            self.label_count.config(text=f"People Count: {count}")

            # Schedule next update in 1 second
            self.window.after(1000, self.update_info)
