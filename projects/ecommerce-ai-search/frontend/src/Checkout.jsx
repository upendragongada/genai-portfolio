
import { useState } from "react";

export default function Checkout({ cart, cartTotal, onBack, onOrderPlaced }) {
  const [form, setForm] = useState({
    name: "",
    email: "",
    phone: "",
    address: "",
    city: "",
    pincode: "",
  });

  const [orderId, setOrderId] = useState("");

  function handleChange(event) {
    setForm({ ...form, [event.target.name]: event.target.value });
  }

  function placeOrder(event) {
    event.preventDefault();

    const id = "SS" + Date.now().toString().slice(-8);
    setOrderId(id);
    onOrderPlaced();
  }

  if (orderId) {
    return (
      <div className="checkout-success">
        <h1>🎉 Order Placed Successfully!</h1>
        <p>Your order ID: <strong>{orderId}</strong></p>
        <p>Thank you for shopping with ShopSmart.</p>
        <button onClick={onBack}>Continue Shopping</button>
      </div>
    );
  }

  return (
    <div className="checkout-page">
      <button onClick={onBack}>← Back to Cart</button>
      <h1>Checkout</h1>

      <div className="checkout-layout">
        <form onSubmit={placeOrder}>
          <h2>Delivery Details</h2>

          {[
            ["name", "Full Name", "text"],
            ["email", "Email Address", "email"],
            ["phone", "Phone Number", "tel"],
            ["address", "Delivery Address", "text"],
            ["city", "City", "text"],
            ["pincode", "PIN Code", "text"],
          ].map(([name, placeholder, type]) => (
            <input
              key={name}
              name={name}
              type={type}
              placeholder={placeholder}
              value={form[name]}
              onChange={handleChange}
              required
            />
          ))}

          <button type="submit">Place Order</button>
        </form>

        <div className="checkout-summary">
          <h2>Order Summary</h2>
          {cart.map((item) => (
            <p key={item.id}>
              {item.name} × {item.quantity}
            </p>
          ))}
          <h3>Total: ₹{cartTotal.toLocaleString("en-IN")}</h3>
        </div>
      </div>
    </div>
  );
}
