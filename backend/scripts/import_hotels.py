import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "hotel_database")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME", "hotels")

if not MONGO_URI:
    raise ValueError("MONGO_URI is not configured in .env")

# Excel file
EXCEL_FILE = "data/ota_hotels.xlsx"

# Read Excel
print("Reading Excel file...")

df = pd.read_excel(EXCEL_FILE)

print(f"Found {len(df)} hotels")

# Convert dataframe to dictionaries
hotels = df.to_dict(orient="records")

# Connect to MongoDB
print("Connecting to MongoDB...")

client = MongoClient(MONGO_URI)

# Test connection
client.admin.command("ping")

print("MongoDB connection successful!")

# Select database and collection
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]

# Clear existing data to avoid duplicates
collection.delete_many({})

# Insert hotels
if hotels:
    result = collection.insert_many(hotels)
    print(f"Inserted {len(result.inserted_ids)} hotels successfully!")
else:
    print("No hotel records found.")

# Create useful indexes
collection.create_index("hotel_name")
collection.create_index("city")
collection.create_index("country")
collection.create_index("star_rating")
collection.create_index("property_type")
collection.create_index("is_active")

print("Indexes created successfully.")

# Close connection
client.close()

print("Import completed!")