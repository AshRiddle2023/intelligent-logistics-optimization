# intelligent-logistics-optimization
**MathorCup 2025 project: Hybrid forecasting and multi-objective optimization for urban logistics**

## Problem Summary

The competition focused on **short-distance logistics demand forecasting and vehicle scheduling**. Short-distance transport occurs in the last stage of urban or provincial logistics networks, where goods are delivered from local sorting centers to distribution outlets. This stage is critical for timely delivery, customer experience, and efficient use of transportation resources.

Key tasks included:

1. **Demand Forecasting:** Predict the number of packages for each route for the next day, using available historical and "pre-known" package data. Forecast results were required at **10-minute granularity** to support vehicle scheduling.
2. **Vehicle Scheduling:** Determine the number of vehicles and dispatch times for each route, including "combined dispatch" (串点) when package volumes are low across nearby routes. The goal was to maximize the utilization of **own fleet vehicles** and minimize overall cost, while ensuring all packages are delivered on time.
3. **Container Optimization:** Explore the use of a standard container to shorten loading/unloading time but with reduced capacity, and adjust the vehicle scheduling accordingly.
4. **Robustness Analysis:** Evaluate how forecast deviations affect the scheduling optimization results.

> The full problem description is available in `problem_description/problem_description.pdf`.

## Repository Structure

- problem_description/ # Competition problem statement PDF
- data/ # Original datasets provided by the competition
- code/ # Scripts for forecasting and optimization
- results/ # Generated output Excel files & Final paper

### **Data Description**

- **fleet_routes_info.xlsx** – Contains route information, fleet assignment, transit duration, and cost data (own fleet and external carriers).  
- **packages_10min_granularity.xlsx** – Forecasted package volumes per route at 10-minute intervals.  
- **daily_packages.xlsx** – Daily total package volume per route.  
- **combinable_routes.xlsx** – Defines which stations/routes can be merged for dispatch ("串点").  
- **fleet_info.xlsx** – Number of vehicles owned by each fleet team.

### **Results Description**

- **final_paper.pdf** – Final project report summarizing methodology, forecasting, vehicle scheduling, container optimization, and robustness analysis.
- **daily_freight_volume.xlsx** – Predicted total freight volume per line per day.
- **freight_10min_granularity.xlsx** – Predicted freight volume per line at 10-minute intervals.
- **vehicle_scheduling.xlsx** – Vehicle allocation and dispatch timing based on forecasted freight volume. 
- **container_vehicle_scheduling.xlsx** – Vehicle scheduling plan using standard containers. 

## How to Run

1. Ensure **Python 3.x** is installed.
2. Install required packages.
