import tkinter as tk

class VehicleInfoWindow:
    def __init__(self, vehicle, title=None):
        self.vehicle = vehicle

        self.window = tk.Toplevel()
        self.window.title(title or f"{vehicle.name} Info")
        self.window.geometry("250x120")

        self.passenger_label = tk.Label(
            self.window,
            text="Passengers: Loading...",
            font=("Consolas", 12)
        )
        self.passenger_label.pack(padx=10, pady=10)

        self.close_btn = tk.Button(self.window, text="Close", command=self.window.destroy)
        self.close_btn.pack(pady=5)

        # Start live update loop
        self.update_passenger_count()

    def update_passenger_count(self):
        if self.window.winfo_exists():
            # Train 1 uses real-time current_occupancy; others have a random or preset list
            if hasattr(self.vehicle, "current_occupancy"):
                passenger_count = self.vehicle.current_occupancy
            else:
                # Fallback (buses/train2) might store .passengers list
                passenger_count = len(self.vehicle.passengers)

            self.passenger_label.config(text=f"Passenger Count: {passenger_count}")
            # Refresh every second
            self.window.after(1000, self.update_passenger_count)
