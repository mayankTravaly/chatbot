# Hotel Chatbot Backend

This is the backend service for the Hotel Chatbot Widget, built using **Python (FastAPI)** and **MongoDB**. It handles user messages from the frontend widget, processes them using OpenAI's GPT-4o, and executes database queries to determine the active/inactive status of hotel URLs.

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- MongoDB instance running (local or Atlas)
- OpenAI API Key

### 1. Installation

Install the required Python dependencies:

```bash
cd chatbot/backend
pip install -r requirements.txt
```

### 2. Environment Variables

We use a `.env` file to manage sensitive credentials. There is a `.env` file already present (which is ignored by Git). You will need to add your production keys before running the server:

```ini
OPENAI_API_KEY=your_production_openai_key_here
MONGO_URI=mongodb://localhost:27017
DB_NAME=hotel_chatbot
```

### 3. Data Ingestion

Before the chatbot can answer queries, you need to load the Google Sheet data into MongoDB. We have provided an automated script for this:

1. Ensure the `sample_data.csv` is present in the `backend/` folder (it contains the URL, Status, and Reason).
2. Run the ingestion script:

```bash
python ingest_data.py
```
*This will parse the CSV and insert the data into the `hotel_urls` collection in MongoDB.*

### 4. Running the Server

Start the FastAPI server:

```bash
uvicorn main:app --reload
```
The server will run on `http://localhost:8000`. You can test the API endpoints directly via the interactive Swagger UI at `http://localhost:8000/docs`.

---

## 🧠 Architecture & How It Works

This backend is designed to minimize token usage and prevent the LLM from hallucinating data by utilizing **Retrieval-Augmented Generation (RAG)** via **Function Calling**.

1. **Frontend Request:** The frontend widget sends a POST request to `/api/chat` containing the conversation history.
2. **Intent Extraction:** The backend passes the conversation to OpenAI. The system prompt instructs the LLM to use the `check_hotel_status` tool if the user provides a URL.
3. **Database Query:** If the LLM identifies a URL, it extracts it and calls the function. Our backend (`services/chat.py`) intercepts this, connects to MongoDB, and performs an exact match search for the URL in the `hotel_urls` collection.
4. **Final Response:** The database result (Active/Inactive + Notes) is fed *back* to the LLM, which then formulates a natural, conversational response and sends it back to the frontend.

## 📁 File Structure

- `main.py`: The FastAPI application entry point, containing the `/api/chat` route and CORS configurations to sync with the frontend.
- `ingest_data.py`: A standalone script to wipe the database and ingest the latest `sample_data.csv`.
- `services/db.py`: Manages the asynchronous MongoDB connection pool (`motor`).
- `services/chat.py`: Contains the core OpenAI integration, function calling definitions, and the database search execution logic.
- `requirements.txt`: The list of Python dependencies.

## 🔌 Syncing with the Frontend

The frontend is a lightweight widget (similar to Intercom/Crisp) that can be embedded into any website via a `<script>` tag. 

When the user types a message in the widget, the frontend executes a simple `fetch()` request to `http://localhost:8000/api/chat` (or the production URL once deployed), passing a JSON array of the conversation history. 

FastAPI's CORS middleware in `main.py` is configured to allow requests from any origin (`allow_origins=["*"]`) during development so the frontend can communicate with it locally without encountering browser security errors. In production, this array should be restricted to your specific domain names.

---

## ✅ Completed Steps

- Defined the overall backend architecture using Python (FastAPI) and MongoDB.
- Created the FastAPI application and REST endpoints.
- Integrated OpenAI's `gpt-4o` with Function Calling / Tool capabilities.
- Downloaded the hotel data sheet from Google Sheets as a CSV.
- Created the `ingest_data.py` script and successfully parsed the URL-based dataset into the `hotel_urls` MongoDB collection.
- Set up proper `.gitignore` rules to prevent sensitive `.env` files and datasets from being committed.

## 🔜 Next Steps

- **Add Production Credentials:** Insert the actual `OPENAI_API_KEY` and production `MONGO_URI` into the `.env` file.
  > **Note on OpenAI Credits:** We ran into an issue testing the live chat because OpenAI recently removed their free tier for new accounts, resulting in an `Error 429: Insufficient Quota` on newly generated development keys. As Mayank noted: *"LLM: please work with OpenAI if that permits... We have the production API keys. We will use that."* Please ensure the key you place in the `.env` file is the production key with funded billing credits.
- **Frontend Development:** Build the frontend chat widget (HTML/CSS/JS or React) that will embed into the website and communicate with this backend.
- **Deployment:** Deploy the FastAPI application to a production environment (like AWS, Render, or Railway) and update the CORS settings in `main.py` to only allow the frontend's domain.
