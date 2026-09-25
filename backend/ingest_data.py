import asyncio
import csv
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "hotel_chatbot")

async def ingest_data():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db["hotel_urls"]
    
    # Optional: clear existing data before ingestion
    await collection.delete_many({})
    
    csv_file_path = os.path.join(os.path.dirname(__file__), "sample_data.csv")
    
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader) # Skip header row
        
        hotels = []
        for row in reader:
            if len(row) >= 2:
                url = row[0].strip()
                status = row[1].strip()
                notes = row[2].strip() if len(row) > 2 else ""
                
                hotels.append({
                    "url": url,
                    "is_active": status.lower() == 'active',
                    "status_text": status,
                    "notes": notes
                })
            
        if hotels:
            await collection.insert_many(hotels)
            print(f"Successfully ingested {len(hotels)} hotel URLs into MongoDB.")
        else:
            print("No data found in the CSV.")
            
    client.close()

if __name__ == "__main__":
    asyncio.run(ingest_data())
