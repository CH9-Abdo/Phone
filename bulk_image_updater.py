import os
import re
import requests
import time
from bs4 import BeautifulSoup

# Configuration
JS_FILE_PATH = os.path.join("js", "phones_data.js")
PHOTOS_DIR = "Photos"

# Headers for scraping
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def download_phone_image(phone_name):
    """
    Searches for a phone on GSMArena and downloads the main image.
    Returns the filename of the saved image, or None if failed.
    """
    print(f"🔍 Searching for: {phone_name}...")
    
    try:
        # 1. Search GSMArena
        search_url = "https://www.gsmarena.com/results.php3"
        params = {"sQuickSearch": "yes", "sName": phone_name}
        
        response = requests.get(search_url, params=params, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 2. Find phone link
        phone_link = soup.select_one('.makers a')
        if not phone_link:
            print(f"❌ Phone not found on GSMArena: {phone_link}")
            return None
            
        phone_url = "https://www.gsmarena.com/" + phone_link['href']
        
        # 3. Get phone page
        response = requests.get(phone_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 4. Find main image
        main_img = soup.select_one('.specs-photo-main img')
        if not main_img or not main_img.get('src'):
            print(f"❌ No image found for: {phone_name}")
            return None
            
        img_url = main_img['src']
        if not img_url.startswith('http'):
            img_url = 'https://www.gsmarena.com/' + img_url
            
        # 5. Download image
        img_response = requests.get(img_url, headers=HEADERS, timeout=10)
        img_response.raise_for_status()
        
        # 6. Save image
        ext = img_url.split('.')[-1].split('?')[0]
        if ext not in ['jpg', 'jpeg', 'png', 'webp']:
            ext = 'jpg'
            
        # Create filename based on phone name
        safe_name = phone_name.replace(" ", "_").replace("/", "-")
        filename = f"{safe_name}.{ext}"
        filepath = os.path.join(PHOTOS_DIR, filename)
        
        # Ensure Photos dir exists
        os.makedirs(PHOTOS_DIR, exist_ok=True)
        
        with open(filepath, 'wb') as f:
            f.write(img_response.content)
            
        print(f"✅ Downloaded: {filename}")
        return f"{PHOTOS_DIR}/{filename}"
        
    except Exception as e:
        print(f"⚠️ Error downloading {phone_name}: {e}")
        return None

def main():
    if not os.path.exists(JS_FILE_PATH):
        print(f"Error: {JS_FILE_PATH} not found.")
        return

    with open(JS_FILE_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    modified_lines = []
    current_phone_name = None
    
    print("🚀 Starting bulk update...")

    for line in lines:
        # 1. Capture Phone Name
        # Looking for line like: name: "Samsung Galaxy S24",
        name_match = re.search(r'name:\s*"(.*?)",', line)
        if name_match:
            current_phone_name = name_match.group(1)
            
        # 2. Check for Image
        # Looking for line like: image: "...",
        img_match = re.search(r'image:\s*"(.*?)",', line)
        if img_match:
            current_image = img_match.group(1)
            
            should_download = False
            
            # Check if it's a URL
            if current_image.startswith("http"):
                should_download = True
            # Check if it's a local file that is MISSING
            elif not os.path.exists(current_image):
                 # Try with current working dir prefix just in case
                 if not os.path.exists(os.path.join(os.getcwd(), current_image)):
                     should_download = True
            
            if should_download and current_phone_name:
                print(f"🔄 Processing {current_phone_name}...")
                time.sleep(2) # Avoid Rate Limiting
                new_image_path = download_phone_image(current_phone_name)
                
                if new_image_path:
                    # Replace the URL with the new local path
                    # We use replace on the string literal to be safe
                    line = line.replace(f'"{current_image}"', f'"{new_image_path}"')
        
        modified_lines.append(line)

    # Write everything back
    with open(JS_FILE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(modified_lines)
        
    print("\n🎉 Process completed! js/script.js updated.")

if __name__ == "__main__":
    main()