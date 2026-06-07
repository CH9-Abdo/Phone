# 📱 Djellal Boutique - Your Premier Smartphone Store

Welcome to **Djellal Boutique**, a professional, responsive web application for showcasing smartphones with advanced installment plans and inventory management. This project is designed for the Algerian market, featuring localized pricing and a modern user interface.

## 🚀 How to Run

This is a static website, making it fast and easy to deploy.

1.  **Open locally (Simplest):**
    Simply double-click `index.html` to open it in your browser.

2.  **Using a local server (Recommended for development):**
    For the best experience without CORS issues, run a simple local server. If you have Python installed:
    ```bash
    python3 -m http.server 8000
    ```
    Then, open `http://localhost:8000` in your browser.

## 📂 Project Structure

```
Le_Boutique/
├── css/
│   └── style.css          # Main stylesheet (Premium Dark-Green Theme)
├── js/
│   ├── phones_data.js     # DATABASE: Contains all products, history, and status
│   └── script.js          # LOGIC: Filtering, sorting, and modal logic
├── Photos/                # Optimized phone images
├── index.html             # Main website entry point
│
├── SmartPhoneManager.py   # NEW: All-in-one Management & Scraping Tool (PyQt5)
├── admin_manager.py       # Legacy GUI tool (Tkinter)
│
└── README.md              # Project documentation
```

---

## 🛠️ Management Suite (The Pro Tool)

We have consolidated all previous utility scripts into a single, high-quality application: **`SmartPhoneManager.py`**.

### `SmartPhoneManager.py` (Unified Tool)
This is your **Main Command Center**. It features a modern PyQt5 interface with three powerful tabs:

1.  **📋 Phone List**: View and edit every detail of your inventory.
    *   **Stock Management**: Easily toggle phones between "Available" and "Out of Stock".
    *   **Price History**: Click the **📈 History** button to see a log of all previous price changes.
    *   **Auto-Fix**: Automatically handles unescaped quotes in specs to prevent site crashes.

2.  **🚀 Smart Importer**: Add new phones in seconds.
    *   **Full Auto-Add**: Type a phone name (e.g., "Samsung M55") and click. It will automatically download the **Specs** AND the **Official Photo** from GSMArena.
    *   **Image Optimization**: All photos are automatically resized to **800px** for maximum website speed.

3.  **🛠️ Batch Tools**: Manage your entire shop at once.
    *   **💰 Bulk Price Updater**: Increase or decrease prices for all phones or a specific brand by a percentage (%) or fixed amount (DZD).
    *   **Bulk Download**: Finds missing photos for all phones in your database automatically.

**To run the tool:**
```bash
# Make sure Pillow is installed for image resizing
pip install Pillow
python3 SmartPhoneManager.py
```

---

## ✨ Website Features

*   **Custom Installment Filter**: Users can filter by their monthly budget (DZD/month).
*   **"Sold Out" Support**: Inventory status is visually reflected with red "نفذت الكمية" badges.
*   **Detailed WhatsApp Orders**: Customer messages now include specific RAM/Storage and chosen payment plans.
*   **Performance**: native `loading="lazy"` and auto-resized images ensure a smooth experience even on mobile data.

---

## 💻 For Developers

### Data Format
The `js/phones_data.js` now supports advanced fields like `status` and `price_history`:
```javascript
{
    id: 51,
    name: "Samsung Galaxy M55s 5G",
    brand: "Samsung",
    price: 38000,
    status: "available",
    price_history: [{ date: "2026-06-07", price: 38000 }],
    specs: {
        screen: "6.7 inches",
        refresh: "120Hz",
        ram: "8GB",
        storage: "128GB",
        // ...
    }
},
```

---
*This project was developed with the assistance of Gemini CLI. Documentation last updated on June 7, 2026.*
