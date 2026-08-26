from database.mongodb import hotels_collection


def search_hotels(
    city=None,
    country=None,
    min_rating=None,
    property_type=None,
    limit=20
):
    query = {
        "is_active": True
    }

    if city:
        query["city"] = {
            "$regex": city,
            "$options": "i"
        }

    if country:
        query["country"] = {
            "$regex": country,
            "$options": "i"
        }

    if min_rating is not None:
        query["star_rating"] = {
            "$gte": float(min_rating)
        }

    if property_type:
        query["property_type"] = {
            "$regex": property_type,
            "$options": "i"
        }

    hotels = hotels_collection.find(
        query,
        {"_id": 0}
    ).limit(limit)

    return list(hotels)