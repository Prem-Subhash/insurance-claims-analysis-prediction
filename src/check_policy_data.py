
import pandas as pd

# Load the Policies sheet
file_path = "data/raw/Data set _insurance_data (1).xlsx"

policies = pd.read_excel(file_path, sheet_name="Policies")

# Show all combinations of coverage type and property type
print("--- Coverage Type and Property Type ---")

print(
    pd.crosstab(
        policies["CoverageType"],
        policies["PropertyType"]
    )
)

# Check the insured amount for each coverage type
print("\n--- Sum Insured by Coverage Type ---")

print(
    policies.groupby("CoverageType")["SumInsured"].describe()
)

# Check whether any values have extra spaces
print("\n--- Extra Space Check ---")

for column in ["CoverageType", "PropertyType"]:
    for value in policies[column].unique():
        if value != value.strip():
            print("Extra spaces found in", column, ":", repr(value))

print("\nPolicy investigation completed.")
