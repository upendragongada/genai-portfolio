# AI-Powered E-Commerce Search Engine

An intelligent product search engine combining traditional keyword search, BM25 ranking, semantic search, and OpenSearch hybrid search.

## Project Overview

This project demonstrates how modern e-commerce platforms can improve product discovery by combining lexical and semantic search techniques.

Users can search for products using natural-language queries and retrieve relevant results through an API.

## Architecture

**Search pipeline:**

1. Product data is loaded from JSON.
2. Sentence Transformers generates 384-dimensional embeddings.
3. BM25 provides keyword-based relevance.
4. Semantic search retrieves conceptually similar products.
5. OpenSearch performs lexical and vector retrieval.
6. A hybrid search pipeline combines relevance scores.
7. FastAPI exposes search functionality through REST endpoints.

## Technology Stack

- Python
- FastAPI
- OpenSearch 2.19.1
- BM25
- Sentence Transformers
- all-MiniLM-L6-v2
- Vector Search
- Hybrid Search
- Reciprocal Rank Fusion (RRF)
- Docker
- Pytest

## Key Features

- Keyword-based product search
- BM25 ranking
- Semantic search using vector embeddings
- Hybrid search combining lexical and semantic retrieval
- OpenSearch vector indexing
- OpenSearch hybrid search pipeline
- REST API with FastAPI
- Swagger API documentation
- Automated API tests

## Project Structure

```text
ecommerce-ai-search/
├── data/
│   └── products.json
├── src/
│   ├── main.py
│   ├── search.py
│   ├── bm25_search.py
│   ├── semantic_search.py
│   ├── hybrid_search.py
│   ├── opensearch_loader.py
│   ├── opensearch_vector_loader.py
│   ├── opensearch_vector_search.py
│   ├── opensearch_hybrid_search.py
│   └── api.py
├── tests/
│   ├── test_search.py
│   ├── test_hybrid.py
│   └── test_api.py
├── docs/
│   └── hybrid-search.md
└── requirements.txt
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/health` | Health check |
| GET | `/search?q=smartphone` | Hybrid product search |

Interactive API documentation is available at `/docs` while the API server is running.

## Example Search

Query:

```text
best smartphone for photography
```

The API returns matching products with their names, categories, prices, and relevance scores.

## Run Locally in the Development Environment

Install dependencies:

```bash
pip install -r projects/ecommerce-ai-search/requirements.txt
```

Start the API:

```bash
uvicorn api:app --app-dir projects/ecommerce-ai-search/src --host 0.0.0.0 --port 8000
```

Open `/docs` to explore the API.

OpenSearch must be running and configured before using the hybrid search endpoint.

## Run Tests

```bash
pytest projects/ecommerce-ai-search/tests/ -v
```

## Learning Outcomes

- Understanding lexical and semantic information retrieval
- Implementing vector embeddings
- Working with OpenSearch indexes and mappings
- Building hybrid search pipelines
- Developing REST APIs using FastAPI
- Writing automated tests with Pytest

## Project Status

Core search engine, OpenSearch hybrid search, FastAPI integration, and automated API tests completed.

Further improvements planned: larger product datasets, performance benchmarking, frontend integration, and cloud deployment.

## Author

GenAI Engineer Portfolio Project

Built as a practical learning project demonstrating modern AI-powered search architecture.