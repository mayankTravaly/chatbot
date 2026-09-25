# Hotel Chatbot AI Widget

An intelligent, AI-powered hotel chatbot widget designed to be easily embedded into any hotel website. This project uses a **React + Vite** frontend widget that natively parses Markdown, and a **FastAPI + MongoDB + OpenAI** backend to handle natural language queries and database lookups via RAG (Retrieval-Augmented Generation).

## 📂 Project Structure

This monorepo is divided into three main components:

1. **`/backend`**: The Python FastAPI server. It provides the REST API (`/api/chat`) that connects to MongoDB and OpenAI. It handles data ingestion and intelligent function calling (searching for hotels, checking availability, etc.).
2. **`/frontend`**: A React application built with Vite. It compiles down to a single `chatbot.iife.js` script that acts as an embeddable chat widget. It uses `react-markdown` to render human-like spacing, bold text, and bullet points.
3. **`/widget-test`**: A simple static HTML website used to test the compiled widget in a production-like environment without needing React.

## 🚀 Quick Start Guide

### 1. Setup the Backend
Navigate to the backend directory, configure your `.env` file with your `OPENAI_API_KEY` and `MONGO_URI`, and ingest the hotel data.
```bash
cd backend
pip install -r requirements.txt
python ingest_hotels_info.py  # Ingests the CSV data into MongoDB
uvicorn main:app --reload --port 8000
```
*See `backend/README.md` for detailed backend instructions.*

### 2. Build the Frontend Widget
Navigate to the frontend directory to compile the React code into a single embeddable script.
```bash
cd frontend
npm install
npm run build
```

### 3. Test the Widget
Simply open the `widget-test/index.html` file in your browser to see the widget running live on a dummy website!
