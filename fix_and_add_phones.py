import os

JS_FILE_PATH = os.path.join("js", "script.js")

new_phones_data = [
    {
        "id": 16,
        "name": "Samsung Galaxy A05s",
        "brand": "Samsung",
        "price": 23500,
        "rating": 4.2,
        "specs": {"screen": "6.7\" PLS LCD", "refresh": "90Hz", "ram": "4GB", "storage": "128GB", "camera": "50MP Main", "battery": "5000mAh", "processor": "Snapdragon 680", "network": "4G"}
    },
    {
        "id": 17,
        "name": "Xiaomi Redmi 13C",
        "brand": "Xiaomi",
        "price": 26000,
        "rating": 4.1,
        "specs": {"screen": "6.74\" IPS LCD", "refresh": "90Hz", "ram": "6GB", "storage": "128GB", "camera": "50MP Main", "battery": "5000mAh", "processor": "Helio G85", "network": "4G"}
    },
    {
        "id": 18,
        "name": "Realme C53",
        "brand": "Realme",
        "price": 25000,
        "rating": 4.0,
        "specs": {"screen": "6.74\" IPS LCD", "refresh": "90Hz", "ram": "6GB", "storage": "128GB", "camera": "50MP Main", "battery": "5000mAh", "processor": "Unisoc T612", "network": "4G"}
    },
    {
        "id": 19,
        "name": "Infinix Hot 40i",
        "brand": "Infinix",
        "price": 22000,
        "rating": 4.0,
        "specs": {"screen": "6.56\" IPS LCD", "refresh": "90Hz", "ram": "4GB", "storage": "128GB", "camera": "50MP Main", "battery": "5000mAh", "processor": "Unisoc T606", "network": "4G"}
    },
    {
        "id": 20,
        "name": "Tecno Spark 20",
        "brand": "Tecno",
        "price": 24500,
        "rating": 4.1,
        "specs": {"screen": "6.6\" IPS LCD", "refresh": "90Hz", "ram": "8GB", "storage": "256GB", "camera": "50MP Main", "battery": "5000mAh", "processor": "Helio G85", "network": "4G"}
    },
    {
        "id": 21,
        "name": "Samsung Galaxy A15",
        "brand": "Samsung",
        "price": 34000,
        "rating": 4.5,
        "specs": {"screen": "6.5\" Super AMOLED", "refresh": "90Hz", "ram": "6GB", "storage": "128GB", "camera": "50MP Main", "battery": "5000mAh", "processor": "Helio G99", "network": "4G"}
    },
    {
        "id": 22,
        "name": "Xiaomi Redmi A3",
        "brand": "Xiaomi",
        "price": 18500,
        "rating": 3.8,
        "specs": {"screen": "6.71\" IPS LCD", "refresh": "90Hz", "ram": "3GB", "storage": "64GB", "camera": "8MP Main", "battery": "5000mAh", "processor": "Helio G36", "network": "4G"}
    },
    {
        "id": 23,
        "name": "Samsung Galaxy A25",
        "brand": "Samsung",
        "price": 46000,
        "rating": 4.6,
        "specs": {"screen": "6.5\" Super AMOLED", "refresh": "120Hz", "ram": "8GB", "storage": "256GB", "camera": "50MP OIS", "battery": "5000mAh", "processor": "Exynos 1280", "network": "5G"}
    },
    {
        "id": 24,
        "name": "Xiaomi Redmi Note 13 Pro 4G",
        "brand": "Xiaomi",
        "price": 54000,
        "rating": 4.7,
        "specs": {"screen": "6.67\" AMOLED", "refresh": "120Hz", "ram": "8GB", "storage": "256GB", "camera": "200MP OIS", "battery": "5000mAh", "processor": "Helio G99 Ultra", "network": "4G"}
    },
    {
        "id": 25,
        "name": "Realme 11 Pro",
        "brand": "Realme",
        "price": 62000,
        "rating": 4.6,
        "specs": {"screen": "6.7\" AMOLED Curved", "refresh": "120Hz", "ram": "8GB", "storage": "256GB", "camera": "100MP OIS", "battery": "5000mAh", "processor": "Dimensity 7050", "network": "5G"}
    },
    {
        "id": 26,
        "name": "Infinix Note 40 Pro",
        "brand": "Infinix",
        "price": 58000,
        "rating": 4.5,
        "specs": {"screen": "6.78\" AMOLED", "refresh": "120Hz", "ram": "12GB", "storage": "256GB", "camera": "108MP OIS", "battery": "5000mAh", "processor": "Helio G99 Ultimate", "network": "4G"}
    },
    {
        "id": 27,
        "name": "Poco X6 Pro",
        "brand": "Xiaomi",
        "price": 78000,
        "rating": 4.8,
        "specs": {"screen": "6.67\" AMOLED", "refresh": "120Hz", "ram": "12GB", "storage": "512GB", "camera": "64MP OIS", "battery": "5000mAh", "processor": "Dimensity 8300 Ultra", "network": "5G"}
    },
    {
        "id": 28,
        "name": "Samsung Galaxy M55",
        "brand": "Samsung",
        "price": 69000,
        "rating": 4.4,
        "specs": {"screen": "6.7\" Super AMOLED", "refresh": "120Hz", "ram": "8GB", "storage": "256GB", "camera": "50MP OIS", "battery": "5000mAh", "processor": "Snapdragon 7 Gen 1", "network": "5G"}
    },
    {
        "id": 29,
        "name": "Oppo Reno 11 F",
        "brand": "Oppo",
        "price": 65000,
        "rating": 4.5,
        "specs": {"screen": "6.7\" AMOLED", "refresh": "120Hz", "ram": "8GB", "storage": "256GB", "camera": "64MP Main", "battery": "5000mAh", "processor": "Dimensity 7050", "network": "5G"}
    },
    {
        "id": 30,
        "name": "Tecno Camon 30",
        "brand": "Tecno",
        "price": 49000,
        "rating": 4.3,
        "specs": {"screen": "6.78\" AMOLED", "refresh": "120Hz", "ram": "12GB", "storage": "512GB", "camera": "50MP OIS", "battery": "5000mAh", "processor": "Helio G99 Ultimate", "network": "4G"}
    },
    {
        "id": 31,
        "name": "Samsung Galaxy S23 FE",
        "brand": "Samsung",
        "price": 95000,
        "rating": 4.6,
        "specs": {"screen": "6.4\" Dynamic AMOLED", "refresh": "120Hz", "ram": "8GB", "storage": "256GB", "camera": "50MP Triple", "battery": "4500mAh", "processor": "Exynos 2200", "network": "5G"}
    },
    {
        "id": 32,
        "name": "Xiaomi 13T",
        "brand": "Xiaomi",
        "price": 89000,
        "rating": 4.7,
        "specs": {"screen": "6.67\" AMOLED", "refresh": "144Hz", "ram": "12GB", "storage": "256GB", "camera": "50MP Leica", "battery": "5000mAh", "processor": "Dimensity 8200 Ultra", "network": "5G"}
    },
    {
        "id": 33,
        "name": "Poco F6",
        "brand": "Xiaomi",
        "price": 92000,
        "rating": 4.8,
        "specs": {"screen": "6.67\" AMOLED", "refresh": "120Hz", "ram": "12GB", "storage": "512GB", "camera": "50MP OIS", "battery": "5000mAh", "processor": "Snapdragon 8s Gen 3", "network": "5G"}
    },
    {
        "id": 34,
        "name": "Google Pixel 7a",
        "brand": "Google Pixel",
        "price": 85000,
        "rating": 4.5,
        "specs": {"screen": "6.1\" OLED", "refresh": "90Hz", "ram": "8GB", "storage": "128GB", "camera": "64MP Dual", "battery": "4385mAh", "processor": "Tensor G2", "network": "5G"}
    },
    {
        "id": 35,
        "name": "Realme GT 6",
        "brand": "Realme",
        "price": 115000,
        "rating": 4.9,
        "specs": {"screen": "6.78\" LTPO AMOLED", "refresh": "120Hz", "ram": "16GB", "storage": "512GB", "camera": "50MP OIS", "battery": "5500mAh", "processor": "Snapdragon 8s Gen 3", "network": "5G"}
    },
    {
        "id": 36,
        "name": "OnePlus 12R",
        "brand": "OnePlus",
        "price": 120000,
        "rating": 4.7,
        "specs": {"screen": "6.78\" LTPO4 AMOLED", "refresh": "120Hz", "ram": "16GB", "storage": "256GB", "camera": "50MP OIS", "battery": "5500mAh", "processor": "Snapdragon 8 Gen 2", "network": "5G"}
    },
    {
        "id": 37,
        "name": "Samsung Galaxy S24",
        "brand": "Samsung",
        "price": 165000,
        "rating": 4.8,
        "specs": {"screen": "6.2\" Dynamic LTPO", "refresh": "120Hz", "ram": "8GB", "storage": "256GB", "camera": "50MP Triple", "battery": "4000mAh", "processor": "Exynos 2400", "network": "5G"}
    },
    {
        "id": 38,
        "name": "iPhone 13",
        "brand": "Apple",
        "price": 110000,
        "rating": 4.7,
        "specs": {"screen": "6.1\" Super Retina", "refresh": "60Hz", "ram": "4GB", "storage": "128GB", "camera": "12MP Dual", "battery": "3240mAh", "processor": "A15 Bionic", "network": "5G"}
    },
    {
        "id": 39,
        "name": "iPhone 14 Pro Max",
        "brand": "Apple",
        "price": 230000,
        "rating": 4.9,
        "specs": {"screen": "6.7\" Super Retina", "refresh": "120Hz", "ram": "6GB", "storage": "256GB", "camera": "48MP Triple", "battery": "4323mAh", "processor": "A16 Bionic", "network": "5G"}
    },
    {
        "id": 40,
        "name": "iPhone 15",
        "brand": "Apple",
        "price": 175000,
        "rating": 4.8,
        "specs": {"screen": "6.1\" Super Retina", "refresh": "60Hz", "ram": "6GB", "storage": "128GB", "camera": "48MP Dual", "battery": "3349mAh", "processor": "A16 Bionic", "network": "5G"}
    },
    {
        "id": 41,
        "name": "Samsung Galaxy Z Flip 5",
        "brand": "Samsung",
        "price": 155000,
        "rating": 4.6,
        "specs": {"screen": "6.7\" Foldable AMOLED", "refresh": "120Hz", "ram": "8GB", "storage": "512GB", "camera": "12MP Dual", "battery": "3700mAh", "processor": "Snapdragon 8 Gen 2", "network": "5G"}
    },
    {
        "id": 42,
        "name": "Xiaomi 14",
        "brand": "Xiaomi",
        "price": 160000,
        "rating": 4.8,
        "specs": {"screen": "6.36\" LTPO OLED", "refresh": "120Hz", "ram": "12GB", "storage": "512GB", "camera": "50MP Leica", "battery": "4610mAh", "processor": "Snapdragon 8 Gen 3", "network": "5G"}
    },
    {
        "id": 43,
        "name": "Honor Magic 6 Pro",
        "brand": "Huawei", 
        "price": 215000,
        "rating": 4.9,
        "specs": {"screen": "6.8\" LTPO OLED", "refresh": "120Hz", "ram": "12GB", "storage": "512GB", "camera": "180MP Periscope", "battery": "5600mAh", "processor": "Snapdragon 8 Gen 3", "network": "5G"}
    },
    {
        "id": 44,
        "name": "Google Pixel 9",
        "brand": "Google Pixel",
        "price": 190000,
        "rating": 4.8,
        "specs": {"screen": "6.3\" OLED", "refresh": "120Hz", "ram": "12GB", "storage": "256GB", "camera": "50MP Dual", "battery": "4700mAh", "processor": "Tensor G4", "network": "5G"}
    },
    {
        "id": 45,
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

    # Create JS string entries
    new_entries_str = ""
    for phone in new_phones_data:
        safe_name = phone['name'].replace(" ", "_").replace("/", "-")
        # Ensure we use the correct path that matches what bulk_image_updater downloaded
        img_path = f"Photos/{safe_name}.jpg"
        
        entry = f'''    {{
        id: {phone['id']},
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
    }},'''
        new_entries_str += "\n" + entry

    # Find the FIRST occurrence of "];" which closes the "const products" array.
    # The first one is around line 279 in the clean file.
    
    first_closing_bracket = content.find("];")
    
    if first_closing_bracket != -1:
        new_content = content[:first_closing_bracket] + new_entries_str + "\n" + content[first_closing_bracket:]
        
        with open(JS_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ Added phones to the CORRECT location in script.js")
    else:
        print("❌ Could not find closing bracket of products array")

if __name__ == "__main__":
    main()