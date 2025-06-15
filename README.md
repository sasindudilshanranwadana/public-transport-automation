# Public Transport Automation System

An integrated IoT-powered, AI-enhanced, SCADA-controlled real-time public transport synchronization and safety system.

---

## Project Overview

This project is a full-stack smart public transport synchronization system designed to optimize Melbourne's metro network. It integrates hardware-level IoT devices, AI-based computer vision, real-time MQTT communication, and centralized SCADA monitoring to address real-world public transport challenges such as overcrowding, scheduling delays, safety hazards, and lack of real-time data visibility.

---

## System Features

### 1. **Train Occupancy Monitoring System**
- Bidirectional IR sensors detect passenger entry/exit at train doors.
- Arduino microcontroller processes sensor data.
- LCD display shows real-time occupancy inside each train carriage.
- Occupancy data is transmitted via MQTT protocol to central servers.

### 2. **Platform Occupancy Monitoring System**
- Overhead camera streams live video from station platforms.
- Python-based object detection using YOLOv5 deep learning model.
- People counting algorithm extracts real-time crowd estimates.
- Processed data is published to MQTT for central monitoring.

### 3. **Smart Train Door System**
- Motorized sliding doors and retractable platform steps.
- Obstacle detection sensors ensure safe deployment.
- Fully automated door-step mechanism integrated with SCADA.

### 4. **Communication Layer**
- Lightweight MQTT protocol handles real-time messaging.
- Node-RED used for message parsing, business logic, and routing.
- Tailscale VPN mesh ensures secure communication channels.

### 5. **SCADA System**
- Real-time control center developed using OpenSCADA.
- Visualizes occupancy, train positions, and alerts.
- Provides decision support to operators via HMI dashboards.

### 6. **Mobile Application**
- Public-facing app built using PTV OpenAPI.
- Displays real-time train schedules and occupancy data.
- Allows commuters to plan their journeys efficiently.

---

## Technology Stack

- **Programming Languages:** Python, Arduino (C++), JavaScript
- **AI/Computer Vision:** YOLOv5, PyTorch, OpenCV
- **IoT Hardware:** Arduino Uno, IR Sensors, Cameras, LCD Modules
- **Communication:** MQTT (Mosquitto), Node-RED
- **Networking:** Tailscale VPN (WireGuard-based secure overlay)
- **Control Systems:** OpenSCADA (Human Machine Interface)
- **Cloud/Deployment:** Docker, Ubuntu
- **Database:** PostgreSQL
- **APIs:** PTV OpenAPI

---

## Project Architecture

```bash
public-transport-automation/
│
├── scada-system/             # SCADA simulation and monitoring system
├── train-occupancy/          # Arduino IR sensor code and serial-MQTT bridge
├── platform-occupancy/       # YOLOv5 model, people counter script, dataset
├── mqtt-communication/       # Node-RED flows and Mosquitto configs
├── mobile-app/               # PTV OpenAPI integration code (mobile companion app)
├── diagrams/                 # Architecture and system design diagrams
└── README.md
