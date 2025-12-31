# 📱 Djellal Boutique - Your Premier Smartphone Store

Welcome to **Djellal Boutique**, a modern, responsive web application for showcasing smartphones with installment plans. This project is built with standard HTML, CSS, and vanilla JavaScript, making it fast and easy to deploy.

## 🚀 How to Run

This is a static website, so no complex backend is needed.

1.  **Open locally (Simplest):**
    Simply double-click `index.html` to open it in your favorite web browser.

2.  **Using a local server (Recommended for development):**
    For the best experience without potential file access issues (CORS), run a simple local server. If you have Python installed:
    ```bash
    # Make sure you are in the project directory
    python3 -m http.server 8000
    ```
    Then, open `http://localhost:8000` in your browser.

## 📂 Project Structure

```
Le_Boutique/
├── css/
│   └── style.css          # Main stylesheet for the website
├── js/
│   ├── phones_data.js     # DATABASE: Contains the list of all phone products
│   └── script.js          # LOGIC: Core application logic (rendering, filtering, pagination)
├── Photos/                # Folder containing all downloaded phone images
├── index.html             # Main entry point of the website
│
├── admin_manager.py       # GUI tool to manage phones (add/edit/delete)
├── phone_downloader.py    # GUI tool to download a single phone's images
│
└── README.md              # Project documentation
```

---


## 🛠️ How to Manage Products

We have provided custom Python tools to make managing your inventory easy.

### `admin_manager.py` (Main Tool)
This is a **graphical interface** to add, edit, or remove phones from your database (`js/phones_data.js`) without touching any code.

1.  **Run the tool:**
    ```bash
    python3 admin_manager.py
    ```
2.  Use the list to select a phone and the form to edit its details.
3.  Click "Save Changes" to update the `phones_data.js` file automatically.

### `phone_downloader.py`
A simple GUI tool to quickly download images for a **single phone** from GSMArena. It's useful if you only need to add one or two phones.

1.  **Run the tool:**
    ```bash
    python3 phone_downloader.py
    ```
2.  Type the phone name (e.g., "Samsung S24") and click Download.
3.  The images will be saved in the `Photos` folder.

---


## ⚙️ Maintenance & Utility Scripts

Over time, we created several scripts to perform bulk updates and fixes. **You generally do not need to run these again**, but they are documented here for completeness.

*   `bulk_image_updater.py`: This powerful script reads the `js/phones_data.js` file, finds any phones that have a web URL or a missing local image, and automatically searches GSMArena to download a new, high-quality local image for them. It's the best way to add images for many phones at once.

*   `add_phones_generator.py` & `fix_and_add_phones.py`: These were one-time scripts created to add a large batch of 30 phones to the database and fix insertion errors. They can be re-used or adapted if you need to add another large batch in the future.

*   `fix_quotes.py`: A one-time utility script created to fix a specific syntax error in `js/phones_data.js` where unescaped double quotes (e.g., `6.7"`) were causing the site to fail.

---


## 💻 For Developers

### Adding a New Phone Manually
1.  Open `js/phones_data.js`.
2.  Add a new object to the `products` array. **Remember to escape quotes inside strings!**
```javascript
{
    id: 46, // Must be a unique ID
    name: "My New Phone",
    brand: "MyBrand",
    price: 50000,
    image: "Photos/my_new_phone.jpg", // The image path
    rating: 4.5,
    specs: {
        screen: "6.5\" AMOLED", // Note: The quote for inches is escaped: \"
        refresh: "120Hz",
        ram: "8GB",
        storage: "256GB",
        camera: "50MP",
        battery: "5000mAh",
        processor: "MyChip",
        network: "5G"
    }
},
```
3. After adding, you can run `python3 bulk_image_updater.py` to automatically download the image for `my_new_phone.jpg`.

### Customizing Styles
Edit `css/style.css` to change colors, fonts, or layout. The CSS variables at the top of the file control the main color scheme.

---
*This project was developed with the assistance of Gemini. Documentation last updated on 2025-12-31.*
