import pandas as pd

file_path = "data/ota_hotels.xlsx"

df = pd.read_excel(file_path)

print("\n===== DATASET INFORMATION =====")
print("Total rows:", len(df))
print("Total columns:", len(df.columns))

print("\n===== COLUMN NAMES =====")
for i, column in enumerate(df.columns, start=1):
    print(f"{i}. {column}")

print("\n===== FIRST 5 ROWS =====")
print(df.head().to_string())

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())