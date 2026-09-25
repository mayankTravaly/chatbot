import csv
import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "hotel_chatbot")

def ingest_hotels_data():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db["hotels_info"]
    
    # Optional: clear existing data before ingestion
    collection.delete_many({})
    
    csv_file_path = os.path.join(os.path.dirname(__file__), "hotels_data.csv")
    
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        hotels = []
        for row in reader:
            # Clean up the row and parse booleans/numbers
            row['is_active'] = row.get('is_active', '').strip().lower() == 'true'
            row['star_rating'] = int(row.get('star_rating', 0)) if row.get('star_rating') else 0
            hotels.append(row)
            
        if hotels:
            collection.insert_many(hotels)
            print(f"Successfully ingested {len(hotels)} detailed hotel records into MongoDB.")
            
            # Create a text index for search
            collection.create_index([
                ("hotel_name", pymongo.TEXT),
                ("city", pymongo.TEXT),
                ("description", pymongo.TEXT),
                ("state", pymongo.TEXT),
                ("country", pymongo.TEXT)
            ])
            print("Successfully created Text Index on hotels_info collection.")
        else:
            print("No data found in the CSV.")
            
    client.close()

if __name__ == "__main__":
    ingest_hotels_data()
