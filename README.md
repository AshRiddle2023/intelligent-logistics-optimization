# intelligent-logistics-optimization
MathorCup 2025 project: Hybrid forecasting and multi-objective optimization for urban logistics

## Problem Summary

The competition focused on **short-distance logistics demand forecasting and vehicle scheduling**. Short-distance transport occurs in the last stage of urban or provincial logistics networks, where goods are delivered from local sorting centers to distribution outlets. This stage is critical for timely delivery, customer experience, and efficient use of transportation resources.

Key tasks included:

1. **Demand Forecasting:** Predict the number of packages for each route for the next day, using available historical and "pre-known" package data. Forecast results were required at **10-minute granularity** to support vehicle scheduling.
2. **Vehicle Scheduling:** Determine the number of vehicles and dispatch times for each route, including "combined dispatch" (串点) when package volumes are low across nearby routes. The goal was to maximize the utilization of **own fleet vehicles** and minimize overall cost, while ensuring all packages are delivered on time.
3. **Container Optimization:** Explore the use of a standard container to shorten loading/unloading time but with reduced capacity, and adjust the vehicle scheduling accordingly.
4. **Robustness Analysis:** Evaluate how forecast deviations affect the scheduling optimization results.

> The full problem description is available in `problem_description/problem_description.pdf`.
