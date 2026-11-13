
import pandas as pd

file_path = "data/raw/Data set _insurance_data (1).xlsx"

customers = pd.read_excel(file_path, sheet_name="Customers")
policies = pd.read_excel(file_path, sheet_name="Policies")
claims = pd.read_excel(file_path, sheet_name="Claims")
external = pd.read_excel(file_path, sheet_name="ExternalData")
interactions = pd.read_excel(file_path, sheet_name="CustomerInteractions")

print("--- Customer Categories ---")

print("\nGender:")
print(customers["Gender"].value_counts())

print("\nIncome Bracket:")
print(customers["IncomeBracket"].value_counts())

print("\nMarital Status:")
print(customers["MaritalStatus"].value_counts())

print("\n--- Policy Categories ---")

print("\nCoverage Type:")
print(policies["CoverageType"].value_counts())

print("\nProperty Type:")
print(policies["PropertyType"].value_counts())

print("\n--- Claim Categories ---")

print("\nClaim Description:")
print(claims["Description"].value_counts())

print("\nClaim Outcome:")
print(claims["Outcome"].value_counts())

print("\n--- Interaction Categories ---")

print("\nChannel:")
print(interactions["Channel"].value_counts())

print("\n--- External Data Categories ---")

print("\nCrime Rate:")
print(external["CrimeRate"].value_counts())

print("\nWeather Risk:")
print(external["WeatherRisk"].value_counts())

print("\nFlood Risk:")
print(external["FloodRisk"].value_counts())
