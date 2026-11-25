
import { useState } from "react";
import Checkout from "./Checkout";
import {
  Search,
  ShoppingCart,
  MapPin,
  User,
  Menu,
  ChevronRight,
  Heart,
  Truck,
  ShieldCheck,
  Headphones,
  Laptop,
  Smartphone,
  Shirt,
  Watch,
  Sparkles,
  Zap
} from "lucide-react";

import "./App.css";

// ==========================================
// CATEGORIES
// ==========================================

const categories = [
  {
    name: "Mobiles",
    icon: Smartphone,
    image: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500"
  },
  {
    name: "Laptops",
    icon: Laptop,
    image: "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500"
  },
  {
    name: "Headphones",
    icon: Headphones,
    image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500"
  },
  {
    name: "Fashion",
    icon: Shirt,
    image: "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=500"
  },
  {
    name: "Shoes",
    icon: Zap,
    image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500"
  },
  {
    name: "Accessories",
    icon: Watch,
    image: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500"
  }
];

// ==========================================
// DEMO PRODUCTS
// ==========================================

const products = [
  {
    id: 1,
    name: "Premium Wireless Headphones",
    brand: "Sony",
    category: "Headphones",
    price: 24999,
    oldPrice: 29999,
    rating: 4.8,
    image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=700",
    tag: "BEST SELLER"
  },
  {
    id: 2,
    name: "Professional Laptop",
    brand: "Dell",
    category: "Laptops",
    price: 74999,
    oldPrice: 89999,
    rating: 4.7,
    image: "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=700",
    tag: "POPULAR"
  },
  {
    id: 3,
    name: "Latest Generation Smartphone",
    brand: "Samsung",
    category: "Mobiles",
    price: 59999,
    oldPrice: 69999,
    rating: 4.6,
    image: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=700",
    tag: "TRENDING"
  },
  {
    id: 4,
    name: "Running Sports Sneakers",
    brand: "Nike",
    category: "Shoes",
    price: 4999,
    oldPrice: 6999,
    rating: 4.5,
    image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=700",
    tag: "SPECIAL OFFER"
  }
];

// ==========================================
// MAIN APP
// ==========================================

function App() {
  const [search, setSearch] = useState("");
  const [cart, setCart] = useState([]);
  const [cartOpen, setCartOpen] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [checkoutOpen, setCheckoutOpen] = useState(false);

  const [apiProducts, setApiProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState("");
  const [hasSearched, setHasSearched] = useState(false);

  const [openMenu, setOpenMenu] = useState(null);
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");

  // Backend category mapping
  const categoryMapping = {
    Mobiles: "Smartphones",
    Laptops: "Laptops",
    Headphones: "Headphones",
    Fashion: "Dresses",
    Shoes: "Shoes",
    Accessories: "Accessories"
  };
  // SHOPPING CART FUNCTIONS

function addToCart(product) {
  setCart((currentCart) => {
    const existing = currentCart.find(
      (item) => item.id === product.id
    );

    if (existing) {
      return currentCart.map((item) =>
        item.id === product.id
          ? { ...item, quantity: item.quantity + 1 }
          : item
      );
    }

    return [...currentCart, { ...product, quantity: 1 }];
  });

  setCartOpen(true);
}

function updateCartQuantity(productId, change) {
  setCart((currentCart) =>
    currentCart
      .map((item) =>
        item.id === productId
          ? { ...item, quantity: item.quantity + change }
          : item
      )
      .filter((item) => item.quantity > 0)
  );
}

function removeFromCart(productId) {
  setCart((currentCart) =>
    currentCart.filter((item) => item.id !== productId)
  );
}

const cartCount = cart.reduce(
  (total, item) => total + item.quantity,
  0
);

const cartTotal = cart.reduce(
  (total, item) => total + Number(item.price) * item.quantity,
  0
);

  // ========================================
  // SEARCH FUNCTION
  // ========================================

  async function handleSearch(
    categoryOverride = selectedCategory,
    queryOverride = search
  ) {
    const query = String(queryOverride || "").trim();

    if (query.length < 2) {
      setApiError("Please enter at least 2 characters.");
      return;
    }

    setLoading(true);
    setApiError("");
    setHasSearched(true);

    try {
      const params = new URLSearchParams({
        q: query,
        top_k: "5"
      });

      if (categoryOverride !== "All") {
        params.set(
        "category",
        categoryMapping[categoryOverride] || categoryOverride
        );
      }

      if (minPrice !== "") {
        params.set("min_price", minPrice);
      }

      if (maxPrice !== "") {
        params.set("max_price", maxPrice);
      }

      const url = `/api/search?${params.toString()}`;

      console.log("SEARCH URL:", url);

      // Make exactly one API request
      const response = await fetch(url);

      // Read response body only once
      const responseText = await response.text();

      console.log("HTTP STATUS:", response.status);
      console.log(
        "CONTENT TYPE:",
        response.headers.get("content-type")
      );
      console.log("RAW API RESPONSE:", responseText);

      if (!response.ok) {
        throw new Error(
          `API error ${response.status}: ${
            responseText || "Empty server response"
          }`
        );
      }

      if (!responseText.trim()) {
        throw new Error(
          "Search API returned an empty response. Check FastAPI terminal."
        );
      }

      let data;

      try {
        data = JSON.parse(responseText);
      } catch {
        throw new Error(
          "Invalid JSON response: " + responseText.slice(0, 250)
        );
      }

      if (!Array.isArray(data.results)) {
        throw new Error(
          "API response does not contain a results array."
        );
      }

      console.log("API RESPONSE:", data);

      // Convert backend products into frontend products
      const formattedProducts = data.results.map((product) => {
        const matchingCategory = categories.find(
          (category) =>
            category.name === product.category ||
            (category.name === "Mobiles" &&
              product.category === "Smartphones") ||
            (category.name === "Fashion" &&
              product.category === "Dresses")
        );

        return {
          id: product.id,
          name: product.name || "Unnamed product",
          brand: (product.name || "ShopSmart").split(" ")[0],
          category: product.category || "Other",
          price: Number(product.price) || 0,
          oldPrice: null,
          rating: null,
          score: Number(product.score) || 0,
          tag: "AI MATCH",
          image:
            matchingCategory?.image ||
            "https://placehold.co/500x400?text=Product"
        };
      });

      setApiProducts(formattedProducts);

      console.log("FORMATTED PRODUCTS:", formattedProducts);

      if (formattedProducts.length === 0) {
        setApiError(
          "No matching products found. Try another search."
        );
      }

    } catch (error) {
      console.error("SEARCH ERROR:", error);

      setApiError(
        error.message || "Something went wrong during search."
      );

      setApiProducts([]);

    } finally {
      setLoading(false);
    }
  }

  // ========================================
  // MENU CATEGORY SEARCH
  // ========================================

  function handleMenuCategory(categoryName) {
    const defaultQueries = {
      All: "popular products",
      Mobiles: "smartphone",
      Laptops: "laptop",
      Headphones: "wireless headphones",
      Fashion: "dress",
      Shoes: "running shoes",
      Accessories: "watch"
    };

    const query = defaultQueries[categoryName] || "popular products";

    setSelectedCategory(categoryName);
    setSearch(query);
    setOpenMenu(null);

    handleSearch(categoryName, query);

    document
      .getElementById("products")
      ?.scrollIntoView({ behavior: "smooth" });
  }

  // ========================================
  // DEMO PRODUCT FILTERING
  // ========================================

  const filteredProducts = products.filter((product) => {
    const matchesSearch =
      `${product.name} ${product.brand} ${product.category}`
        .toLowerCase()
        .includes(search.toLowerCase());

    const matchesCategory =
      selectedCategory === "All" ||
      product.category === selectedCategory;

    return matchesSearch && matchesCategory;
  });

  const displayProducts = hasSearched
    ? apiProducts
    : filteredProducts;

  // ========================================
  // CATEGORY SELECTION
  // ========================================

  function handleCategorySelect(categoryName) {
    setSelectedCategory(categoryName);

    if (hasSearched && search.trim().length >= 2) {
      handleSearch(categoryName, search);
    }
  }

  // ========================================
  // NAVIGATION MENU TOGGLE
  // ========================================

  function toggleMenu(menuName) {
    setOpenMenu((current) =>
      current === menuName ? null : menuName
    );
  }

  // ========================================
  // RENDER
  // ========================================

  return (
    <div className="app">

      {/* ANNOUNCEMENT */}

      <div className="announcement">
        <span>✨ Welcome to ShopSmart</span>
        <span>
          Discover smarter shopping with AI-powered search
        </span>
        <span>Free delivery on selected products</span>
      </div>

      {/* HEADER */}

      <header className="main-header">

        <div className="header-top">

          <div className="brand">
            <div className="brand-icon">S</div>

            <div>
              <h1>
                Shop<span>Smart</span>
              </h1>
              <small>SMARTER SHOPPING. BETTER LIVING.</small>
            </div>
          </div>

          <div className="delivery-location">
            <MapPin size={19} />

            <div>
              <small>Deliver to</small>
              <strong>India</strong>
            </div>
          </div>

          {/* SEARCH BAR */}

          <form
            className="search-box"
            onSubmit={(event) => {
              event.preventDefault();
              handleSearch();
            }}
          >
            <Search size={20} />

            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search products, brands and more..."
            />

            <button type="submit" disabled={loading}>
              {loading ? "Searching..." : "Search"}
            </button>
          </form>

          <button className="header-action">
            <User size={21} />
            <span>Account</span>
          </button>

          <button
            className="header-action cart-action"
            onClick={() => setCartOpen(true)}
          >
            <ShoppingCart size={23} />
            <span>Cart</span>
            <b>{cartCount}</b>
          </button>

        </div>

        {/* NAVIGATION */}

        <nav className="category-nav">

          {/* ALL CATEGORIES */}

          <div
            className={`nav-dropdown ${
              openMenu === "all" ? "open" : ""
            }`}
          >
            <button
              className="nav-menu"
              onClick={() => toggleMenu("all")}
              aria-expanded={openMenu === "all"}
            >
              <Menu size={18} />
              All Categories
              <ChevronRight size={15} />
            </button>

            <div className="dropdown-content">
              <button onClick={() => handleMenuCategory("All")}>
                All Products
              </button>
              <button onClick={() => handleMenuCategory("Mobiles")}>
                Smartphones
              </button>
              <button onClick={() => handleMenuCategory("Laptops")}>
                Laptops
              </button>
              <button onClick={() => handleMenuCategory("Headphones")}>
                Headphones & Audio
              </button>
              <button onClick={() => handleMenuCategory("Fashion")}>
                Fashion & Dresses
              </button>
              <button onClick={() => handleMenuCategory("Shoes")}>
                Shoes & Footwear
              </button>
              <button onClick={() => handleMenuCategory("Accessories")}>
                Accessories
              </button>
            </div>
          </div>

          {/* TODAY'S DEALS */}

          <div
            className={`nav-dropdown ${
              openMenu === "deals" ? "open" : ""
            }`}
          >
            <button
              className="nav-menu"
              onClick={() => toggleMenu("deals")}
              aria-expanded={openMenu === "deals"}
            >
              Today's Deals
              <ChevronRight size={15} />
            </button>

            <div className="dropdown-content">
              <button onClick={() => handleMenuCategory("All")}>
                Featured Deals
              </button>
              <button onClick={() => handleMenuCategory("Headphones")}>
                Audio Offers
              </button>
              <button onClick={() => handleMenuCategory("Laptops")}>
                Laptop Offers
              </button>
            </div>
          </div>

          {/* ELECTRONICS */}

          <div
            className={`nav-dropdown ${
              openMenu === "electronics" ? "open" : ""
            }`}
          >
            <button
              className="nav-menu"
              onClick={() => toggleMenu("electronics")}
              aria-expanded={openMenu === "electronics"}
            >
              Electronics
              <ChevronRight size={15} />
            </button>

            <div className="dropdown-content">
              <button onClick={() => handleMenuCategory("Mobiles")}>
                Smartphones
              </button>
              <button onClick={() => handleMenuCategory("Laptops")}>
                Laptops & Computers
              </button>
              <button onClick={() => handleMenuCategory("Headphones")}>
                Headphones
              </button>
              <button onClick={() => handleMenuCategory("Accessories")}>
                Accessories
              </button>
            </div>
          </div>

          {/* FASHION */}

          <div
            className={`nav-dropdown ${
              openMenu === "fashion" ? "open" : ""
            }`}
          >
            <button
              className="nav-menu"
              onClick={() => toggleMenu("fashion")}
              aria-expanded={openMenu === "fashion"}
            >
              Fashion
              <ChevronRight size={15} />
            </button>

            <div className="dropdown-content">
              <button onClick={() => handleMenuCategory("Fashion")}>
                Dresses
              </button>
              <button onClick={() => handleMenuCategory("Shoes")}>
                Shoes
              </button>
              <button onClick={() => handleMenuCategory("Accessories")}>
                Accessories
              </button>
            </div>
          </div>

          {/* HOME APPLIANCES */}

          <div
            className={`nav-dropdown ${
              openMenu === "home" ? "open" : ""
            }`}
          >
            <button
              className="nav-menu"
              onClick={() => toggleMenu("home")}
              aria-expanded={openMenu === "home"}
            >
              Home Appliances
              <ChevronRight size={15} />
            </button>

            <div className="dropdown-content">
              <button onClick={() => handleMenuCategory("All")}>
                All Home Appliances
              </button>
              <button onClick={() => handleMenuCategory("All")}>
                Washing Machines
              </button>
              <button onClick={() => handleMenuCategory("All")}>
                Air Conditioners
              </button>
              <button onClick={() => handleMenuCategory("All")}>
                Air Fryers
              </button>
            </div>
          </div>

          {/* BEST SELLERS */}

          <div
            className={`nav-dropdown ${
              openMenu === "best" ? "open" : ""
            }`}
          >
            <button
              className="nav-menu"
              onClick={() => toggleMenu("best")}
              aria-expanded={openMenu === "best"}
            >
              Best Sellers
              <ChevronRight size={15} />
            </button>

            <div className="dropdown-content">
              <button onClick={() => handleMenuCategory("Headphones")}>
                Popular Headphones
              </button>
              <button onClick={() => handleMenuCategory("Laptops")}>
                Popular Laptops
              </button>
              <button onClick={() => handleMenuCategory("Mobiles")}>
                Popular Smartphones
              </button>
            </div>
          </div>

          {/* NEW ARRIVALS */}

          <div
            className={`nav-dropdown ${
              openMenu === "new" ? "open" : ""
            }`}
          >
            <button
              className="nav-menu"
              onClick={() => toggleMenu("new")}
              aria-expanded={openMenu === "new"}
            >
              New Arrivals
              <ChevronRight size={15} />
            </button>

            <div className="dropdown-content">
              <button onClick={() => handleMenuCategory("Mobiles")}>
                New Smartphones
              </button>
              <button onClick={() => handleMenuCategory("Laptops")}>
                New Laptops
              </button>
              <button onClick={() => handleMenuCategory("Fashion")}>
                New Fashion
              </button>
            </div>
          </div>

        </nav>

      </header>

      <main>

        {/* HERO BANNER */}

        <section className="hero">

          <div className="hero-content">

            <div className="hero-label">
              <Sparkles size={15} />
              THE FUTURE OF SHOPPING
            </div>

            <h2>
              Everything you love.
              <br />
              <span>All in one place.</span>
            </h2>

            <p>
              Explore 1,000+ products across electronics,
              fashion and home appliances. Discover what
              you need with intelligent AI search.
            </p>

            <button
              className="hero-button"
              onClick={() =>
                document
                  .getElementById("products")
                  ?.scrollIntoView({ behavior: "smooth" })
              }
            >
              Explore Collection
              <ChevronRight size={18} />
            </button>

            <div className="hero-stats">
              <div>
                <strong>1,000+</strong>
                <small>Products</small>
              </div>

              <div>
                <strong>10</strong>
                <small>Categories</small>
              </div>

              <div>
                <strong>AI</strong>
                <small>Smart Search</small>
              </div>
            </div>

          </div>

          <div className="hero-image">
            <img
              src="https://images.unsplash.com/photo-1607082349566-187342175e2f?w=1100"
              alt="Shopping collection"
            />

            <div className="hero-image-card">
              <Sparkles size={19} />

              <div>
                <strong>Smart Discovery</strong>
                <small>Find products you'll love</small>
              </div>
            </div>
          </div>

        </section>

        {/* BENEFITS */}

        <section className="benefits">

          <div>
            <Truck />
            <span>
              <strong>Convenient Shopping</strong>
              <small>Browse from anywhere</small>
            </span>
          </div>

          <div>
            <ShieldCheck />
            <span>
              <strong>Smart Discovery</strong>
              <small>Intelligent product search</small>
            </span>
          </div>

          <div>
            <Zap />
            <span>
              <strong>Fast Search</strong>
              <small>Find products quickly</small>
            </span>
          </div>

          <div>
            <Heart />
            <span>
              <strong>More Choices</strong>
              <small>Explore multiple categories</small>
            </span>
          </div>

        </section>

        {/* CATEGORY SECTION */}

        <section className="section">

          <div className="section-heading">

            <div>
              <span className="eyebrow">EXPLORE COLLECTIONS</span>
              <h2>Shop by Category</h2>
              <p>Find everything you need in one place.</p>
            </div>

            <button
              className="text-button"
              onClick={() => {
                setSelectedCategory("All");
                setHasSearched(false);
                setApiError("");
                setApiProducts([]);
                setSearch("");

                document
                  .getElementById("products")
                  ?.scrollIntoView({ behavior: "smooth" });
              }}
            >
              View all categories
              <ChevronRight size={17} />
            </button>

          </div>

          <div className="category-grid">

            {categories.map((category) => {
              const Icon = category.icon;

              return (
                <button
                  className={`category-card ${
                    selectedCategory === category.name ? "active" : ""
                  }`}
                  key={category.name}
                  onClick={() => {
                    handleMenuCategory(category.name);

                    document
                      .getElementById("products")
                      ?.scrollIntoView({ behavior: "smooth" });
                  }}
                >
                  <div className="category-image">
                    <img
                      src={category.image}
                      alt={category.name}
                    />

                    <div className="category-icon">
                      <Icon size={19} />
                    </div>
                  </div>

                  <strong>{category.name}</strong>

                  <small>
                    Explore collection
                    <ChevronRight size={13} />
                  </small>
                </button>
              );
            })}

          </div>

        </section>

        {/* PRODUCTS */}

        <section
          className="section products-section"
          id="products"
        >

          <div className="section-heading">

            <div>
              <span className="eyebrow">
                {hasSearched
                  ? "AI-POWERED SEARCH"
                  : "HANDPICKED FOR YOU"}
              </span>

              <h2>
                {hasSearched ? "Search Results" : "Featured Products"}
              </h2>

              <p>
                {hasSearched
                  ? `Results for "${search}"`
                  : "Popular choices from our collection."}
              </p>
            </div>

            <button
              className="text-button"
              onClick={() => {
                setSelectedCategory("All");
                setHasSearched(false);
                setApiError("");
                setApiProducts([]);
                setSearch("");
                setOpenMenu(null);
              }}
            >
              View all products
              <ChevronRight size={17} />
            </button>

          </div>

          {/* PRODUCT FILTERS */}

          <div className="product-filter">

            {["All", "Mobiles", "Laptops", "Headphones", "Shoes"].map(
              (category) => (
                <button
                  key={category}
                  className={
                    selectedCategory === category
                      ? "filter-active"
                      : ""
                  }
                  onClick={() => {
                    if (category === "All") {
                      setSelectedCategory("All");

                      if (hasSearched && search.trim().length >= 2) {
                        handleSearch("All", search);
                      } else {
                        setHasSearched(false);
                        setApiProducts([]);
                        setApiError("");
                      }
                    } else {
                      handleCategorySelect(category);
                    }
                  }}
                >
                  {category}
                </button>
              )
            )}

          </div>
  <div className="advanced-filters">
    <strong>Filter by price</strong>

    <input
      type="number"
      min="0"
      placeholder="Minimum ₹"
      value={minPrice}
      onChange={(event) => setMinPrice(event.target.value)}
    />

    <input
      type="number"
      min="0"
      placeholder="Maximum ₹"
      value={maxPrice}
      onChange={(event) => setMaxPrice(event.target.value)}
    />

    <button
      onClick={() => handleSearch(selectedCategory, search)}
      disabled={loading}
    >
      Apply Filters
    </button>

    <button
      className="clear-filter"
      onClick={() => {
        setMinPrice("");
        setMaxPrice("");
        handleSearch(selectedCategory, search);
      }}
      disabled={loading}
  >
    Clear
  </button>
</div>

          {/* LOADING */}

          {loading && (
            <div className="empty-state">
              <Sparkles size={20} />
              <p>Finding the best products using AI search...</p>
            </div>
          )}

          {/* ERROR */}

          {apiError && !loading && (
            <div className="empty-state">
              {apiError}
            </div>
          )}

          {/* PRODUCT GRID */}

          {!loading && !apiError && (
            <div className="product-grid">

              {displayProducts.length > 0 ? (
                displayProducts.map((product) => (
                  <article
                    className="product-card"
                    key={product.id}
                  >

                    <div className="product-image">

                      <img
                        src={product.image}
                        alt={product.name}
                        onError={(event) => {
                          event.currentTarget.src =
                            "https://placehold.co/500x400?text=Product";
                        }}
                      />

                      <span className="product-tag">
                        {product.tag}
                      </span>

                      <button className="wishlist">
                        <Heart size={18} />
                      </button>

                    </div>

                    <div className="product-info">

                      <small className="product-brand">
                        {product.brand}
                      </small>

                      <h3>{product.name}</h3>

                      <div className="rating">
                        <Sparkles size={14} color="#f5a623" />

                        <strong>
                          {product.score != null
                            ? `AI relevance: ${product.score.toFixed(4)}`
                            : `${product.rating} rating`}
                        </strong>
                      </div>

                      <div className="price-row">

                        <strong>
                          ₹{Number(product.price).toLocaleString("en-IN")}
                        </strong>

                        {product.oldPrice != null && (
                          <del>
                            ₹{Number(product.oldPrice).toLocaleString("en-IN")}
                          </del>
                        )}

                      </div>

                      <button
                        className="add-cart"
                        onClick={() => addToCart(product)}
                      >
                        <ShoppingCart size={17} />
                        Add to Cart
                      </button>

                    </div>

                  </article>
                ))
              ) : (
                <div className="empty-state">
                  No products found. Try another search or category.
                </div>
              )}

            </div>
          )}

        </section>

        {/* PROMOTIONAL STRIP */}

        <section className="promo-strip">

          <div>
            <span>SHOP SMARTER WITH AI</span>

            <h2>
              Search by what you need, not just product names.
            </h2>

            <p>
              Discover products using meaning-based AI search.
            </p>
          </div>

          <Sparkles size={55} />

        </section>

      </main>
      {/* SHOPPING CART PANEL */}

{cartOpen && (
  <div
    className="cart-overlay"
    onClick={() => setCartOpen(false)}
  >
    <div
      className="cart-panel"
      onClick={(event) => event.stopPropagation()}
    >
      <div className="cart-header">
        <h2>
          Your Cart ({cartCount})
        </h2>

        <button onClick={() => setCartOpen(false)}>
          ✕
        </button>
      </div>

      {cart.length === 0 ? (
        <div className="cart-empty">
          <ShoppingCart size={42} />
          <h3>Your cart is empty</h3>
          <p>Add some products to get started.</p>
        </div>
      ) : (
        <>
          <div className="cart-items">
            {cart.map((item) => (
              <div className="cart-item" key={item.id}>
                <img
                  src={item.image}
                  alt={item.name}
                />

                <div className="cart-item-details">
                  <strong>{item.name}</strong>

                  <p>
                    ₹{Number(item.price).toLocaleString("en-IN")}
                  </p>

                  <div className="quantity-controls">
                    <button
                      onClick={() =>
                        updateCartQuantity(item.id, -1)
                      }
                    >
                      −
                    </button>

                    <span>{item.quantity}</span>

                    <button
                      onClick={() =>
                        updateCartQuantity(item.id, 1)
                      }
                    >
                      +
                    </button>
                  </div>
                </div>

                <button
                  className="remove-cart-item"
                  onClick={() => removeFromCart(item.id)}
                >
                  Remove
                </button>
              </div>
            ))}
          </div>

          <div className="cart-total">
            <span>Total</span>
            <strong>
              ₹{cartTotal.toLocaleString("en-IN")}
            </strong>
          </div>

          <button
            className="checkout-button"
            onClick={() => {
              setCartOpen(false);
              setCheckoutOpen(true);
            }}
            disabled={cart.length === 0}
          >
          Proceed to Checkout
          </button>
        </>
      )}
    </div>
  </div>
)}
      {/* FOOTER */}

      <footer className="footer">

        <div className="footer-brand">
          <h2>
            Shop<span>Smart</span>
          </h2>

          <p>A smarter way to discover products.</p>
        </div>

        <div className="footer-bottom">
          © 2026 ShopSmart. AI-powered e-commerce demonstration.
        </div>

      </footer>

      {checkoutOpen && (
        <Checkout
          cart={cart}
          cartTotal={cartTotal}
          onBack={() => setCheckoutOpen(false)}
          onOrderPlaced={() => {
            setCart([]);
            setCartOpen(false);
          }}
        />
      )}

    </div>
  );
}

export default App;
