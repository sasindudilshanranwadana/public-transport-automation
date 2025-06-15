# mobile.main.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A Kivy-based public transport companion app with KV-defined UI.
- Starts GPS (Android only via Plyer)
- Posts location to backend
- Plans trips (including Lilydale example)
- Makes payments
"""
import threading
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from plyer import gps
from kivy.utils import platform
# Configuration: change to your backend base URL
BASE_URL = "http://localhost:8000"

# KV layout embedded
KV = '''    
<TransportUI>:
    # Root background
    canvas.before:
        Color:
            rgba: 0.737, 0.255, 0.169, 1   # Persian red
        Rectangle:
            pos: self.pos
            size: self.size

    orientation: 'vertical'
    padding: '12dp'
    spacing: '12dp'

    ################################
    # 1. GPS Status Section        #
    ################################
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: '80dp'
        padding: '8dp'
        spacing: '8dp'
        canvas.before:
            Color:
                rgba: 0.880, 0.960, 0.880, 1  # light-green bg
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [16]

        Label:
            text: 'GPS Status'
            size_hint_y: None
            height: '24dp'
            font_size: '16sp'
            bold: True
            color: 0, 0, 0, 1

        BoxLayout:
            spacing: '10dp'
            Label:
                id: status_label
                text: 'Initializing…'
                font_size: '14sp'
                color: 0, 0, 0, 1
            Label:
                id: lat_label
                text: 'Lat: --'
                font_size: '14sp'
                color: 0, 0, 0, 1
            Label:
                id: lon_label
                text: 'Lon: --'
                font_size: '14sp'
                color: 0, 0, 0, 1

    ################################
    # 2. Nearby Vehicles Section   #
    ################################
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 0.3
        padding: '8dp'
        spacing: '8dp'
        canvas.before:
            Color:
                rgba: 0.95, 0.95, 0.95, 1   # off-white bg
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [16]

        Label:
            text: 'Nearby Vehicles'
            size_hint_y: None
            height: '24dp'
            font_size: '16sp'
            bold: True
            color: 0, 0, 0, 1

        ScrollView:
            GridLayout:
                id: vehicles_list
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: '5dp'
                padding: '5dp'

    ################################
    # 3. Trip Planner Section      #
    ################################
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: '120dp'
        padding: '8dp'
        spacing: '8dp'
        canvas.before:
            Color:
                rgba: 0.95, 0.95, 0.95, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [16]

        Label:
            text: 'Plan Your Trip'
            size_hint_y: None
            height: '24dp'
            font_size: '16sp'
            bold: True
            color: 0, 0, 0, 1

        BoxLayout:
            spacing: '8dp'
            TextInput:
                id: dest_input
                hint_text: 'Enter destination'
                multiline: False
                foreground_color: 0, 0, 0, 1
                background_color: 1, 1, 1, 1
            Button:
                text: 'Plan'
                size_hint_x: None
                width: '80dp'
                background_color: 0.020, 0.659, 0.667, 1
                color: 1, 1, 1, 1
                on_press: root.on_plan()

        BoxLayout:
            spacing: '8dp'
            Button:
                text: 'Quick Lilydale Trip'
                on_press: root.on_plan_lilydale()
            Label:
                id: plan_result
                text: ''
                valign: 'middle'
                font_size: '14sp'
                color: 0, 0, 0, 1

    ################################
    # 4. Payment Section           #
    ################################
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: '100dp'
        padding: '8dp'
        spacing: '8dp'
        canvas.before:
            Color:
                rgba: 0.95, 0.95, 0.95, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [16]

        Label:
            text: 'Make Payment'
            size_hint_y: None
            height: '24dp'
            font_size: '16sp'
            bold: True
            color: 0, 0, 0, 1

        BoxLayout:
            spacing: '8dp'
            TextInput:
                id: trip_id_input
                hint_text: 'Trip ID'
                multiline: False
                foreground_color: 0, 0, 0, 1
                background_color: 1, 1, 1, 1
            TextInput:
                id: amount_input
                hint_text: 'Amount'
                input_filter: 'float'
                multiline: False
                foreground_color: 0, 0, 0, 1
                background_color: 1, 1, 1, 1
            Button:
                text: 'Pay'
                size_hint_x: None
                width: '80dp'
                background_color: 0.020, 0.659, 0.667, 1
                color: 1, 1, 1, 1
                on_press: root.on_pay()

        Label:
            id: pay_result
            text: ''
            size_hint_y: None
            height: '24dp'
            font_size: '14sp'
            color: 0, 0, 0, 1

'''

# Load the KV definition
Builder.load_string(KV)


def post_location(lat, lon):
    try:
        requests.post(f"{BASE_URL}/location", json={"lat": lat, "lon": lon}, timeout=5)
    except requests.RequestException:
        pass


def fetch_vehicles(lat, lon):
    try:
        resp = requests.get(f"{BASE_URL}/vehicles", params={"lat": lat, "lon": lon}, timeout=5)
        return resp.json()
    except requests.RequestException:
        return []


def plan_trip_request(origin_lat, origin_lon, destination):
    try:
        resp = requests.post(f"{BASE_URL}/plan", json={"origin": {"lat": origin_lat, "lon": origin_lon}, "destination": destination}, timeout=10)
        return resp.json()
    except requests.RequestException:
        return {"error": "Request failed"}


def make_payment(trip_id, amount):
    try:
        resp = requests.post(f"{BASE_URL}/payment", json={"trip_id": trip_id, "amount": amount}, timeout=5)
        return resp.json()
    except requests.RequestException:
        return {"error": "Payment failed"}


class TransportUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if platform == "android":
            Clock.schedule_once(self.start_gps, 1)
        else:
            self.on_location(lat="-37.8100", lon="144.9600")
            self.ids.status_label.text = "GPS unavailable on desktop"

    def start_gps(self, dt):
        try:
            gps.configure(on_location=self.on_location, on_status=self.on_status)
            gps.start(minTime=1000, minDistance=1)
        except NotImplementedError:
            self.ids.status_label.text = "GPS backend not implemented"

    def on_location(self, **kwargs):
        lat, lon = float(kwargs.get("lat")), float(kwargs.get("lon"))
        self.current_lat, self.current_lon = lat, lon
        threading.Thread(target=post_location, args=(lat, lon), daemon=True).start()
        self.ids.lat_label.text = f"Lat: {lat:.5f}"
        self.ids.lon_label.text = f"Lon: {lon:.5f}"
        self.ids.status_label.text = "GPS: active"

    def on_status(self, stype, status):
        self.ids.status_label.text = f"GPS {stype}: {status}"

    def on_nearest(self):
        threading.Thread(target=self._load_nearest, daemon=True).start()

    def _load_nearest(self):
        data = fetch_vehicles(self.current_lat, self.current_lon)
        def update(dt):
            grid = self.ids.vehicles_list
            grid.clear_widgets()
            from kivy.uix.label import Label as KLabel
            for v in data:
                grid.add_widget(KLabel(text=f"{v['route']} in {v['minutes']} min", size_hint_y=None, height='30dp', color=(0,0,0,1)))
        Clock.schedule_once(update, 0)

    def on_plan(self):
        threading.Thread(target=self._do_plan, daemon=True).start()

    def _do_plan(self):
        dest = self.ids.dest_input.text.strip()
        result = plan_trip_request(self.current_lat, self.current_lon, dest)
        text = result.get('error') or f"Trip ID: {result.get('trip_id')}\nETA: {result.get('eta','N/A')}"
        Clock.schedule_once(lambda dt: setattr(self.ids.plan_result, 'text', text), 0)

    def on_plan_lilydale(self):
        origin_lat, origin_lon = -37.8136, 144.9631
        dest = "Lilydale"
        threading.Thread(target=self._do_plan_lilydale, args=(origin_lat, origin_lon, dest), daemon=True).start()

    def _do_plan_lilydale(self, lat, lon, dest):
        result = plan_trip_request(lat, lon, dest)
        if "error" in result:
            text = f"Error: {result['error']}"
        else:
            text = f"Lilydale Trip → ID: {result.get('trip_id')}\nETA: {result.get('eta','N/A')}"
        Clock.schedule_once(lambda dt: setattr(self.ids.plan_result, 'text', text), 0)

    def on_pay(self):
        threading.Thread(target=self._do_pay, daemon=True).start()

    def _do_pay(self):
        trip_id = self.ids.trip_id_input.text.strip()
        try:
            amount = float(self.ids.amount_input.text)
        except ValueError:
            amount = 0.0
        result = make_payment(trip_id, amount)
        text = result.get('error') or f"Payment status: {result.get('status')}"
        Clock.schedule_once(lambda dt: setattr(self.ids.pay_result, 'text', text), 0)


class TransportApp(App):
    def build(self):
        return TransportUI()


if __name__ == "__main__":
    TransportApp().run()