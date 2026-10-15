# 🚲 SafeCycle AI: Intelligent Bicycle Collision Avoidance & Blind-Spot Radar

## Category / Domain
iot-embedded / Artificial Intelligence

## Date
2026-10-15

## Short Description
SafeCycle AI is a smart, rear-mounted IoT device for bicycles that uses computer vision and LiDAR sensors to detect approaching vehicles, calculate collision risks, and provide real-time haptic and visual alerts to the cyclist.

## Problem Statement
Cyclists face significant risks from rear-end collisions and "side-swiping" by vehicles overtaking too closely or at high speeds. Most existing solutions are either passive (mirrors) or high-end proprietary radars (like Garmin Varia) that offer limited data. There is a lack of an open, intelligent system that not only detects presence but classifies vehicle types, estimates speed, and records "near-miss" incidents for infrastructure advocacy.

## Proposed Solution
A hardware-software hybrid system consisting of a rear-mounted unit (ESP32-S3 or Raspberry Pi Zero 2W) equipped with a wide-angle camera and a LiDAR sensor. The system processes video frames locally to detect vehicles and uses LiDAR to measure precise distance and closing speed. When a high-risk approach is detected, the device triggers haptic feedback (vibrating handlebars) and a visual indicator on a smartphone or handlebar-mounted LED strip.

## Target Users
- Urban commuters.
- Long-distance road cyclists.
- Delivery riders.
- City planners (using anonymized near-miss data).

## Core Features
- **Real-time Vehicle Detection:** Identifies cars, trucks, and buses approaching from behind.
- **Distance & Speed Calculation:** Uses LiDAR to determine the "Time-to-Collision" (TTC).
- **Multi-Level Alerting:** Green (safe), Yellow (approaching), Red (high-speed/close-proximity danger).
- **Haptic Feedback:** Wireless handlebar vibration unit to alert the rider without requiring them to look down.
- **Black-Box Recording:** Automatically saves video clips of incidents where a vehicle passes within a dangerous threshold (e.g., < 1 meter).

## Advanced Features
- **Overtaking Quality Index:** Rates the safety of passing drivers and logs data to a cloud map.
- **Automated Emergency SOS:** Detects falls (via accelerometer) following a collision and sends GPS coordinates to emergency contacts.
- **Smart Tail-light:** Increases LED brightness and flash frequency as a vehicle approaches to improve cyclist visibility.
- **Mesh Networking:** Allows a group of cyclists to share radar data, alerting the front of the pack when a car is approaching the rear.

## AI/ML Integration
- **Edge Computer Vision:** A quantized YOLOv8-tiny or MobileNetV2 model running on the edge to classify objects in the rear-view feed.
- **Anomaly Detection:** An LSTM or 1D-CNN model to analyze trajectory data from the LiDAR and predict erratic driving behavior (e.g., swerving).
- **Distance Estimation:** A regression model that fuses camera bounding box size changes with LiDAR data for high-accuracy distance tracking.

## Suggested Tech Stack
- **Hardware:** Raspberry Pi Zero 2W (for vision) or ESP32-S3 (for low-power sensor fusion).
- **Sensors:** TF-Luna LiDAR, OV2640 Camera, MPU6050 Accelerometer/Gyroscope.
- **Firmware:** MicroPython or C++ (Arduino/ESP-IDF).
- **Mobile App:** Flutter or React Native for the dashboard and configuration.
- **Communication:** BLE (Bluetooth Low Energy) for device-to-phone and device-to-haptics.
- **Backend (Optional):** Node.js with PostgreSQL/PostGIS for mapping near-miss hotspots.

## Database Design
- **Incidents Table:** `id`, `timestamp`, `latitude`, `longitude`, `video_clip_url`, `min_distance`, `vehicle_type`.
- **Ride_Logs Table:** `id`, `user_id`, `start_time`, `end_time`, `total_near_misses`.
- **Hotspots Table:** `id`, `location_geom`, `incident_count`, `risk_score`.

## API Route Ideas
- `POST /api/incidents/upload`: Uploads telemetry and metadata for a near-miss event.
- `GET /api/map/hotspots`: Returns GeoJSON of dangerous cycling areas based on community data.
- `POST /api/user/emergency-contacts`: Manages SMS alert recipients.

## UI Pages
- **Live Radar Dashboard:** Visual representation of vehicles behind the cyclist (dots moving on a vertical lane).
- **Ride History:** Map view of previous rides with highlighted danger zones.
- **Device Settings:** Calibration for sensor sensitivity and alert thresholds.
- **Community Heatmap:** Global map of reported incidents.

## MVP Plan
1. Assemble hardware: ESP32-S3, LiDAR, and simple LED buzzer.
2. Implement basic distance-based alerting using LiDAR only.
3. Integrate camera and deploy a basic object detection model (Car vs. No Car).
4. Build a basic Flutter app to receive alerts via BLE.
5. Create a 3D-printed enclosure for seat-post mounting.

## Future Scope
- **Solar-Powered Enclosure:** Integration of small solar panels for extended battery life.
- **AI Voice Coaching:** Audio alerts via bone-conduction headphones (e.g., "Truck approaching fast on left").
- **V2X Integration:** Future-proofing for Vehicle-to-Everything communication protocols.

## Difficulty Level
Advanced (Requires hardware assembly, edge AI optimization, and low-latency wireless communication).

## Portfolio Value
- Demonstrates expertise in **Edge AI** and hardware-software integration.
- Showcases ability to handle **real-time data processing** and sensor fusion.
- High social impact: Addresses a real-world safety problem for millions of cyclists.

## Possible Monetization
- **Hardware Sales:** Selling the DIY kit or pre-assembled units.
- **Premium App Features:** Advanced analytics, cloud video storage, and group-ride features.
- **Data Licensing:** Providing anonymized near-miss data to urban planners and insurance companies.

## Learning Outcomes
- Deep understanding of **Edge Computing** and model quantization.
- Practical experience with **LiDAR and Computer Vision** sensor fusion.
- Mastery of **BLE (Bluetooth Low Energy)** communication protocols.
- Developing for **low-power environments** and thermal management.
