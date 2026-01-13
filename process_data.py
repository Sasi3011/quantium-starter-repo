import pandas as pd
from pathlib import Path

data_folder = Path("data")
all_files = list(data_folder.glob("*.csv"))

dataframes = []
for file in all_files:
    df = pd.read_csv(file)
    dataframes.append(df)

combined = pd.concat(dataframes, ignore_index=True)

# Keep only Pink Morsel
pink = combined[combined["product"].str.lower() == "pink morsel"]

# Convert to numeric
pink["quantity"] = pd.to_numeric(pink["quantity"], errors="coerce")
pink["price"] = pd.to_numeric(pink["price"], errors="coerce")

# Create Sales column
pink["Sales"] = pink["quantity"] * pink["price"]

# Select and rename columns
final = pink[["Sales", "date", "region"]]
final.columns = ["Sales", "Date", "Region"]

# Save output
final.to_csv("output.csv", index=False)

print("output.csv generated successfully!")
