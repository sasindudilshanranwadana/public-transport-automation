Public Transport Automation System

An integrated IoT-powered, AI-enhanced, SCADA-controlled real-time public transport synchronization and safety system.

Project Overview

This project is a full-stack smart public transport synchronization system designed to optimize Melbourne's metro network. It integrates hardware-level IoT devices, AI-based computer vision, real-time MQTT communication, and centralized SCADA monitoring to address real-world public transport challenges such as overcrowding, scheduling delays, safety hazards, and lack of real-time data visibility.

System Features

1. Train Occupancy Monitoring System

Bidirectional IR sensors detect passenger entry/exit at train doors.

Arduino microcontroller processes sensor data.

LCD display shows real-time occupancy inside each train carriage.

Occupancy data is transmitted via MQTT protocol to central servers.

2. Platform Occupancy Monitoring System

Overhead camera streams live video from station platforms.

Python-based object detection using YOLOv5 deep learning model.

People counting algorithm extracts real-time crowd estimates.

Processed data is published to MQTT for central monitoring.

3. Smart Train Door System

Motorized sliding doors and retractable platform steps.

Obstacle detection sensors ensure safe deployment.

Fully automated door-step mechanism integrated with SCADA.

4. Communication Layer

Lightweight MQTT protocol handles real-time messaging.

Node-RED used for message parsing, business logic, and routing.

Tailscale VPN mesh ensures secure communication channels.

5. SCADA System

Real-time control center developed using OpenSCADA.

Visualizes occupancy, train positions, and alerts.

Provides decision support to operators via HMI dashboards.

6. Mobile Application

Public-facing app built using PTV OpenAPI.

Displays real-time train schedules and occupancy data.

Allows commuters to plan their journeys efficiently.

Technology Stack

Programming Languages: Python, Arduino (C++), JavaScript

AI/Computer Vision: YOLOv5, PyTorch, OpenCV

IoT Hardware: Arduino Uno, IR Sensors, Cameras, LCD Modules

Communication: MQTT (Mosquitto), Node-RED

Networking: Tailscale VPN (WireGuard-based secure overlay)

Control Systems: OpenSCADA (Human Machine Interface)

Cloud/Deployment: Docker, Ubuntu

Database: PostgreSQL

APIs: PTV OpenAPI

Project Architecture

public-transport-automation/
│
├── scada-system/             # SCADA simulation and monitoring system
├── train-occupancy/          # Arduino IR sensor code and serial-MQTT bridge
├── platform-occupancy/       # YOLOv5 model, people counter script, dataset
├── mqtt-communication/       # Node-RED flows and Mosquitto configs
├── mobile-app/               # PTV OpenAPI integration code (mobile companion app)
├── diagrams/                 # Architecture and system design diagrams
└── README.md

Setup & Installation

1. SCADA System

Extract and run simulation files from scada-system/

Ensure proper connectivity to MQTT broker.

2. Train Occupancy (Arduino IR Sensor)

Upload Bidirectionalcounterserial.ino to Arduino.

Connect IR sensors and LCD as per circuit diagram.

Start serial_to_mqtt_bridge.py to publish serial data to MQTT broker.

3. Platform Occupancy (YOLOv5 People Counter)

Install dependencies:

pip install torch opencv-python paho-mqtt

Place YOLOv5 model (yolov5s.pt) in correct directory.

Run people_counter.py to begin live people detection.

4. MQTT Broker (Mosquitto)

Deploy using Docker with TLS enabled.

Secure broker behind Tailscale VPN.

5. Node-RED

Import provided Node-RED flows for processing vehicle data.

Handle message parsing, routing, and SCADA forwarding.

6. Mobile App

Implemented using PTV OpenAPI to retrieve live public transport schedules.

Fetch occupancy data via MQTT subscription or SCADA API.

Key Deliverables

IoT-based bidirectional occupancy monitoring

AI-based platform people detection

Real-time synchronized SCADA dashboard

Secure end-to-end MQTT communication

Public-facing mobile application for live passenger data

Fully functional smart door & step prototype
