# Hotel Chatbot Backend

This is the backend service for the Hotel Chatbot Widget, built using **Python (FastAPI)** and **MongoDB**. It handles user messages from the frontend widget, processes them using OpenAI's GPT-4o-mini, and executes database queries (using MongoDB Text Search) to answer hotel availability and feature questions.

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- MongoDB instance running (local or Atlas)
- OpenAI API Key

### 1. Installation

It is highly recommended to use a Python virtual environment.
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the `backend/` directory to manage sensitive credentials:

```ini
OPENAI_API_KEY=your_production_openai_key_here
MONGO_URI=mongodb://localhost:27017
DB_NAME=hotel_chatbot
```

### 3. Data Ingestion

Since `.csv` files are ignored by git for data privacy, you must manually download the hotel datasheet from the Google Spreadsheet and place it inside the `backend/` directory as `hotels_data.csv`.

Once the `hotels_data.csv` file is in the `backend/` directory, run the ingestion script:

```bash
python ingest_hotels_info.py
```
*This will parse the CSV, insert the data into the `hotels_info` collection, and build a full-text search index for the AI to use.*

### 4. Running the Server

Start the FastAPI server:

```bash
uvicorn main:app --reload --port 8000
```
The server will run on `http://localhost:8000`. 

---

## 🧠 Architecture & How It Works

This backend is designed to minimize token usage and prevent the LLM from hallucinating data by utilizing **Retrieval-Augmented Generation (RAG)** via **Function Calling**.

1. **Frontend Request:** The frontend widget sends a POST request to `/api/chat` containing the conversation history.
2. **Intent Extraction:** The backend passes the conversation to OpenAI. The system prompt instructs the LLM to use the `search_hotels_tool` if the user asks for hotel recommendations or details.
3. **Database Query:** If the LLM uses the tool, it passes a search term. Our backend (`services/chat.py`) connects to MongoDB and performs a `$text` search to find matching **active** hotels.
4. **Final Response:** The database result is fed *back* to the LLM, which then formulates a natural, conversational response and sends it back to the frontend.
