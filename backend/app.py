from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from routes.hotels import hotels_bp
from routes.chat import chat_bp
import os

load_dotenv()

app = Flask(__name__)
app.register_blueprint(hotels_bp)
app.register_blueprint(chat_bp)

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "hotel_database")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME", "hotels")

if not MONGO_URI:
    raise ValueError("MONGO_URI is not configured in .env")

client = MongoClient(MONGO_URI)

db = client[MONGO_DB_NAME]
hotels_collection = db[MONGO_COLLECTION_NAME]


@app.route("/")
def home():
    return jsonify({
        "message": "Hotel Chatbot Backend is running"
    })


@app.route("/hotels")
def hotels():
    hotels = list(
        hotels_collection.find({}, {"_id": 0}).limit(10)
    )

    return jsonify(hotels)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)