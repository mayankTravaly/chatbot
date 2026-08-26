from flask import Blueprint, request, jsonify
from services.hotel_service import search_hotels

hotel_routes = Blueprint("hotel_routes", __name__)


@hotel_routes.route("/hotels", methods=["GET"])
def get_hotels():

    city = request.args.get("city")
    country = request.args.get("country")
    min_rating = request.args.get("min_rating")
    property_type = request.args.get("property_type")
    limit = request.args.get("limit", 20, type=int)

    hotels = search_hotels(
        city=city,
        country=country,
        min_rating=min_rating,
        property_type=property_type,
        limit=limit
    )

    return jsonify({
        "count": len(hotels),
        "hotels": hotels
    })