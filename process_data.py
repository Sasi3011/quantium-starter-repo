import pandas as pd
from pathlib import Path

# Folder where CSV files are stored
data_folder = Path("data")

# Read all CSV files
all_files = list(data_folder.glob("*.csv"))

dataframes = []

for file in all_files:
    df = pd.read_csv(file)
    dataframes.append(df)

# Combine all CSVs into one
combined = pd.concat(dataframes, ignore_index=True)

# Keep only Pink Morsels
pink = combined[combined["product"] == "Pink Morsels"]

# Create Sales column
pink["Sales"] = pink["quantity"] * pink["price"]

# Select only required columns
final = pink[["Sales", "date", "region"]]

# Rename columns to match required format
final.columns = ["Sales", "Date", "Region"]

# Save output
final.to_csv("output.csv", index=False)

print("output.csv generated successfully!")

