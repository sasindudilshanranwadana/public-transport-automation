from kivy_garden.mapview import MapView, MapMarkerPopup
from kivy.uix.label import Label

class TransportMapView(MapView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Center on Melbourne CBD by default
        self.zoom = 14
        self.lat = -37.8136
        self.lon = 144.9631

    def add_vehicle_marker(self, lat, lon, route, minutes):
        """Place a marker for a vehicle on the map."""
        marker = MapMarkerPopup(lat=lat, lon=lon)
        marker.add_widget(Label(text=f"{route}\n{minutes} min"))
        self.add_widget(marker)

    def clear_markers(self):
        """Remove existing vehicle markers."""
        for child in list(self.children):
            if isinstance(child, MapMarkerPopup):
                self.remove_widget(child)
