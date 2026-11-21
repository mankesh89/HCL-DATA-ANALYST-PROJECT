# HCL-DATA-ANALYST-PROJECT
data analyst project by mankesh
# Smart Factory Machine Maintenance Analysis

## Overview
A beginner-friendly Python data-analysis project using the supplied `predictive_maintenance.csv` dataset.

## Requirements
- Python 3.9+
- pandas
- numpy
- matplotlib (optional; the current script exports tables and does not require plots)

Install:
```bash
pip install pandas numpy
```

## Run
Keep `predictive_maintenance.csv` and `machine_maintenance_analysis.py` in the same folder, then run:
```bash
python machine_maintenance_analysis.py
```
Results are saved in the `outputs/` folder.

## Dataset columns
UDI, Product ID, Type, Air temperature [K], Process temperature [K], Rotational speed [rpm], Torque [Nm], Tool wear [min], Target, Failure Type.

## Important limitations
The supplied file has 10,000 rows and 10 columns. It has no vibration or operating-hours field, and Product ID is unique in each row. Therefore:
- Vibration comparisons and vibration-IQR flagging cannot be performed. Torque IQR outliers are provided as a clearly labelled alternative.
- Ranking machines by average operating hours cannot be performed. A tool-wear record ranking is provided as a clearly labelled alternative.
- The risk bands (tool wear <=100, 101-200, >200 minutes) are exploratory thresholds selected for this assignment, not manufacturer-approved limits.
- `Target` and `Failure Type` are not fully consistent in every row; inspect `target_failure_type_cross_tab.csv`.

## Outputs
The script writes CSV summaries, flagged records, risk-band results, a cleaned dataset, and maintenance recommendations to `outputs/`.

## Interpretation
The results describe associations in this dataset. They do not establish that a sensor reading causes a machine failure. Maintenance thresholds should be validated with equipment manuals and plant engineers.
