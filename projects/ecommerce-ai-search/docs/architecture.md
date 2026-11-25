# System Architecture

```mermaid
flowchart TD
    A[User Search Query] --> B[FastAPI REST API]
    B --> C[OpenSearch Hybrid Search]
    C --> D[BM25 Keyword Search]
    C --> E[Vector Semantic Search]
    D --> F[Score Normalization]
    E --> F
    F --> G[Combined Ranking]
    G --> H[Product Search Results]
