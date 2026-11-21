# NAME- MANKESH KUMAR GOLA
# ADDMISSION NO-2026B01010811


"""
Machine Maintenance Analysis
A beginner-friendly data analytics project using pandas, NumPy, matplotlib and seaborn.

Run from the project root:
    python src/maintenance_analysis.py

The script reads data/raw/05_machine_maintenance.csv and writes cleaned data,
summary statistics and charts into data/processed/ and images/.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data" / "raw" / "05_machine_maintenance.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
IMAGE_DIR = ROOT / "images"

REQUIRED_COLUMNS = [
    "Machine_ID", "Operating_Hours", "Temperature_C", "Vibration_mm_s",
    "Rotational_Speed_RPM", "Tool_Wear_Minutes",
    "Maintenance_Required", "Failure_Type"
]
NUMERIC_COLUMNS = [
    "Operating_Hours", "Temperature_C", "Vibration_mm_s",
    "Rotational_Speed_RPM", "Tool_Wear_Minutes"
]


def load_data(file_path=RAW_FILE):
    """Load the original CSV and check that expected columns exist."""
    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}\n"
            "Place 05_machine_maintenance.csv inside data/raw/."
        )
    data = pd.read_csv(file_path)
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(data.columns))
    if missing_columns:
        raise ValueError(f"Dataset is missing columns: {missing_columns}")
    return data


def clean_data(data):
    """Clean types, text and missing values without changing the raw file."""
    cleaned = data.copy()

    # Remove exact duplicate records, if any.
    cleaned = cleaned.drop_duplicates()

    # Normalize text fields to avoid inconsistent labels.
    for column in ["Machine_ID", "Maintenance_Required", "Failure_Type"]:
        cleaned[column] = cleaned[column].astype("string").str.strip()
    cleaned["Maintenance_Required"] = cleaned["Maintenance_Required"].str.title()
    cleaned["Failure_Type"] = cleaned["Failure_Type"].str.title()

    # Convert measurements to numeric; invalid text becomes NaN.
    for column in NUMERIC_COLUMNS:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    # Median imputation is used for the 9 missing vibration readings.
    cleaned["Vibration_mm_s"] = cleaned["Vibration_mm_s"].fillna(
        cleaned["Vibration_mm_s"].median()
    )

    # Missing failure types are retained as an explicit reporting category.
    # A missing failure type does NOT prove that a machine had no failure.
    cleaned["Failure_Type"] = cleaned["Failure_Type"].fillna("Not Recorded")

    # Keep only documented target labels; unexpected values are made visible.
    invalid_targets = ~cleaned["Maintenance_Required"].isin(["Yes", "No"])
    if invalid_targets.any():
        raise ValueError(
            "Unexpected Maintenance_Required values: "
            f"{cleaned.loc[invalid_targets, 'Maintenance_Required'].unique().tolist()}"
        )
    return cleaned


def save_data_quality_report(raw, cleaned):
    """Save a compact report describing the input data and cleaning."""
    lines = [
        "MACHINE MAINTENANCE DATA QUALITY REPORT",
        "=" * 42,
        f"Raw rows: {len(raw)}",
        f"Rows after duplicate removal: {len(cleaned)}",
        f"Exact duplicate rows removed: {len(raw) - len(cleaned)}",
        "",
        "Missing values in raw data:",
        raw.isna().sum().to_string(),
        "",
        "Missing values after cleaning:",
        cleaned.isna().sum().to_string(),
        "",
        "Maintenance required counts:",
        cleaned["Maintenance_Required"].value_counts().to_string(),
        "",
        "Failure type counts (missing values labelled 'Not Recorded'):",
        cleaned["Failure_Type"].value_counts().to_string(),
    ]
    (PROCESSED_DIR / "data_quality_report.txt").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def create_charts(data):
    """Create charts for maintenance status, machine metrics and failure types."""
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(7, 5))
    sns.countplot(data=data, x="Maintenance_Required", order=["No", "Yes"], color="steelblue")
    plt.title("Machines by Maintenance Requirement")
    plt.xlabel("Maintenance Required")
    plt.ylabel("Number of Machines")
    plt.tight_layout()
    plt.savefig(IMAGE_DIR / "maintenance_required_count.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.boxplot(data=data, x="Maintenance_Required", y="Temperature_C",
                order=["No", "Yes"], color="steelblue")
    plt.title("Temperature by Maintenance Requirement")
    plt.xlabel("Maintenance Required")
    plt.ylabel("Temperature (°C)")
    plt.tight_layout()
    plt.savefig(IMAGE_DIR / "temperature_by_maintenance.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.boxplot(data=data, x="Maintenance_Required", y="Vibration_mm_s",
                order=["No", "Yes"], color="steelblue")
    plt.title("Vibration by Maintenance Requirement")
    plt.xlabel("Maintenance Required")
    plt.ylabel("Vibration (mm/s)")
    plt.tight_layout()
    plt.savefig(IMAGE_DIR / "vibration_by_maintenance.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    order = data["Failure_Type"].value_counts().index
    sns.countplot(data=data, y="Failure_Type", order=order, color="steelblue")
    plt.title("Recorded Failure Types")
    plt.xlabel("Number of Records")
    plt.ylabel("Failure Type")
    plt.tight_layout()
    plt.savefig(IMAGE_DIR / "failure_type_count.png", dpi=150)
    plt.close()

    plt.figure(figsize=(9, 6))
    corr = data[NUMERIC_COLUMNS].corr(numeric_only=True)
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", square=True)
    plt.title("Correlation Between Machine Measurements")
    plt.tight_layout()
    plt.savefig(IMAGE_DIR / "correlation_heatmap.png", dpi=150)
    plt.close()


def create_summary(data):
    """Generate descriptive statistics and group comparisons."""
    maintenance_rate = data["Maintenance_Required"].eq("Yes").mean() * 100
    numeric_summary = data[NUMERIC_COLUMNS].describe().round(2)
    group_summary = (
        data.groupby("Maintenance_Required")[NUMERIC_COLUMNS]
        .mean()
        .round(2)
    )
    failure_counts = data["Failure_Type"].value_counts()

    output = [
        "MACHINE MAINTENANCE ANALYSIS SUMMARY",
        "=" * 40,
        f"Total machine records: {len(data)}",
        f"Records requiring maintenance: {(data['Maintenance_Required'] == 'Yes').sum()}",
        f"Maintenance-required rate: {maintenance_rate:.1f}%",
        "",
        "NUMERIC DESCRIPTIVE STATISTICS",
        numeric_summary.to_string(),
        "",
        "AVERAGE MEASUREMENTS BY MAINTENANCE STATUS",
        group_summary.to_string(),
        "",
        "FAILURE TYPE COUNTS",
        failure_counts.to_string(),
        "",
        "CORRELATION MATRIX",
        data[NUMERIC_COLUMNS].corr().round(2).to_string(),
        "",
        "Interpretation note: group differences and correlations describe association,",
        "not proof that a measurement causes maintenance to be required.",
        "Failure_Type values marked 'Not Recorded' were missing in the original file.",
    ]
    (PROCESSED_DIR / "analysis_summary.txt").write_text(
        "\n".join(output), encoding="utf-8"
    )

    return maintenance_rate, group_summary


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_data()
    cleaned = clean_data(raw)
    cleaned.to_csv(PROCESSED_DIR / "machine_maintenance_clean.csv", index=False)

    save_data_quality_report(raw, cleaned)
    create_charts(cleaned)
    maintenance_rate, group_summary = create_summary(cleaned)

    print("Analysis completed successfully.")
    print(f"Rows analysed: {len(cleaned)}")
    print(f"Maintenance-required rate: {maintenance_rate:.1f}%")
    print("\nAverage measurements by maintenance status:")
    print(group_summary)
    print(f"\nCleaned data and reports: {PROCESSED_DIR}")
    print(f"Charts: {IMAGE_DIR}")


if __name__ == "__main__":
    main()
