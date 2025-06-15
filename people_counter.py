import cv2
import torch
import csv
from datetime import datetime
import time
import paho.mqtt.client as mqtt

# --- CONFIGURATION ---
broker_address = "localhost"  # 🔧 or use your Node-RED or MQTT broker IP
mqtt_topic = "scada/platform_count"  # ✅ UPDATED to match SCADA input topic
station_id = 1  # ✅ Set your station ID (for multi-station setups if needed)

# --- MQTT Setup ---
client = mqtt.Client()
client.connect(broker_address, 1883, 60)
client.loop_start()  # optional: keeps the client responsive

# --- Load YOLOv5 Model ---
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', device='cuda' if torch.cuda.is_available() else 'cpu')
cap = cv2.VideoCapture(0)

# --- Open CSV File ---
with open('people_counts.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'People Count', 'Station ID'])
    last_saved = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        people = [d for d in results.pred[0] if int(d[5]) == 0]
        count = len(people)

        annotated_frame = results.render()[0].copy()
        cv2.putText(annotated_frame, f'People Count: {count}', (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

        # Save every 60 seconds
        current_time = time.time()
        if current_time - last_saved >= 60:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([timestamp, count, station_id])
            print(f"Saved at {timestamp} - People: {count}")

            # --- Publish to MQTT ---
            mqtt_payload = f"{count},{timestamp},{station_id}"  # ✅ includes station ID if needed
            client.publish(mqtt_topic, mqtt_payload)
            print(f"📤 Published to {mqtt_topic}: {mqtt_payload}")

            last_saved = current_time

        cv2.imshow('People Counter', annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
