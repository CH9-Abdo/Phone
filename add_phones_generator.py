import os
import re

JS_FILE_PATH = os.path.join("js", "script.js")

# List of 30 phones popular in Algeria (Prices are approximate estimates in DZD)
new_phones_data = [
    # --- Budget / Entry Level (20k - 40k) ---
    {
        "name": "Samsung Galaxy A05s",
        "brand": "Samsung",
        "price": 23500,
        "rating": 4.2,
        "specs": {"screen": "6.7\" PLS LCD", "refresh": "90Hz", "ram": "4GB", "storage": "128GB", "camera": "50MP Main", "battery": "5000mAh", "processor": "Snapdragon 680", "network": "4G"}
    },
    {
        "name": "Xiaomi Redmi 13C",
        "brand": "Xiaomi",
        "price": 26000,
        "rating": 4.1,
        "specs": {"screen": "6.74\" IPS LCD", "refresh": "90Hz", "ram": "6GB", "storage": "128GB", "camera": "50MP Main", "battery": "5000mAh", "processor": "Helio G85", "network": "4G"}
    },
    {
        "name": "Realme C53",
        "brand": "Realme",
        "price": 25000,
        "rating": 4.0,
        "specs": {"screen": "6.74\" IPS LCD", "refresh": "90Hz", "ram": "6GB", "storage": "128GB", "camera": "50MP Main", "battery": "5000mAh", "processor": "Unisoc T612", "network": "4G"}
    },
    {
        "name": "Infinix Hot 40i",
        "brand": "Infinix",
        "price": 22000,
        "rating": 4.0,
        "specs": {"screen": "6.56\" IPS LCD", "refresh": "90Hz", "ram": "4GB", "storage": "128GB", "camera": "50MP Main", "battery": "5000mAh", "processor": "Unisoc T606", "network": "4G"}
    },
    {
        "name": "Tecno Spark 20",
        "brand": "Tecno",
        "price": 24500,
        "rating": 4.1,
        "specs": {"screen": "6.6\" IPS LCD", "refresh": "90Hz", "ram": "8GB", "storage": "256GB", "camera": "50MP Main", "battery": "5000mAh", "processor": "Helio G85", "network": "4G"}
    },
    {
        "name": "Samsung Galaxy A15",
        "brand": "Samsung",
        "price": 34000,
        "rating": 4.5,
        "specs": {"screen": "6.5\" Super AMOLED", "refresh": "90Hz", "ram": "6GB", "storage": "128GB", "camera": "50MP Main", "battery": "5000mAh", "processor": "Helio G99", "network": "4G"}
    },
    {
        "name": "Xiaomi Redmi A3",
        "brand": "Xiaomi",
        "price": 18500,
        "rating": 3.8,
        "specs": {"screen": "6.71\" IPS LCD", "refresh": "90Hz", "ram": "3GB", "storage": "64GB", "camera": "8MP Main", "battery": "5000mAh", "processor": "Helio G36", "network": "4G"}
    },
    
    # --- Mid Range (40k - 80k) ---
    {
        "name": "Samsung Galaxy A25",
        "brand": "Samsung",
        "price": 46000,
        "rating": 4.6,
        "specs": {"screen": "6.5\" Super AMOLED", "refresh": "120Hz", "ram": "8GB", "storage": "256GB", "camera": "50MP OIS", "battery": "5000mAh", "processor": "Exynos 1280", "network": "5G"}
    },
    {
        "name": "Xiaomi Redmi Note 13 Pro 4G",
        "brand": "Xiaomi",
        "price": 54000,
        "rating": 4.7,
        "specs": {"screen": "6.67\" AMOLED", "refresh": "120Hz", "ram": "8GB", "storage": "256GB", "camera": "200MP OIS", "battery": "5000mAh", "processor": "Helio G99 Ultra", "network": "4G"}
    },
    {
        "name": "Realme 11 Pro",
        "brand": "Realme",
        "price": 62000,
        "rating": 4.6,
        "specs": {"screen": "6.7\" AMOLED Curved", "refresh": "120Hz", "ram": "8GB", "storage": "256GB", "camera": "100MP OIS", "battery": "5000mAh", "processor": "Dimensity 7050", "network": "5G"}
    },
    {
        "name": "Infinix Note 40 Pro",
        "brand": "Infinix",
        "price": 58000,
        "rating": 4.5,
        "specs": {"screen": "6.78\" AMOLED", "refresh": "120Hz", "ram": "12GB", "storage": "256GB", "camera": "108MP OIS", "battery": "5000mAh", "processor": "Helio G99 Ultimate", "network": "4G"}
    },
    {
        "name": "Poco X6 Pro",
        "brand": "Xiaomi",
        "price": 78000,
        "rating": 4.8,
        "specs": {"screen": "6.67\" AMOLED", "refresh": "120Hz", "ram": "12GB", "storage": "512GB", "camera": "64MP OIS", "battery": "5000mAh", "processor": "Dimensity 8300 Ultra", "network": "5G"}
    },
    {
        "name": "Samsung Galaxy M55",
        "brand": "Samsung",
        "price": 69000,
        "rating": 4.4,
        "specs": {"screen": "6.7\" Super AMOLED", "refresh": "120Hz", "ram": "8GB", "storage": "256GB", "camera": "50MP OIS", "battery": "5000mAh", "processor": "Snapdragon 7 Gen 1", "network": "5G"}
    },
    {
        "name": "Oppo Reno 11 F",
        "brand": "Oppo",
        "price": 65000,
        "rating": 4.5,
        "specs": {"screen": "6.7\" AMOLED", "refresh": "120Hz", "ram": "8GB", "storage": "256GB", "camera": "64MP Main", "battery": "5000mAh", "processor": "Dimensity 7050", "network": "5G"}
    },
    {
        "name": "Tecno Camon 30",
        "brand": "Tecno",
        "price": 49000,
        "rating": 4.3,
        "specs": {"screen": "6.78\" AMOLED", "refresh": "120Hz", "ram": "12GB", "storage": "512GB", "camera": "50MP OIS", "battery": "5000mAh", "processor": "Helio G99 Ultimate", "network": "4G"}
    },

    # --- Flagship Killers / High End (80k - 150k) ---
    {
        "name": "Samsung Galaxy S23 FE",
        "brand": "Samsung",
        "price": 95000,
        "rating": 4.6,
        "specs": {"screen": "6.4\" Dynamic AMOLED", "refresh": "120Hz", "ram": "8GB", "storage": "256GB", "camera": "50MP Triple", "battery": "4500mAh", "processor": "Exynos 2200", "network": "5G"}
    },
    {
        "name": "Xiaomi 13T",
        "brand": "Xiaomi",
        "price": 89000,
        "rating": 4.7,
        "specs": {"screen": "6.67\" AMOLED", "refresh": "144Hz", "ram": "12GB", "storage": "256GB", "camera": "50MP Leica", "battery": "5000mAh", "processor": "Dimensity 8200 Ultra", "network": "5G"}
    },
    {
        "name": "Poco F6",
        "brand": "Xiaomi",
        "price": 92000,
        "rating": 4.8,
        "specs": {"screen": "6.67\" AMOLED", "refresh": "120Hz", "ram": "12GB", "storage": "512GB", "camera": "50MP OIS", "battery": "5000mAh", "processor": "Snapdragon 8s Gen 3", "network": "5G"}
    },
    {
        "name": "Google Pixel 7a",
        "brand": "Google Pixel",
        "price": 85000,
        "rating": 4.5,
        "specs": {"screen": "6.1\" OLED", "refresh": "90Hz", "ram": "8GB", "storage": "128GB", "camera": "64MP Dual", "battery": "4385mAh", "processor": "Tensor G2", "network": "5G"}
    },
    {
        "name": "Realme GT 6",
        "brand": "Realme",
        "price": 115000,
        "rating": 4.9,
        "specs": {"screen": "6.78\" LTPO AMOLED", "refresh": "120Hz", "ram": "16GB", "storage": "512GB", "camera": "50MP OIS", "battery": "5500mAh", "processor": "Snapdragon 8s Gen 3", "network": "5G"}
    },
    {
        "name": "OnePlus 12R",
        "brand": "OnePlus",
        "price": 120000,
        "rating": 4.7,
        "specs": {"screen": "6.78\" LTPO4 AMOLED", "refresh": "120Hz", "ram": "16GB", "storage": "256GB", "camera": "50MP OIS", "battery": "5500mAh", "processor": "Snapdragon 8 Gen 2", "network": "5G"}
    },

    # --- Premium / Flagships (150k +) ---
    {
        "name": "Samsung Galaxy S24",
        "brand": "Samsung",
        "price": 165000,
        "rating": 4.8,
        "specs": {"screen": "6.2\" Dynamic LTPO", "refresh": "120Hz", "ram": "8GB", "storage": "256GB", "camera": "50MP Triple", "battery": "4000mAh", "processor": "Exynos 2400", "network": "5G"}
    },
    {
        "name": "iPhone 13",
        "brand": "Apple",
        "price": 110000,
        "rating": 4.7,
        "specs": {"screen": "6.1\" Super Retina", "refresh": "60Hz", "ram": "4GB", "storage": "128GB", "camera": "12MP Dual", "battery": "3240mAh", "processor": "A15 Bionic", "network": "5G"}
    },
    {
        "name": "iPhone 14 Pro Max",
        "brand": "Apple",
        "price": 230000,
        "rating": 4.9,
        "specs": {"screen": "6.7\" Super Retina", "refresh": "120Hz", "ram": "6GB", "storage": "256GB", "camera": "48MP Triple", "battery": "4323mAh", "processor": "A16 Bionic", "network": "5G"}
    },
    {
        "name": "iPhone 15",
        "brand": "Apple",
        "price": 175000,
        "rating": 4.8,
        "specs": {"screen": "6.1\" Super Retina", "refresh": "60Hz", "ram": "6GB", "storage": "128GB", "camera": "48MP Dual", "battery": "3349mAh", "processor": "A16 Bionic", "network": "5G"}
    },
    {
        "name": "Samsung Galaxy Z Flip 5",
        "brand": "Samsung",
        "price": 155000,
        "rating": 4.6,
        "specs": {"screen": "6.7\" Foldable AMOLED", "refresh": "120Hz", "ram": "8GB", "storage": "512GB", "camera": "12MP Dual", "battery": "3700mAh", "processor": "Snapdragon 8 Gen 2", "network": "5G"}
    },
    {
        "name": "Xiaomi 14",
        "brand": "Xiaomi",
        "price": 160000,
        "rating": 4.8,
        "specs": {"screen": "6.36\" LTPO OLED", "refresh": "120Hz", "ram": "12GB", "storage": "512GB", "camera": "50MP Leica", "battery": "4610mAh", "processor": "Snapdragon 8 Gen 3", "network": "5G"}
    },
    {
        "name": "Honor Magic 6 Pro",
        "brand": "Huawei", 
        "price": 215000,
        "rating": 4.9,
        "specs": {"screen": "6.8\" LTPO OLED", "refresh": "120Hz", "ram": "12GB", "storage": "512GB", "camera": "180MP Periscope", "battery": "5600mAh", "processor": "Snapdragon 8 Gen 3", "network": "5G"}
    },
    {
        "name": "Google Pixel 9",
        "brand": "Google Pixel",
        "price": 190000,
        "rating": 4.8,
        "specs": {"screen": "6.3\" OLED", "refresh": "120Hz", "ram": "12GB", "storage": "256GB", "camera": "50MP Dual", "battery": "4700mAh", "processor": "Tensor G4", "network": "5G"}
    },
    {
        "name": "Samsung Galaxy S23 Ultra",
        "brand": "Samsung",
        "price": 195000,
        "rating": 4.9,
        "specs": {"screen": "6.8\" Dynamic AMOLED", "refresh": "120Hz", "ram": "12GB", "storage": "512GB", "camera": "200MP Quad", "battery": "5000mAh", "processor": "Snapdragon 8 Gen 2", "network": "5G"}
    }
]

def main():
    if not os.path.exists(JS_FILE_PATH):
        print("JS File not found")
        return

    with open(JS_FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the last ID
    ids = re.findall(r'id:\s*(\d+)', content)
    last_id = int(ids[-1]) if ids else 0

    new_entries = []
    
    for phone in new_phones_data:
        last_id += 1
        safe_name = phone['name'].replace(" ", "_").replace("/", "-")
        # We point to a local file that doesn't exist yet, forcing the updater to fetch it
        img_path = f"Photos/{safe_name}.jpg"
        
        entry = f"""    {{
        id: {last_id},
        name: "{phone['name']}",
        brand: "{phone['brand']}",
        price: {phone['price']},
        image: "{img_path}",
        rating: {phone['rating']},
        specs: {{
            screen: "{phone['specs']['screen']}",
            refresh: "{phone['specs']['refresh']}",
            ram: "{phone['specs']['ram']}",
            storage: "{phone['specs']['storage']}",
            camera: "{phone['specs']['camera']}",
            battery: "{phone['specs']['battery']}",
            processor: "{phone['specs']['processor']}",
            network: "{phone['specs']['network']}",
        }},
    }},"""
        new_entries.append(entry)

    # Insert before the closing bracket of the array
    # Looking for the last "];"
    split_index = content.rfind("];")
    
    if split_index != -1:
        new_content = content[:split_index] + "\n".join(new_entries) + "\n" + content[split_index:]
        
        with open(JS_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Added {len(new_entries)} new phones to script.js")
    else:
        print("❌ Could not find end of products array")

if __name__ == "__main__":
    main()
