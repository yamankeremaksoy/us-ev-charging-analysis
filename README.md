# EV Charging Station Optimal Allocation Analysis

This project analyzes NREL 2025-2030 Electric Vehicle (EV) growth projections across US states and applies an optimization algorithm to allocate 1,000 new charging stations based on projected demand and grid impact.

## Project Structure
- `ev_charging_analysis.py`: Main Python script for data processing and allocation analysis.
- `requirements.txt`: Python dependencies required to run the analysis.
- `national_state-2030ncn-results/`: Dataset containing state-level EV projections.

## Key Features
- **Data Consolidation**: Merges multi-file Excel datasets automatically.
- **Dynamic Grouping**: Handles state-level FIPS codes and metrics safely without column collision.
- **Demand Projections**: Calculates absolute EV growth and percentage growth rates (2025–2030).
- **Optimal Allocation**: Allocates 1,000 charging infrastructure units proportional to regional growth.
- **Automated Reporting**: Generates an `EV_Charging_Optimal_Allocation.xlsx` report upon execution.

## Installation & Setup

1. Install required Python packages:
   ```bash
   pip install -r requirements.txt
