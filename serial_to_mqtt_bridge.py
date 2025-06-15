
import serial
import paho.mqtt.client as mqtt
import time

# === CONFIGURATION ===
SERIAL_PORT = 'COM3'  # Change this to your actual port (e.g., 'COM4' or '/dev/ttyUSB0')
BAUD_RATE = 9600

MQTT_BROKER = '100.85.1.16'  # Ruwin's Mosquitto broker IP
MQTT_PORT = 1883
MQTT_TOPIC = 'bus/occupancy/people_count'

# === SETUP SERIAL & MQTT ===
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
except serial.SerialException:
    print(f"❌ Could not open serial port {SERIAL_PORT}. Check the connection.")
    exit(1)

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

print(f"✅ Serial-to-MQTT bridge started. Listening on {SERIAL_PORT}...")
time.sleep(2)

# === MAIN LOOP ===
while True:
    try:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            if line.isdigit():
                print(f"📤 Publishing count: {line}")
                client.publish(MQTT_TOPIC, line)
    except Exception as e:
        print(f"⚠️ Error: {e}")
