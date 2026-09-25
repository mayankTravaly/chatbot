import os
from openai import AsyncOpenAI
import json
from services.db import get_db

# Initialize clients (We initialize both, but only use the one selected in .env)
# Provide a dummy string fallback so the server doesn't crash on startup if the OpenAI key is empty
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY") or "dummy_key")

# OpenAI Tool Schema
openai_tools = [
    {
        "type": "function",
        "function": {
            "name": "check_hotel_status_tool",
            "description": "Check if a specific hotel URL is active or inactive in our system.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The exact URL of the hotel."
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_hotels_tool",
            "description": "Search for hotels based on a text query (e.g., city, hotel name, or description).",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_query": {
                        "type": "string",
                        "description": "The search term, like 'Dhaka' or 'White Palace'."
                    }
                },
                "required": ["search_query"]
            }
        }
    }
]

async def execute_hotel_search(arguments):
    """Executes the MongoDB query to check URL status."""
    db = get_db()
    collection = db["hotel_urls"]
    
    url_to_search = arguments.get("url", "")
    
    # Exact match search for the URL
    hotel = await collection.find_one({"url": url_to_search})
    
    if not hotel:
        return "I couldn't find that URL in our database."
        
    status = "ACTIVE" if hotel.get("is_active") else "INACTIVE"
    notes = hotel.get("notes", "")
    
    return f"The hotel at that URL is currently {status}. {notes}"


# Initialize a global synchronous DB client for the Gemini tool.
# By keeping the connection open globally, we save 1-2 seconds of connection overhead per query!
import pymongo
sync_mongo_client = pymongo.MongoClient(os.environ.get("MONGO_URI", "mongodb://localhost:27017"))
sync_db = sync_mongo_client[os.environ.get("DB_NAME", "hotel_chatbot")]

# Define Python function for Gemini tool calling
def check_hotel_status_tool(url: str) -> str:
    """Check if a specific hotel URL is active or inactive in our system."""
    import time
    start_time = time.time()
    
    hotel = sync_db.hotel_urls.find_one({"url": url})
    
    print(f"DEBUG: MongoDB lookup took {time.time() - start_time:.4f} seconds")

    if not hotel:
        return "I couldn't find that URL in our database."
        
    status = "ACTIVE" if hotel.get("is_active") else "INACTIVE"
    notes = hotel.get("notes", "")
    return f"The hotel at that URL is currently {status}. {notes}"

def search_hotels_tool(search_query: str) -> str:
    """Search for hotels based on a text query (e.g., city, hotel name, or description)."""
    import time
    start_time = time.time()
    
    # Filter only for active hotels to hide internal/inactive data from customers!
    results = sync_db.hotels_info.find(
        {"$text": {"$search": search_query}, "is_active": True},
        {"score": {"$meta": "textScore"}}
    ).sort([("score", {"$meta": "textScore"})]).limit(3)
    
    hotels = list(results)
    
    print(f"DEBUG: MongoDB text search took {time.time() - start_time:.4f} seconds")

    if not hotels:
        return f"I couldn't find any available hotels matching '{search_query}'."
        
    response_lines = ["Found the following available hotels:"]
    for h in hotels:
        name = h.get('hotel_name', 'Unknown')
        city = h.get('city', 'Unknown')
        rating = h.get('star_rating', '')
        desc = h.get('description', '')[:200] + '...' # Truncate long descriptions
        response_lines.append(f"- {name} ({rating} Star) in {city}: {desc}")
        
    return "\n".join(response_lines)


async def generate_openai_response(messages):
    """
    Generate a response using OpenAI's API.
    Supports tool calling for 'check_hotel_status_tool' and 'search_hotels_tool'.
    """
    import json
    
    # Inject system prompt
    system_prompt = {
        "role": "system",
        "content": "You are a customer-facing hotel concierge. Always be polite, helpful, and natural. Do NOT expose internal database jargon like 'status active/inactive' or raw URLs to the user. Simply recommend hotels or say they are available/unavailable."
    }
    messages_with_system = [system_prompt] + messages

    # 1. Send the initial request to OpenAI with the tools definitions
    response = await openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_with_system,
        tools=openai_tools,
        tool_choice="auto"
    )  
    response_message = response.choices[0].message
    
    if response_message.tool_calls:
        messages_with_system.append(response_message)
        
        # Map tool names to their corresponding python functions
        tool_mapping = {
            "check_hotel_status_tool": check_hotel_status_tool,
            "search_hotels_tool": search_hotels_tool
        }
        
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            
            # Verify we actually have a function by that name
            if function_name in tool_mapping:
                function_to_call = tool_mapping[function_name]
                function_args = json.loads(tool_call.function.arguments)
                
                # Execute the local python function
                function_response = function_to_call(**function_args)
                
                # Append the tool's result to the message list
                messages_with_system.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })
            
        # 3. Send the updated message list back to OpenAI to get the final natural language response
        second_response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_with_system
        )
        return second_response.choices[0].message.content
        
    return response_message.content

async def generate_chat_response(messages):
    """Router for the AI Provider."""
    return await generate_openai_response(messages)
