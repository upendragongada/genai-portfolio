
import streamlit as st
import sys
from pathlib import Path

SRC_PATH = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC_PATH))

from opensearch_hybrid_search import hybrid_search

st.set_page_config(
    page_title="AI Product Search",
    page_icon="🛍️",
    layout="wide"
)

st.title("🛍️ AI-Powered E-Commerce Search")
st.caption("Discover products using keyword and semantic hybrid search.")

query = st.text_input(
    "What are you looking for?",
    placeholder="Example: best smartphone for photography"
)

top_k = st.slider("Number of results", 1, 8, 5)

if st.button("Search Products", type="primary"):
    if len(query.strip()) < 2:
        st.warning("Please enter at least 2 characters.")
    else:
        with st.spinner("Searching products..."):
            try:
                results = hybrid_search(query, top_k)

                if not results:
                    st.info("No matching products found.")
                else:
                    st.success(f"Found {len(results)} products")

                    for hit in results:
                        product = hit["_source"]

                        with st.container(border=True):
                            st.subheader(product["name"])
                            st.write(f"Category: {product['category']}")
                            st.write(f"Price: ₹{product['price']:,}")
                            st.write(
                                f"Relevance score: {hit['_score']:.5f}"
                            )

            except Exception:
                st.error(
                    "Search failed. Check that OpenSearch is running "
                    "and its credentials are configured."
                )
