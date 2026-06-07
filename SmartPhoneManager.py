import sys
import os
import re
import json
import requests
import shutil
from datetime import datetime
from bs4 import BeautifulSoup
try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QTextEdit, 
                             QLabel, QFileDialog, QListWidget, QStackedWidget,
                             QFormLayout, QFrame, QMessageBox, QScrollArea,
                             QProgressBar, QListWidgetItem, QComboBox)
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette

# Configuration
JS_FILE_PATH = os.path.join("js", "phones_data.js")
PHOTOS_DIR = "Photos"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

class DownloadThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(dict) # Emits the full phone data if successful
    error = pyqtSignal(str)
    
    def __init__(self, phone_name, download_image=True):
        super().__init__()
        self.phone_name = phone_name
        self.download_image = download_image
        
    def run(self):
        try:
            self.progress.emit(f"🔍 Searching for: {self.phone_name}...")
            
            # 1. Search GSMArena
            search_url = "https://www.gsmarena.com/results.php3"
            params = {"sQuickSearch": "yes", "sName": self.phone_name}
            
            response = requests.get(search_url, params=params, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 2. Find phone link
            phone_link = soup.select_one('.makers a')
            if not phone_link:
                self.error.emit(f"❌ Phone not found: {self.phone_name}")
                return
                
            phone_url = "https://www.gsmarena.com/" + phone_link['href']
            
            # 3. Get phone page
            response = requests.get(phone_url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # --- SCRAPE SPECS ---
            specs = {
                'screen': "TBA",
                'refresh': "TBA",
                'ram': "TBA",
                'storage': "TBA",
                'camera': "TBA",
                'battery': "TBA",
                'processor': "TBA",
                'network': "TBA"
            }
            
            # Helper to find data by GSMArena's internal 'data-spec' attributes
            def get_by_data_spec(spec_name):
                tag = soup.select_one(f'.nfo[data-spec="{spec_name}"]')
                return tag.text.strip() if tag else "TBA"

            # 1. Screen Size
            specs['screen'] = get_by_data_spec('displaysize').split(',')[0]
            
            # 2. Refresh Rate (usually in displaytype like "AMOLED, 120Hz")
            display_type = get_by_data_spec('displaytype')
            refresh_match = re.search(r'(\d+Hz)', display_type)
            specs['refresh'] = refresh_match.group(1) if refresh_match else "60Hz"
            
            # 3. Memory (RAM and Storage usually in internalmemory like "128GB 8GB RAM")
            memory_info = get_by_data_spec('internalmemory')
            # Extract first storage mentioned (e.g. 128GB)
            storage_match = re.search(r'(\d+GB|\d+TB)', memory_info)
            specs['storage'] = storage_match.group(1) if storage_match else "TBA"
            # Extract first RAM mentioned (e.g. 8GB RAM)
            ram_match = re.search(r'(\d+GB RAM|\d+GB)', memory_info.split(',')[-1])
            specs['ram'] = ram_match.group(0).replace(" RAM", "") if ram_match else "TBA"
            
            # 4. Camera (Main)
            specs['camera'] = get_by_data_spec('cam1modules').split(',')[0]
            
            # 5. Battery
            specs['battery'] = get_by_data_spec('batdescription1').split(',')[0]
            
            # 6. Processor
            specs['processor'] = get_by_data_spec('chipset').split('(')[0].strip()
            
            # 7. Network
            net_tech = get_by_data_spec('nettech')
            specs['network'] = "5G" if "5G" in net_tech else "4G"

            # --- DOWNLOAD IMAGE ---
            img_path = ""
            if self.download_image:
                main_img = soup.select_one('.specs-photo-main img')
                if main_img and main_img.get('src'):
                    img_url = main_img['src']
                    if not img_url.startswith('http'):
                        img_url = 'https://www.gsmarena.com/' + img_url
                    
                    os.makedirs(PHOTOS_DIR, exist_ok=True)
                    safe_name = self.phone_name.replace(" ", "_").replace("/", "-")
                    filename = f"{safe_name}.jpg"
                    filepath = os.path.join(PHOTOS_DIR, filename)
                    
                    img_res = requests.get(img_url, headers=HEADERS, timeout=10)
                    img_res.raise_for_status()
                    
                    with open(filepath, 'wb') as f:
                        f.write(img_res.content)
                    
                    # --- IMAGE RESIZING ---
                    if HAS_PILLOW:
                        try:
                            img = Image.open(filepath)
                            img.thumbnail((800, 800))
                            img.save(filepath, "JPEG", quality=85)
                            self.progress.emit(f"⚡ Image optimized (resized to 800px)")
                        except Exception as e:
                            self.progress.emit(f"⚠️ Optimization failed: {str(e)}")
                    
                    img_path = f"{PHOTOS_DIR}/{filename}"
                    self.progress.emit(f"✅ Image downloaded: {filename}")

            full_data = {
                'name': self.phone_name,
                'brand': self.phone_name.split(' ')[0],
                'specs': specs,
                'image': img_path
            }
            
            self.finished.emit(full_data)
            
        except Exception as e:
            self.error.emit(f"❌ Error: {str(e)}")

class SmartPhoneManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.phones = []
        self.current_js_content = ""
        self.active_threads = [] # To prevent garbage collection
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.setWindowTitle("🚀 SmartPhone Manager 2026")
        self.resize(1200, 800)
        
        # Stylesheet
        self.setStyleSheet("""
            QMainWindow { background-color: #f0f2f5; }
            #Sidebar { 
                background-color: #1e293b; 
                min-width: 220px; 
                max-width: 220px;
            }
            #Sidebar QListWidget {
                background-color: transparent;
                border: none;
                color: #cbd5e1;
                font-size: 14px;
                outline: none;
            }
            #Sidebar QListWidget::item {
                padding: 15px;
                border-radius: 5px;
                margin: 5px 10px;
            }
            #Sidebar QListWidget::item:selected {
                background-color: #38bdf8;
                color: white;
            }
            #Content { background-color: white; border-top-left-radius: 20px; }
            QPushButton#Primary {
                background-color: #0ea5e9;
                color: white;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton#Primary:hover { background-color: #0284c7; }
            QPushButton#Danger {
                background-color: #ef4444;
                color: white;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton#Danger:hover { background-color: #dc2626; }
            QLineEdit, QTextEdit {
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 8px;
                background: #f8fafc;
            }
            QLabel#Header { font-size: 24px; font-weight: bold; color: #0f172a; }
            QScrollArea { border: none; }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Sidebar
        sidebar_frame = QFrame()
        sidebar_frame.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(sidebar_frame)
        
        logo = QLabel("📱 PhoneManager")
        logo.setStyleSheet("color: white; font-size: 20px; font-weight: bold; padding: 20px;")
        sidebar_layout.addWidget(logo)

        self.nav_list = QListWidget()
        self.nav_list.addItem(QListWidgetItem("📋 Phone List"))
        self.nav_list.addItem(QListWidgetItem("⬇️ Downloader"))
        self.nav_list.addItem(QListWidgetItem("🛠️ Batch Tools"))
        self.nav_list.currentRowChanged.connect(self.switch_tab)
        sidebar_layout.addWidget(self.nav_list)
        sidebar_layout.addStretch()
        
        layout.addWidget(sidebar_frame)

        # Main Content
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("Content")
        
        self.setup_list_tab()
        self.setup_download_tab()
        self.setup_tools_tab()
        
        layout.addWidget(self.content_stack)

    def switch_tab(self, index):
        self.content_stack.setCurrentIndex(index)

    # --- TAB: List & Editor ---
    def setup_list_tab(self):
        page = QWidget()
        layout = QHBoxLayout(page)
        
        # Left side: List
        left_panel = QVBoxLayout()
        header = QLabel("Smartphone List")
        header.setObjectName("Header")
        left_panel.addWidget(header)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search phones...")
        self.search_input.textChanged.connect(self.filter_phones)
        left_panel.addWidget(self.search_input)
        
        self.phone_list = QListWidget()
        self.phone_list.currentRowChanged.connect(self.load_phone_details)
        left_panel.addWidget(self.phone_list)
        
        add_btn = QPushButton("+ Add New Phone")
        add_btn.setObjectName("Primary")
        add_btn.clicked.connect(self.new_phone)
        left_panel.addWidget(add_btn)
        
        layout.addLayout(left_panel, 1)
        
        # Right side: Form
        right_panel = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        form_container = QWidget()
        self.form_layout = QFormLayout(form_container)
        
        self.inputs = {}
        for key in ['Name', 'Brand', 'Price', 'Rating', 'Image']:
            self.inputs[key.lower()] = QLineEdit()
            self.form_layout.addRow(QLabel(f"{key}:"), self.inputs[key.lower()])
            
        self.inputs['status'] = QComboBox()
        self.inputs['status'].addItems(['available', 'out_of_stock'])
        self.form_layout.addRow(QLabel("Status:"), self.inputs['status'])

        self.form_layout.addRow(QLabel("<b>Specifications:</b>"), QLabel(""))
        for key in ['Screen', 'Refresh', 'RAM', 'Storage', 'Camera', 'Battery', 'Processor', 'Network']:
            self.inputs[key.lower()] = QLineEdit()
            self.form_layout.addRow(QLabel(f"  {key}:"), self.inputs[key.lower()])
            
        self.inputs['tag'] = QLineEdit()
        self.form_layout.addRow(QLabel("Special Tag:"), self.inputs['tag'])
        
        scroll.setWidget(form_container)
        right_panel.addWidget(scroll)
        
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("💾 Save Changes")
        self.save_btn.setObjectName("Primary")
        self.save_btn.clicked.connect(self.save_current_phone)
        
        self.hist_btn = QPushButton("📈 History")
        self.hist_btn.clicked.connect(self.show_price_history)

        self.del_btn = QPushButton("🗑️ Delete")
        self.del_btn.setObjectName("Danger")
        self.del_btn.clicked.connect(self.delete_current_phone)
        
        btn_layout.addWidget(self.del_btn)
        btn_layout.addWidget(self.hist_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.save_btn)
        right_panel.addLayout(btn_layout)
        
        layout.addLayout(right_panel, 2)
        self.content_stack.addWidget(page)

    # --- TAB: Downloader ---
    def setup_download_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        header = QLabel("Smart Importer")
        header.setObjectName("Header")
        layout.addWidget(header)
        
        layout.addWidget(QLabel("Enter a phone name to automatically download its <b>specs AND photo</b> from GSMArena."))
        
        search_layout = QHBoxLayout()
        self.dl_input = QLineEdit()
        self.dl_input.setPlaceholderText("Enter phone name (e.g. iPhone 17 Pro)")
        
        self.auto_add_btn = QPushButton("🚀 Full Auto-Add")
        self.auto_add_btn.setObjectName("Primary")
        self.auto_add_btn.setToolTip("Download specs + photo and add to list")
        self.auto_add_btn.clicked.connect(lambda: self.start_download(self.dl_input.text(), mode="auto-add"))
        
        self.dl_img_only_btn = QPushButton("🖼️ Just Photo")
        self.dl_img_only_btn.clicked.connect(lambda: self.start_download(self.dl_input.text(), mode="photo-only"))
        
        search_layout.addWidget(self.dl_input)
        search_layout.addWidget(self.auto_add_btn)
        search_layout.addWidget(self.dl_img_only_btn)
        layout.addLayout(search_layout)
        
        self.dl_log = QTextEdit()
        self.dl_log.setReadOnly(True)
        layout.addWidget(self.dl_log)
        
        self.content_stack.addWidget(page)

    # --- TAB: Tools ---
    def setup_tools_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        header = QLabel("Batch Tools")
        header.setObjectName("Header")
        layout.addWidget(header)
        
        btn1 = QPushButton("🆕 Add Popular 2026 Models")
        btn1.setMinimumHeight(60)
        btn1.clicked.connect(self.batch_add_phones)
        layout.addWidget(btn1)
        
        btn2 = QPushButton("🖼️ Bulk Download Missing Photos")
        btn2.setMinimumHeight(60)
        btn2.clicked.connect(self.bulk_download)
        layout.addWidget(btn2)
        
        # --- BULK PRICE SECTION ---
        bulk_group = QFrame()
        bulk_group.setStyleSheet("background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; margin-top: 20px;")
        bulk_l = QVBoxLayout(bulk_group)
        bulk_l.addWidget(QLabel("<b>💰 Bulk Price Updater</b>"))
        
        form = QHBoxLayout()
        self.bulk_brand = QComboBox()
        self.bulk_brand.addItem("All Brands")
        # Brands list will be populated later
        
        self.bulk_type = QComboBox()
        self.bulk_type.addItems(["Percentage (%)", "Fixed Amount (DZD)"])
        
        self.bulk_val = QLineEdit()
        self.bulk_val.setPlaceholderText("Value (e.g. 5 or -1000)")
        self.bulk_val.setFixedWidth(150)
        
        bulk_btn = QPushButton("Apply Change")
        bulk_btn.setObjectName("Primary")
        bulk_btn.clicked.connect(self.apply_bulk_update)
        
        form.addWidget(QLabel("Brand:"))
        form.addWidget(self.bulk_brand)
        form.addWidget(QLabel("Change By:"))
        form.addWidget(self.bulk_type)
        form.addWidget(self.bulk_val)
        form.addWidget(bulk_btn)
        bulk_l.addLayout(form)
        layout.addWidget(bulk_group)

        btn3 = QPushButton("✨ Fix Data Formatting (Quotes)")
        btn3.setMinimumHeight(60)
        btn3.clicked.connect(self.fix_quotes)
        layout.addWidget(btn3)
        
        layout.addStretch()
        self.content_stack.addWidget(page)

    # --- Logic: Data Handling ---
    def load_data(self):
        if not os.path.exists(JS_FILE_PATH):
            QMessageBox.critical(self, "Error", f"Could not find {JS_FILE_PATH}")
            return

        with open(JS_FILE_PATH, 'r', encoding='utf-8') as f:
            self.current_js_content = f.read()
            
        self.phones = self.parse_js_array(self.current_js_content)
        self.refresh_list()
        
        # Update bulk brands
        brands = sorted(list(set(p['brand'] for p in self.phones)))
        self.bulk_brand.clear()
        self.bulk_brand.addItem("All Brands")
        self.bulk_brand.addItems(brands)

    # ... [keep existing parse methods] ...

    def show_price_history(self):
        row = self.phone_list.currentRow()
        if row < 0: return
        p = self.phones[row]
        hist = p.get('price_history', [])
        if not hist:
            QMessageBox.information(self, "History", "No price history available for this phone.")
            return
        
        text = f"Price History for {p['name']}:\n\n"
        for entry in hist:
            text += f"• {entry['date']}: {entry['price']:,} DZD\n"
        
        QMessageBox.information(self, "History", text)

    def apply_bulk_update(self):
        brand = self.bulk_brand.currentText()
        change_type = self.bulk_type.currentText()
        try:
            val = float(self.bulk_val.text())
        except:
            QMessageBox.warning(self, "Error", "Invalid numeric value.")
            return
            
        if QMessageBox.question(self, "Confirm", f"Update prices for {brand} by {val}? This cannot be undone.") != QMessageBox.Yes:
            return
            
        count = 0
        for p in self.phones:
            if brand == "All Brands" or p['brand'] == brand:
                old_p = p['price']
                if "Percentage" in change_type:
                    p['price'] = int(p['price'] * (1 + val/100))
                else:
                    p['price'] = int(p['price'] + val)
                
                # Add to history if changed
                if old_p != p['price']:
                    if 'price_history' not in p: p['price_history'] = []
                    p['price_history'].append({
                        'date': datetime.now().strftime("%Y-%m-%d"),
                        'price': p['price']
                    })
                    count += 1
        
        self.write_to_js()
        self.refresh_list()
        QMessageBox.information(self, "Success", f"Updated {count} phones!")


    def parse_js_array(self, content):
        match = re.search(r'const products = \[\s*([\s\S]*?)\];', content)
        if not match: return []
        
        inner = match.group(1)
        objects = []
        depth = 0
        current = ""
        for char in inner:
            if char == '{': depth += 1
            if depth > 0: current += char
            if char == '}':
                depth -= 1
                if depth == 0:
                    objects.append(self.parse_obj(current))
                    current = ""
        return objects

    def parse_obj(self, s):
        data = {'specs': {}}
        # Simple regex extraction
        def get(pattern, default=""):
            m = re.search(pattern, s)
            return m.group(1) if m else default

        data['id'] = int(get(r'id:\s*(\d+)', "0"))
        data['name'] = get(r'name:\s*"(.*?)"')
        data['brand'] = get(r'brand:\s*"(.*?)"')
        data['price'] = int(get(r'price:\s*(\d+)', "0"))
        data['image'] = get(r'image:\s*"(.*?)"')
        data['rating'] = float(get(r'rating:\s*([\d\.]+)', "0"))
        data['status'] = get(r'status:\s*"(.*?)"', 'available')
        
        # Parse Price History
        data['price_history'] = []
        hist_m = re.search(r'price_history:\s*\[([\s\S]*?)\]', s)
        if hist_m:
            hist_str = hist_m.group(1)
            # Find { date: "...", price: ... } blocks
            entries = re.findall(r'\{\s*date:\s*"(.*?)",\s*price:\s*(\d+)\s*\}', hist_str)
            for d, p in entries:
                data['price_history'].append({'date': d, 'price': int(p)})

        specs_match = re.search(r'specs:\s*\{([\s\S]*?)\}', s)
        if specs_match:
            for line in specs_match.group(1).split(','):
                if ':' in line:
                    k, v = line.split(':', 1)
                    data['specs'][k.strip()] = v.strip().strip('"')
        
        tags_m = re.search(r'tags:\s*\[(.*?)\]', s)
        if tags_m:
            data['tags'] = [t.strip().strip('"') for t in tags_m.group(1).split(',') if t.strip()]
            
        return data

    def refresh_list(self):
        self.phone_list.clear()
        for p in self.phones:
            self.phone_list.addItem(p.get('name', 'Unknown'))

    def filter_phones(self, text):
        for i in range(self.phone_list.count()):
            item = self.phone_list.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def load_phone_details(self, row):
        if row < 0 or row >= len(self.phones): return
        p = self.phones[row]
        for key in self.inputs:
            if key == 'status':
                idx = self.inputs['status'].findText(p.get('status', 'available'))
                self.inputs['status'].setCurrentIndex(idx if idx >= 0 else 0)
            elif key in p:
                self.inputs[key].setText(str(p[key]))
            elif key in p.get('specs', {}):
                self.inputs[key].setText(str(p['specs'][key]))
            elif key == 'tag' and p.get('tags'):
                self.inputs[key].setText(p['tags'][0])
            else:
                if hasattr(self.inputs[key], 'clear'):
                    self.inputs[key].clear()

    def new_phone(self):
        for i in self.inputs.values(): i.clear()
        self.phone_list.clearSelection()
        self.inputs['name'].setFocus()

    def save_current_phone(self):
        name = self.inputs['name'].text()
        if not name: return
        
        row = self.phone_list.currentRow()
        new_price = int(self.inputs['price'].text() or 0)
        
        # Determine History
        history = []
        if row >= 0:
            p_old = self.phones[row]
            history = p_old.get('price_history', [])
            # If price changed, add to history
            if p_old.get('price') != new_price:
                history.append({
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'price': new_price
                })
        else:
            # New phone, start history
            history = [{'date': datetime.now().strftime("%Y-%m-%d"), 'price': new_price}]

        new_p = {
            'id': self.phones[row]['id'] if row >= 0 else self.get_next_id(),
            'name': name,
            'brand': self.inputs['brand'].text(),
            'price': new_price,
            'rating': float(self.inputs['rating'].text() or 0),
            'image': self.inputs['image'].text(),
            'status': self.inputs['status'].currentText(),
            'price_history': history,
            'specs': {k: self.inputs[k].text() for k in ['screen', 'refresh', 'ram', 'storage', 'camera', 'battery', 'processor', 'network']},
        }
        if self.inputs['tag'].text():
            new_p['tags'] = [self.inputs['tag'].text()]
            
        if row >= 0:
            self.phones[row] = new_p
        else:
            self.phones.append(new_p)
            
        self.write_to_js()
        self.refresh_list()
        QMessageBox.information(self, "Success", "Phone saved successfully!")

    def delete_current_phone(self):
        row = self.phone_list.currentRow()
        if row < 0: return
        if QMessageBox.question(self, "Delete", f"Are you sure you want to delete {self.phones[row]['name']}?") == QMessageBox.Yes:
            del self.phones[row]
            self.write_to_js()
            self.refresh_list()
            self.new_phone()

    def get_next_id(self):
        return max([p['id'] for p in self.phones] + [0]) + 1

    def write_to_js(self):
        js_parts = ["[\n"]
        for p in self.phones:
            js_parts.append("    {\n")
            js_parts.append(f'        id: {p["id"]},\n')
            js_parts.append(f'        name: "{p["name"]}",\n')
            js_parts.append(f'        brand: "{p["brand"]}",\n')
            js_parts.append(f'        price: {p["price"]},\n')
            js_parts.append(f'        image: "{p["image"]}",\n')
            js_parts.append(f'        rating: {p["rating"]},\n')
            js_parts.append(f'        status: "{p.get("status", "available")}",\n')
            
            # Write Price History
            if p.get('price_history'):
                hist_lines = []
                for entry in p['price_history']:
                    hist_lines.append(f'{{ date: "{entry["date"]}", price: {entry["price"]} }}')
                js_parts.append(f'        price_history: [{", ".join(hist_lines)}],\n')

            js_parts.append('        specs: {\n')
            for k, v in p['specs'].items():
                v_safe = v.replace('"', '\\"') # Auto-fix quotes
                js_parts.append(f'            {k}: "{v_safe}",\n')
            js_parts.append('        },\n')
            if 'tags' in p:
                js_parts.append(f'        tags: {json.dumps(p["tags"])},\n')
            js_parts.append("    },\n")
        js_parts.append("];")
        
        new_content = re.sub(
            r'const products = \[\s*([\s\S]*?)\];', 
            f'const products = {"".join(js_parts)}', 
            self.current_js_content
        )
        with open(JS_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        self.current_js_content = new_content

    # --- Logic: Downloader ---
    def start_download(self, name, mode="auto-add"):
        if not name: return
        self.dl_log.append(f"🚀 Starting {mode} for {name}...")
        
        thread = DownloadThread(name, download_image=True)
        thread.mode = mode # Custom attribute for the callback
        thread.progress.connect(lambda m: self.dl_log.append(m))
        thread.finished.connect(lambda data: self.on_download_finished(data, thread))
        thread.error.connect(lambda err: self.on_download_error(err, thread))
        
        self.active_threads.append(thread) # Keep alive
        thread.start()

    def on_download_finished(self, data, thread):
        self.dl_log.append(f"🎉 Successfully fetched data for {data['name']}")
        
        if thread.mode == "auto-add":
            new_p = {
                'id': self.get_next_id(),
                'name': data['name'],
                'brand': data['brand'],
                'price': 0,
                'rating': 4.5,
                'image': data['image'],
                'status': 'available',
                'specs': data['specs']
            }
            self.phones.append(new_p)
            self.write_to_js()
            self.refresh_list()
            self.dl_log.append(f"✅ Added {data['name']} to your phone list!")
        else:
            # photo-only mode
            row = self.phone_list.currentRow()
            if row >= 0:
                self.inputs['image'].setText(data['image'])
                self.save_current_phone()
        
        if thread in self.active_threads:
            self.active_threads.remove(thread)

    def on_download_error(self, err, thread):
        self.dl_log.append(err)
        if thread in self.active_threads:
            self.active_threads.remove(thread)

    # --- Logic: Tools ---
    def fix_quotes(self):
        self.write_to_js()
        QMessageBox.information(self, "Fix", "All quote marks in specs have been escaped.")

    def batch_add_phones(self):
        # Sample data from your old generator
        new_data = [
            {"name": "Samsung Galaxy S26 FE", "brand": "Samsung", "price": 145000, "specs": {"screen": "6.5\" AMOLED", "ram": "8GB", "storage": "256GB"}},
            {"name": "OnePlus 14 Pro", "brand": "OnePlus", "price": 185000, "specs": {"screen": "6.8\" LTPO", "ram": "16GB", "storage": "512GB"}},
            {"name": "Realme GT 7", "brand": "Realme", "price": 105000, "specs": {"screen": "6.78\" AMOLED", "ram": "12GB", "storage": "256GB"}},
        ]
        count = 0
        for d in new_data:
            if not any(p['name'] == d['name'] for p in self.phones):
                p = {
                    'id': self.get_next_id(),
                    'name': d['name'],
                    'brand': d['brand'],
                    'price': d['price'],
                    'rating': 4.5,
                    'image': f"Photos/{d['name'].replace(' ', '_')}.jpg",
                    'status': 'available',
                    'specs': {k: d['specs'].get(k, "TBA") for k in ['screen', 'refresh', 'ram', 'storage', 'camera', 'battery', 'processor', 'network']}
                }
                self.phones.append(p)
                count += 1
        self.write_to_js()
        self.refresh_list()
        QMessageBox.information(self, "Success", f"Added {count} new phone models!")

    def bulk_download(self):
        self.switch_tab(1)
        self.dl_log.append("🔄 Bulk download started...")
        for p in self.phones:
            if not os.path.exists(p['image']):
                self.start_download(p['name'])
                # This is a bit simplistic since it won't wait, but the threads will queue
                # For a better bulk downloader, we'd need a queue system.

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SmartPhoneManager()
    window.show()
    sys.exit(app.exec_())
