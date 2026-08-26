from flask import Blueprint, request, jsonify
import re

from routes.hotels import hotels_collection

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({
            "error": "Message is required"
        }), 400

    message = data["message"]

    # Find budget
    budget_match = re.search(
        r"(?:under|below|less than|upto|up to)\s*(?:₹|rs\.?|inr)?\s*(\d+)",
        message.lower()
    )

    max_price = None

    if budget_match:
        max_price = float(budget_match.group(1))

    # Cities to check
    cities = [
        "Bangalore",
        "Bengaluru",
        "Hyderabad",
        "Chennai",
        "Mumbai",
        "Delhi",
        "Pune"
    ]

    city = None

    for c in cities:
        if c.lower() in message.lower():
            city = c
            break

    # Build MongoDB query
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
        ).limit(10)
    )

    return jsonify({
        "message": message,
        "city": city,
        "max_price": max_price,
        "count": len(hotels),
        "hotels": hotels
    })