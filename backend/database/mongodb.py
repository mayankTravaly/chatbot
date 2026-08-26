import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "hotel_database")
MONGO_COLLECTION_NAME = os.getenv(
    "MONGO_COLLECTION_NAME",
    "hotels"
)

client = MongoClient(MONGO_URI)

db = client[MONGO_DB_NAME]

hotels_collection = db[MONGO_COLLECTION_NAME]