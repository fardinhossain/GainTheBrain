# ⚡ VoltSentry AI: Electrical Signature Analysis for Predictive Industrial Safety

## Category / Domain
**IndustrySphere AI** (Industrial Automation / IoT / Safety)

## Date
2026-08-12

## Short Description
VoltSentry AI is a high-frequency electrical monitoring platform that uses Non-Intrusive Load Monitoring (NILM) and Deep Learning to detect equipment degradation, prevent electrical fires, and optimize energy consumption at the circuit-breaker level without requiring sensors on every individual machine.

## Problem Statement
Industrial facilities face two major electrical challenges: catastrophic equipment failure and fire hazards. Conventional thermal imaging and manual inspections are periodic and reactive. Furthermore, monitoring every motor, pump, or HVAC unit with individual IoT sensors is cost-prohibitive and complex to maintain. Electrical faults, such as arc faults or harmonic distortions, often go unnoticed until a breakdown occurs, leading to expensive downtime or safety incidents.

## Proposed Solution
VoltSentry AI utilizes high-frequency sampling of current and voltage signatures at a single point (the electrical panel). By applying machine learning to these "electrical fingerprints," the system can disaggregate the total load into individual machine signatures. It monitors for Total Harmonic Distortion (THD), transient surges, and micro-arcs that indicate insulation breakdown or bearing wear, providing real-time alerts before a failure occurs.

## Target Users
- **Factory Maintenance Managers**: To transition from scheduled to predictive maintenance.
- **Facility Engineers**: To monitor the health of critical infrastructure (elevators, HVAC, pumps).
- **Industrial Safety Officers**: To mitigate fire risks from electrical aging.
- **Sustainability Officers**: To identify energy-inefficient machinery.

## Core Features
- **Load Disaggregation (NILM)**: Identify the energy footprint of individual machines from a single monitoring point.
- **Health Scoring**: Real-time health index for every connected machine based on its electrical signature.
- **Anomaly Detection**: Instant alerts for arc faults, phase imbalances, and overheating signatures.
- **Energy Audit Dashboard**: Visualize peak demand periods and identify "vampire loads" or inefficient equipment.
- **Reporting Engine**: Weekly PDF reports on asset health and predicted remaining useful life (RUL).

## Advanced Features
- **Digital Twin Integration**: Map electrical signatures to a 3D model of the facility.
- **Edge Processing**: Real-time FFT (Fast Fourier Transform) processing on edge devices to reduce cloud bandwidth.
- **Predictive Fire Modeling**: Correlate electrical transients with environmental humidity/temp to predict high-risk fire conditions.
- **Multi-Site Benchmarking**: Compare equipment performance across different factory locations.

## AI/ML Integration
- **Signal Processing**: Fast Fourier Transform (FFT) and Wavelet Transform for feature extraction from raw AC waveforms.
- **Deep Learning**: Convolutional Neural Networks (CNN) for image-like pattern recognition of V-I (Voltage-Current) trajectories.
- **Sequence Modeling**: LSTM (Long Short-Term Memory) or Transformers to analyze temporal degradation patterns over weeks.
- **Unsupervised Learning**: Isolation Forests for detecting novel electrical anomalies that haven't been seen before.

## Suggested Tech Stack
- **Edge Hardware**: Raspberry Pi 4 or ESP32 with high-speed ADC (Analog-to-Digital Converter) and CT clamps.
- **Backend**: FastAPI (Python) for high-performance data ingestion.
- **Database**: InfluxDB (Time-series data for electrical metrics) and PostgreSQL (Metadata/User management).
- **ML Framework**: PyTorch or TensorFlow for signal classification.
- **Frontend**: React.js with D3.js or Highcharts for complex waveform visualization.
- **Messaging**: MQTT (Mosquitto) for real-time edge-to-cloud communication.

## Database Design
- **Sensors Table**: Metadata for edge devices, installation locations, and phase configurations.
- **Assets Table**: Machine types (e.g., 5HP Induction Motor), expected signatures, and maintenance history.
- **Telemetry (InfluxDB)**: High-resolution current, voltage, power factor, and THD readings.
- **Alerts Table**: Log of anomalies detected, severity levels, and resolution status.

## API Route Ideas
- `GET /api/v1/dashboard/overview`: Summary of total power and active machine health.
- `GET /api/v1/assets/{id}/waveform`: Fetch real-time V-I trajectory for a specific machine.
- `POST /api/v1/alerts/ack`: Acknowledge and categorize an electrical anomaly.
- `GET /api/v1/analytics/energy-saving`: Recommendations for peak-shaving and equipment replacement.

## UI Pages
- **Live Monitoring View**: Real-time scrolling charts of current/voltage and active machine list.
- **Asset Health Matrix**: A grid of all machines color-coded by health (Green/Yellow/Red).
- **Signature Analysis Lab**: A tool for engineers to inspect raw waveforms and FFT results.
- **Alert Configuration**: Setting thresholds for specific harmonic frequencies and power surges.

## MVP Plan
1. Develop a Python script to simulate high-frequency electrical data for 3 machine types (Motor, Heater, LED Lighting).
2. Build the NILM model to identify when each machine is ON/OFF from the combined signal.
3. Implement basic anomaly detection (over-current and phase imbalance).
4. Create a React dashboard to display real-time status and alerts.
5. Deploy the backend using Docker and connect to a mock MQTT broker.

## Future Scope
- **Integration with ERP**: Automatically generate work orders in SAP or Jira when a machine is predicted to fail.
- **Mobile App**: Augmented Reality (AR) view to see machine health by pointing a phone at the electrical panel.
- **Hardware Kit**: Developing a custom PCB for 100kHz sampling rates for finer signature resolution.

## Difficulty Level
Advanced

## Portfolio Value
This project demonstrates mastery of high-frequency data processing, signal analysis, and complex ML disaggregation. It addresses a multi-billion dollar industrial problem (downtime and safety), making it highly attractive to companies in the IoT, Energy, and Manufacturing sectors.

## Possible Monetization
- **SaaS Subscription**: Monthly fee per monitored electrical panel.
- **Energy Consulting**: Taking a percentage of the energy savings identified by the AI.
- **Insurance Partnerships**: Lower premiums for factories that utilize 24/7 AI hazard monitoring.

## Learning Outcomes
- Advanced signal processing techniques (FFT, Wavelets).
- Implementing Non-Intrusive Load Monitoring (NILM) algorithms.
- Managing high-throughput time-series data at scale.
- Bridging the gap between hardware (IoT sensors) and high-level AI insights.
