
# Hybrid Search Architecture

## Objective
Combine lexical and semantic search to improve
product discovery.

## Retrieval Components

1. BM25 lexical search
2. Sentence Transformer embeddings
3. Cosine similarity
4. Reciprocal Rank Fusion

## RRF Formula

RRF(d) = Sum(1 / (k + rank))

Default k = 60

## Advantages

- Exact keyword matching
- Contextual retrieval
- Combines independent ranking systems
- No requirement to directly combine incompatible scores

## Future Improvements

- OpenSearch integration
- Search relevance evaluation
- Precision@K
- Recall@K
- Mean Reciprocal Rank
- Normalized Discounted Cumulative Gain
