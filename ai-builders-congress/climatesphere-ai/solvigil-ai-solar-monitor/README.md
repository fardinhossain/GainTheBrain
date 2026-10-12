# ☀️ SolVigil AI: Intelligent Solar Soiling & Degradation Monitor

## Category / Domain
ClimateSphere AI (Renewable Energy & Environmental Efficiency)

## Date
2026-10-12

## Short Description
An IoT and AI-powered platform that monitors solar panel arrays to detect "soiling" (dust, grime, bird droppings) and hardware degradation, providing data-driven cleaning schedules and ROI analysis for maintenance.

## Problem Statement
Solar panel efficiency drops significantly—sometimes by over 25%—due to the accumulation of dust, pollutants, and debris, a phenomenon known as "soiling." Commercial solar farm operators and residential owners currently rely on fixed cleaning schedules or manual inspections, which are either wasteful (cleaning clean panels) or costly (leaving dirty panels uncleaned). Furthermore, distinguishing between temporary soiling and permanent hardware degradation (micro-cracks or PID) is difficult without specialized, expensive equipment.

## Proposed Solution
SolVigil AI uses a combination of IoT sensors (measuring light intensity vs. electrical output) and weather data to create a digital twin of the solar array. By comparing the theoretical maximum output (based on real-time irradiance) with actual performance, the AI detects soiling patterns. It predicts exactly when the cost of cleaning will be lower than the value of the energy lost, optimizing maintenance for maximum financial and environmental ROI.

## Target Users
- **Commercial Solar Farm Operators:** To optimize utility-scale maintenance.
- **Smart Home Enthusiasts:** To manage residential PV systems.
- **Renewable Energy Asset Managers:** To monitor portfolio-wide performance.
- **Solar Installation Companies:** As a value-add monitoring service for clients.

## Core Features
- **IoT Sensor Integration:** Real-time data ingestion from ESP32/Arduino sensors measuring current, voltage, and ambient light (irradiance).
- **Performance Gap Analysis:** Real-time comparison of actual vs. expected power output.
- **Weather Correlation:** Integration with weather APIs to factor in rain (natural cleaning) and dust storms (soiling events).
- **Maintenance Dashboard:** Visual heatmaps of a solar array showing which panels are underperforming.
- **Alerting System:** Notifications for sudden drops in efficiency or suspected hardware failure.

## Advanced Features
- **Economic ROI Calculator:** Calculates the exact dollar amount lost to soiling and predicts the "break-even" day for a professional cleaning service.
- **Degradation Fingerprinting:** Uses ML to distinguish between soiling (which clears after rain/cleaning) and long-term cell degradation.
- **Satellite Cross-Referencing:** Uses satellite-derived irradiance data for systems without dedicated light sensors.
- **Cleaning Robot Integration:** API hooks to trigger autonomous cleaning robots when efficiency drops below a threshold.

## AI/ML Integration
- **Regression Models:** To predict the rate of soiling based on local historical air quality and weather patterns.
- **Anomaly Detection:** An Isolation Forest or Autoencoder model to identify panels behaving differently from their neighbors in the same string.
- **Time-Series Forecasting:** Predicting future energy yield based on current soiling trends and 7-day weather forecasts.

## Suggested Tech Stack
- **IoT Hardware:** ESP32, INA219 (Current/Power sensor), BH1750 (Ambient Light sensor).
- **Backend:** Python (FastAPI) for high-performance data ingestion.
- **Database:** TimescaleDB or InfluxDB (for time-series sensor data) + PostgreSQL (for user/asset metadata).
- **Frontend:** React with Recharts or D3.js for complex energy performance visualizations.
- **ML Framework:** Scikit-learn or Prophet for time-series forecasting.
- **Communication:** MQTT or WebSockets for real-time sensor-to-server data transmission.

## Database Design
- **Assets Table:** `id, user_id, location_lat, location_long, panel_count, rated_wattage`.
- **Telemetry Table:** `timestamp, asset_id, panel_index, voltage, current, irradiance, temperature`.
- **Weather_Logs Table:** `timestamp, location_id, cloud_cover, rainfall, pm25_index`.
- **Maintenance_Events Table:** `id, asset_id, event_type (cleaning/repair), cost, timestamp`.

## API Route Ideas
- `POST /api/v1/telemetry`: Endpoint for IoT devices to push sensor data.
- `GET /api/v1/analytics/soiling-loss`: Returns the percentage of energy lost to dirt vs. theoretical max.
- `GET /api/v1/maintenance/schedule`: Returns the recommended next cleaning date based on ROI.
- `POST /api/v1/assets/register`: Connect a new solar array/IoT gateway to the account.

## UI Pages
- **Fleet Overview:** A high-level map showing all managed solar sites and their current health status.
- **Site Detail View:** Detailed charts showing Power vs. Irradiance, historical trends, and efficiency gap.
- **ROI Analytics:** A financial-focused page showing "Money Lost Today" and "Cost of Cleaning" projections.
- **Hardware Diagnostics:** A technical view for identifying specific faulty panels or strings.

## MVP Plan
1. Build the IoT prototype using an ESP32 and a small 5V solar cell to simulate a panel.
2. Develop the FastAPI backend to store voltage/current data in a time-series database.
3. Implement the basic "Expected vs. Actual" calculation using a weather API for local irradiance.
4. Create a React dashboard to visualize the real-time efficiency gap.
5. Integrate a basic linear regression model to predict the next cleaning date.

## Future Scope
- **Community Benchmarking:** Allow users to compare their panel performance with neighbors to identify hyper-local issues (e.g., a nearby construction site causing dust).
- **Insurance Integration:** Provide verified data to insurance companies for claims related to hail damage or hardware failure.
- **Mobile App:** A React Native app for field technicians to locate dirty panels using AR (Augmented Reality).

## Difficulty Level
Advanced (Requires integration of hardware, time-series data, and predictive modeling).

## Portfolio Value
- Demonstrates expertise in **IoT/Hardware** integration with cloud services.
- Showcases ability to handle **Time-Series Data** and complex mathematical modeling.
- Highlights commitment to **ClimateTech** and sustainable energy solutions.
- Perfect for roles in Green Energy, Systems Engineering, or Full-Stack Data Science.

## Possible Monetization
- **SaaS Subscription:** For commercial solar operators (Per-MW-monitored fee).
- **Freemium Model:** Free for individual homeowners with 1 site; paid for multiple sites.
- **B2B Partnership:** Licensing the software to solar installation companies to provide white-labeled monitoring to their customers.

## Learning Outcomes
- Master **Time-Series Database** management and optimization.
- Understand the physics of **Photovoltaic energy conversion** and environmental impacts.
- Build a robust **IoT-to-Cloud** pipeline with security and low latency.
- Implement **Predictive Maintenance** algorithms that solve real-world economic problems.
