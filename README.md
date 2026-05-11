# SHL Assessment Recommender

An AI-powered SHL assessment recommender that uses conversational retrieval to suggest the most relevant assessments based on a user’s role, skills, level, and requirements.

The project combines a FastAPI backend with a retrieval pipeline built around LangChain and FAISS, so users can ask natural-language questions and receive contextual assessment recommendations.

## Features

* Conversational assessment recommendation flow
* Retrieval-based search over the assessment catalog
* FastAPI backend for API access
* LangChain-based orchestration for agent/retriever logic
* FAISS vector search for semantic matching
* Modular service layer for recommendation, comparison, conversation, and retrieval

## Project Structure

```text
SHL_ASSESSMENT/
├── app/
│   ├── data/
│   ├── modules/
│   │   └── embedding.py
│   ├── scripts/
│   ├── services/
│   │   ├── agent.py
│   │   ├── comparator.py
│   │   ├── conversation.py
│   │   ├── recommendation.py
│   │   └── retriever.py
│   ├── vectorstore/
│   ├── main.py
│   └── requirements.txt
├── client/
├── main.py
├── pyproject.toml
└── README.md
```

## How It Works

1. The assessment catalog is processed and embedded.
2. Embeddings are stored in a FAISS vector index.
3. The retriever finds the most relevant assessments for a user query.
4. The agent/service layer formats the response and can compare or recommend assessments based on the request.
5. The FastAPI app exposes the functionality through endpoints for backend consumption.

## Tech Stack

* Python 3.12+
* FastAPI
* LangChain
* FAISS
* React / client-side UI
* Vector embeddings

## Getting Started

### Prerequisites

* Python 3.12 or higher
* Node.js and npm/yarn, if you want to run the client

### Backend Setup

```bash
cd app
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

If your project uses `pyproject.toml`, you can also install dependencies with your preferred Python tooling.

### Run the Backend

```bash
python main.py
```

If your FastAPI app is exposed through `app/main.py`, run it with your ASGI server, for example:

```bash
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd client
npm install
npm run dev
```

## API Overview

The backend is designed to support endpoints for:

* assessment recommendations
* conversational Q&A
* comparison of assessments
* retrieval of matching assessments from the catalog

Update this section with your exact routes once they are finalized.

## Example Use Case

A user can ask:

> "I need an assessment for a mid-level software engineer with strong problem-solving skills and coding ability."

The system then retrieves and ranks the most relevant SHL assessments and returns a contextual recommendation.

## Notes

* The repository is structured to keep retrieval, conversation, and recommendation logic separate.
* You can extend the system by adding new ranking rules, better embeddings, or more API endpoints.

## Future Improvements

* Add authentication
* Improve ranking and filtering logic
* Add stronger evaluation for recommendation quality
* Connect the client with live backend endpoints
* Add tests for the retrieval and agent flow

## License

Add your preferred license here.

## Author

Aayush Kumar
