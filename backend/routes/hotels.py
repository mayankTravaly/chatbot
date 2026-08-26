from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "hotel_database")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME", "hotels")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
hotels_collection = db[MONGO_COLLECTION_NAME]

hotels_bp = Blueprint("hotels", __name__)


@hotels_bp.route("/hotels", methods=["GET"])
def get_hotels():
    city = request.args.get("city")
    max_price = request.args.get("max_price", type=float)

    query = {}

    if city:
        query["city"] = {
            "$regex": city,
            "$options": "i"
        }

    if max_price is not None:
        query["price"] = {
            "$lte": max_price
        }

    hotels = list(
        hotels_collection.find(
            query,
            {"_id": 0}
        ).limit(20)
    )

    return jsonify({
        "count": len(hotels),
        "hotels": hotels
    })