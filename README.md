# HrQueryChatbot_project
# 🧠 HR Resource Query Chatbot

This project is part of the AI/ML Engineer assessment. It implements a chatbot system to answer HR-related queries over employee data using FastAPI, LangChain, Streamlit, and Ollama.

## 🚀 Features

- FastAPI backend (/chat, /employees/add)
- Streamlit frontend with chat interface
- LangChain RAG pipeline for document retrieval + response
- Local LLM via Ollama (tinyllama)
- Local embeddings via spaCy (en_core_web_md)
- ChromaDB for vector similarity search
- JSON-based dynamic employee profiles

## 📁 Project Structure

hr_agent/
├── main.py             # FastAPI backend
├── app.py              # Streamlit frontend
├── employees.json      # Sample employee data
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation

## ⚙️ Setup Instructions

1. Clone the repo
   git clone https://github.com/your-username/hr-resource-chatbot.git
   cd hr-resource-chatbot/hr_agent

2. Create & activate virtual environment
   python -m venv venv
   venv\Scripts\activate  (On Windows)

3. Install dependencies
   pip install -r requirements.txt
   python -m spacy download en_core_web_md

4. Install Ollama and pull lightweight model
   ollama pull phi3

## ▶️ Running the App

- Start FastAPI backend:
  uvicorn main:app --reload

- Start Streamlit frontend:
  streamlit run app.py

Then open: http://localhost:8501

## 🔌 API Usage

POST /chat
{
  "question": "Who is available and knows Django?"
}

POST /employees/add
{
  "name": "John Doe",
  "skills": ["Python", "AWS"],
  "experience_years": 4,
  "projects": ["Chatbot", "ML Pipeline"],
  "availability": "Immediate"
}

## 🧠 Models Used

Component     | Tool/Library         | Model
------------- | -------------------- | ------------------------
LLM           | Ollama               |  tinyllama
Embeddings    | spaCy                | en_core_web_md
Vector Store  | LangChain + ChromaDB | Local persistent store


