
import json
import sys
from pathlib import Path

import streamlit as st

SRC_PATH = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_PATH.parent
DATA_FILE = PROJECT_ROOT / "data" / "products.json"

sys.path.insert(0, str(SRC_PATH))

from opensearch_hybrid_search import hybrid_search


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="ShopSmart | Online Shopping",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# PRODUCT IMAGE LIBRARY
# These are representative category images.
# They are not verified photos of individual models.
# --------------------------------------------------

CATEGORY_IMAGES = {
    "Smartphones": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=700",
    "Laptops": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=700",
    "Headphones": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=700",
    "Keyboards": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=700",
    "Dresses": "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=700",
    "Shoes": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=700",
    "Washing Machines": "https://loremflickr.com/700/500/washingmachine",
    "Air Conditioners": "https://loremflickr.com/700/500/airconditioner",
    "Air Fryers": "https://loremflickr.com/700/500/airfryer",
    "Accessories": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=700"
}

CATEGORIES = list(CATEGORY_IMAGES.keys())


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #f5f7fa;
    }

    [data-testid="stHeader"] {
        background: rgba(245,247,250,0.95);
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    /* Navigation */
    .shop-nav {
        background: #131921;
        color: white;
        padding: 17px 22px;
        border-radius: 10px;
        margin-bottom: 18px;
    }

    .shop-logo {
        font-size: 27px;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .shop-logo span {
        color: #ff9900;
    }

    .shop-subtitle {
        color: #d5d9df;
        font-size: 12px;
        margin-top: 3px;
    }

    .delivery {
        color: #d5d9df;
        font-size: 12px;
    }

    /* Hero */
    .hero {
        background: linear-gradient(110deg, #172b4d, #315b83);
        border-radius: 14px;
        padding: 42px 35px;
        color: white;
        margin: 15px 0 25px 0;
    }

    .hero h1 {
        font-size: 35px;
        font-weight: 800;
        color: white;
        margin-bottom: 10px;
    }

    .hero p {
        font-size: 16px;
        color: #e6edf5;
    }

    .hero-tag {
        display: inline-block;
        background: #ff9900;
        color: #17202c;
        font-weight: 700;
        padding: 7px 13px;
        border-radius: 5px;
        font-size: 12px;
        margin-bottom: 15px;
    }

    /* Section headings */
    .section-heading {
        font-size: 23px;
        font-weight: 800;
        color: #17202c;
        margin-top: 28px;
        margin-bottom: 15px;
    }

    .section-subtitle {
        color: #667085;
        font-size: 13px;
        margin-top: -10px;
        margin-bottom: 20px;
    }

    /* Product cards */
    .product-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 18px;
        min-height: 145px;
    }

    .product-name {
        font-size: 16px;
        font-weight: 700;
        color: #182230;
        min-height: 42px;
    }

    .product-category {
        font-size: 12px;
        color: #667085;
        margin-top: 5px;
    }

    .product-price {
        color: #b12704;
        font-size: 22px;
        font-weight: 800;
        margin-top: 10px;
    }

    .product-description {
        color: #667085;
        font-size: 12px;
        min-height: 45px;
    }

    .product-score {
        color: #667085;
        font-size: 11px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    [data-testid="stSidebar"] h2 {
        color: #17202c;
    }

    /* Buttons */
    .stButton > button {
        background: #ff9900;
        color: #17202c;
        border: none;
        border-radius: 7px;
        font-weight: 700;
        min-height: 42px;
    }

    .stButton > button:hover {
        background: #e68a00;
        color: #17202c;
        border: none;
    }

    /* Search input */
    .stTextInput input {
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        min-height: 45px;
    }

    .footer {
        background: #131921;
        color: #d5d9df;
        text-align: center;
        border-radius: 9px;
        padding: 22px;
        margin-top: 35px;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# LOAD PRODUCT DATA
# --------------------------------------------------

with open(DATA_FILE, "r", encoding="utf-8") as file:
    all_products = json.load(file)


def get_product_image(category):
    return CATEGORY_IMAGES.get(
        category,
        "https://placehold.co/600x400?text=Product"
    )


# --------------------------------------------------
# TOP NAVIGATION
# --------------------------------------------------

nav1, nav2, nav3 = st.columns([2, 3, 1])

with nav1:
    st.markdown("""
    <div class="shop-nav">
        <div class="shop-logo">Shop<span>Smart</span></div>
        <div class="shop-subtitle">AI-powered online shopping</div>
    </div>
    """, unsafe_allow_html=True)

with nav2:
    st.markdown("""
    <div class="shop-nav">
        <div class="delivery">📍 Delivering across India</div>
        <div style="font-size:16px;font-weight:700;margin-top:5px;">
            Discover products at the best prices
        </div>
    </div>
    """, unsafe_allow_html=True)

with nav3:
    st.markdown("""
    <div class="shop-nav">
        <div style="font-size:25px;text-align:center;">🛒</div>
        <div style="font-size:12px;text-align:center;">Shop</div>
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.markdown("## 🛍️ Shop by Category")

selected_category = st.sidebar.selectbox(
    "Choose category",
    ["All Categories"] + CATEGORIES,
    key="category_select"
)

st.sidebar.divider()

st.sidebar.markdown("## 💰 Price Range")

min_price = st.sidebar.number_input(
    "Minimum price (₹)",
    min_value=0,
    max_value=200000,
    value=0,
    step=500
)

max_price = st.sidebar.number_input(
    "Maximum price (₹)",
    min_value=0,
    max_value=200000,
    value=200000,
    step=500
)

st.sidebar.divider()

top_k = st.sidebar.slider(
    "Products per search",
    min_value=1,
    max_value=20,
    value=8
)

sort_option = st.sidebar.selectbox(
    "Sort products",
    [
        "Relevance",
        "Price: Low to High",
        "Price: High to Low"
    ]
)

st.sidebar.divider()

st.sidebar.markdown("""
### Why ShopSmart?

- AI-powered product discovery
- Keyword + semantic search
- 1,008 sample products
- 10 product categories
- Smart category and price filters
""")


# --------------------------------------------------
# HERO BANNER
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="hero-tag">SMARTER SHOPPING STARTS HERE</div>
    <h1>Find What You Love.</h1>
    <p>
        Explore smartphones, laptops, fashion, electronics,
        home appliances and much more.
    </p>
    <p><b>Discover products using AI-powered hybrid search.</b></p>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SEARCH BAR
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">What are you shopping for today?</div>',
    unsafe_allow_html=True
)

with st.form("product_search_form"):
    search_col, button_col = st.columns([5, 1])

    with search_col:
        query = st.text_input(
            "Search",
            placeholder="Try: best laptop for programming, wireless headphones..."
            ,
            label_visibility="collapsed"
        )

    with button_col:
        search_button = st.form_submit_button(
            "🔍 Search",
            use_container_width=True
        )


# --------------------------------------------------
# SEARCH RESULTS
# --------------------------------------------------

if search_button:

    if len(query.strip()) < 2:
        st.warning("Please enter at least 2 characters.")

    elif min_price > max_price:
        st.error("Minimum price cannot exceed maximum price.")

    else:
        category_filter = (
            None if selected_category == "All Categories"
            else selected_category
        )

        with st.spinner("Finding the best matching products..."):

            try:
                results = hybrid_search(
                    query=query,
                    top_k=top_k,
                    category=category_filter,
                    min_price=min_price,
                    max_price=max_price
                )

                if sort_option == "Price: Low to High":
                    results.sort(
                        key=lambda x: x["_source"]["price"]
                    )

                elif sort_option == "Price: High to Low":
                    results.sort(
                        key=lambda x: x["_source"]["price"],
                        reverse=True
                    )

                st.markdown(
                    '<div class="section-heading">Search Results</div>',
                    unsafe_allow_html=True
                )

                st.caption(
                    f"{len(results)} products found for '{query}'"
                )

                if not results:
                    st.info("No matching products found.")

                else:
                    columns = st.columns(4)

                    for index, hit in enumerate(results):

                        product = hit["_source"]
                        image_url = get_product_image(
                            product["category"]
                        )

                        with columns[index % 4]:

                            st.markdown('<div class="product-card">',
                                        unsafe_allow_html=True)

                            st.image(
                                image_url,
                                use_container_width=True
                            )

                            st.markdown(
                                f'<div class="product-name">{product["name"]}</div>',
                                unsafe_allow_html=True
                            )

                            st.markdown(
                                f'<div class="product-category">{product["category"]}</div>',
                                unsafe_allow_html=True
                            )

                            st.markdown(
                                f'<div class="product-price">₹{product["price"]:,}</div>',
                                unsafe_allow_html=True
                            )

                            st.markdown(
                                f'<div class="product-description">'
                                f'{product.get("description", "")[:110]}...</div>',
                                unsafe_allow_html=True
                            )

                            st.markdown(
                                f'<div class="product-score">'
                                f'AI relevance: {hit["_score"]:.4f}</div>',
                                unsafe_allow_html=True
                            )

                            st.markdown('</div>', unsafe_allow_html=True)

            except Exception as error:
                st.error("Product search failed.")
                st.exception(error)


# --------------------------------------------------
# HOMEPAGE CATEGORY SECTION
# --------------------------------------------------

else:

    st.markdown(
        '<div class="section-heading">Explore Popular Categories</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Everything you need, all in one place.'
        '</div>',
        unsafe_allow_html=True
    )

    category_columns = st.columns(5)

    for index, category in enumerate(CATEGORIES):

        with category_columns[index % 5]:

            st.image(
                CATEGORY_IMAGES[category],
                use_container_width=True
            )

            st.markdown(
                f"**{category}**"
            )

    st.divider()

    st.markdown(
        '<div class="section-heading">Featured Products</div>',
        unsafe_allow_html=True
    )

    # Display a selection of products on the homepage.
    featured_products = all_products[:12]

    product_columns = st.columns(4)

    for index, product in enumerate(featured_products):

        with product_columns[index % 4]:

            st.image(
                get_product_image(product["category"]),
                use_container_width=True
            )

            st.markdown(f"**{product['name']}**")

            st.caption(product["category"])

            st.markdown(
                f"### ₹{product['price']:,}"
            )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">
    <b>ShopSmart</b><br>
    AI-powered E-Commerce Search Engine<br><br>
    Built with Python · Streamlit · FastAPI · OpenSearch ·
    Sentence Transformers
</div>
""", unsafe_allow_html=True)
