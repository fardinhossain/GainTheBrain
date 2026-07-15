# ☀️ SolarPath AI: Residential Solar Potential & Efficiency Optimizer

## Category / Domain
Climatesphere-ai (Climate / Energy Efficiency)

## Date
2026-07-15

## Short Description
SolarPath AI is a web-based platform that uses satellite imagery and machine learning to analyze residential rooftops, calculate their solar energy potential, and provide a detailed ROI (Return on Investment) analysis for homeowners considering solar panel installation.

## Problem Statement
Many homeowners are interested in renewable energy but are deterred by the complexity of calculating whether solar panels are a viable investment for their specific property. Factors like roof orientation, pitch, shading from nearby trees or buildings, and local weather patterns are difficult for a layperson to quantify. Existing tools are often either too generic or serve as biased lead-generation tools for specific installers.

## Proposed Solution
SolarPath AI provides an objective, data-driven assessment. By entering an address, the system fetches high-resolution satellite imagery, uses computer vision to segment the roof and identify obstructions, and combines this with historical meteorological data to simulate annual energy production. It then cross-references this with local utility rates to provide a clear financial outlook.

## Target Users
- **Homeowners:** Looking to reduce energy costs and carbon footprints.
- **Real Estate Agents:** Wanting to highlight the solar potential of a listing.
- **Small Solar Installers:** Needing a quick, automated tool for preliminary site assessments.
- **Sustainability Consultants:** Helping clients transition to green energy.

## Core Features
- **Address Search & Mapping:** Integration with Map APIs (Google Maps/Mapbox) to locate and visualize the property.
- **Automated Roof Analysis:** Using AI to detect roof area, orientation (azimuth), and pitch.
- **Shadow Mapping:** Identifying potential shading from surrounding structures or vegetation using 3D building data or image shadows.
- **Energy Yield Simulation:** Calculation of monthly and annual kWh production based on local irradiance data.
- **Financial ROI Calculator:** Estimating payback periods, net savings, and environmental impact (CO2 offset).

## Advanced Features
- **Battery Storage Simulation:** Modeling the impact of adding a home battery (e.g., Tesla Powerwall) on energy independence.
- **Regulatory & Incentive Database:** Automatically pulling local tax credits and state-level solar incentives based on the user's ZIP code.
- **Dynamic Weather Integration:** Using real-time weather forecasts to predict the upcoming week's energy production.
- **AR Visualization:** A mobile view allowing users to point their phone at their roof to see a 3D overlay of suggested panel placement.

## AI/ML Integration
- **Computer Vision (Segmentation):** A U-Net or Mask R-CNN model trained on satellite datasets to segment roof facets and identify obstacles like chimneys or HVAC units.
- **Regression Modeling:** A model trained on historical solar production data (e.g., PVWatts) to predict energy yield based on tilt, azimuth, and location-specific irradiance.
- **Time-Series Analysis:** To process and predict solar irradiance patterns from historical meteorological datasets.

## Suggested Tech Stack
- **Frontend:** React.js or Next.js with Tailwind CSS for a responsive dashboard.
- **Backend:** FastAPI (Python) to handle heavy ML computations and API requests.
- **Machine Learning:** PyTorch or TensorFlow for image segmentation; Scikit-learn for ROI regression.
- **Database:** PostgreSQL with PostGIS for spatial data management.
- **APIs:** Google Static Maps API (Satellite view), OpenWeatherMap (Solar Irradiance API), and NREL PVWatts API.

## Database Design
- **Users:** ID, email, password_hash, saved_reports_count.
- **Properties:** ID, user_id, address, latitude, longitude, roof_area, orientation_angle.
- **Simulations:** ID, property_id, estimated_annual_kwh, estimated_savings, setup_cost, payback_years.
- **Incentives:** ID, state_code, incentive_type, amount, expiration_date.

## API Route Ideas
- `POST /api/analyze-property`: Accepts an address, triggers image fetching and ML analysis.
- `GET /api/simulation/{id}`: Retrieves the results of a specific solar simulation.
- `GET /api/incentives/{zipcode}`: Fetches local rebates and tax credits.
- `POST /api/save-report`: Allows registered users to save their analysis.

## UI Pages
- **Landing Page:** Educational content on solar energy and a prominent address search bar.
- **Dashboard:** Interactive map view with an overlay of the analyzed roof facets.
- **Results/ROI Page:** Detailed charts showing monthly energy production vs. consumption and financial charts (NPV, Payback period).
- **Comparison Tool:** Compare different panel types (Monocrystalline vs. Polycrystalline) or battery options.

## MVP Plan
1. Implement address search and satellite image retrieval.
2. Develop a basic ML model to identify roof area from the image.
3. Integrate the NREL PVWatts API to calculate energy yield based on coordinates and area.
4. Build a simple ROI calculator using average electricity rates.
5. Launch a single-page app where users can get a PDF report of their results.

## Future Scope
- **Community Solar Integration:** Connecting users with local community solar projects if their own roof is not viable.
- **IoT Integration:** Connecting to smart meters to pull real energy consumption data for more accurate modeling.
- **B2B API:** Licensing the analysis engine to real estate platforms like Zillow or Redfin.

## Difficulty Level
Intermediate

## Portfolio Value
- Demonstrates proficiency in **Computer Vision** and spatial data processing.
- Shows the ability to integrate multiple third-party APIs (Maps, Weather, Energy Data).
- High **environmental impact** relevance, making it attractive to Green-Tech recruiters.
- Combines complex backend logic with a clean, user-centric frontend.

## Possible Monetization
- **Lead Generation:** Referral fees from solar installation companies.
- **Premium Reports:** Charging a small fee for highly detailed 10-year financial forecasts.
- **SaaS for Real Estate:** Subscription for realtors to generate reports for clients.

## Learning Outcomes
- Handling Geospatial data and coordinate systems.
- Implementing and deploying Computer Vision models for image segmentation.
- Financial modeling and time-series data visualization.
- Building a full-stack application that solves a real-world environmental problem.
