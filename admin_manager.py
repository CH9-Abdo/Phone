import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import re
import shutil

# File Configuration
JS_FILE_PATH = os.path.join("js", "script.js")
PHOTOS_DIR = "Photos"

class PhoneManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smartphone Manager 📱")
        self.root.geometry("1100x750")
        self.root.configure(bg="#f8fafc")

        # Data
        self.phones = []
        self.current_phone_index = None
        self.full_js_content = ""

        # Styles
        self.setup_styles()

        # Layout
        self.main_pane = ttk.PanedWindow(root, orient="horizontal")
        self.main_pane.pack(fill="both", expand=True, padx=15, pady=15)

        # Left Sidebar (List)
        self.sidebar_frame = ttk.Frame(self.main_pane, style="Card.TFrame")
        self.main_pane.add(self.sidebar_frame, weight=1)
        self.setup_sidebar()

        # Right Content (Form)
        self.content_frame = ttk.Frame(self.main_pane, style="Card.TFrame")
        self.main_pane.add(self.content_frame, weight=3)
        self.setup_form()

        # Load Data
        self.load_data()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colors
        bg_color = "#f8fafc"
        card_bg = "#ffffff"
        primary_color = "#0ea5e9"  # Sky Blue
        text_color = "#334155"

        style.configure("TFrame", background=bg_color)
        style.configure("Card.TFrame", background=card_bg)
        
        style.configure("TLabel", background=card_bg, foreground=text_color, font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#0f172a")
        style.configure("SubHeader.TLabel", font=("Segoe UI", 11, "bold"), foreground="#64748b")
        
        style.configure("TButton", font=("Segoe UI", 9, "bold"), padding=8, borderwidth=0)
        style.map("TButton", background=[("active", "#e2e8f0")])
        
        style.configure("Primary.TButton", background=primary_color, foreground="white")
        style.map("Primary.TButton", background=[("active", "#0284c7")])

        style.configure("Delete.TButton", background="#ef4444", foreground="white")
        style.map("Delete.TButton", background=[("active", "#b91c1c")])

    def setup_sidebar(self):
        # Header
        header = ttk.Frame(self.sidebar_frame, padding=15)
        header.pack(fill="x")
        ttk.Label(header, text="Product List", style="SubHeader.TLabel").pack(side="left")
        ttk.Button(header, text="+ New Phone", style="Primary.TButton", command=self.clear_form).pack(side="right")

        # Listbox
        list_container = ttk.Frame(self.sidebar_frame, padding=(15, 0, 15, 15))
        list_container.pack(fill="both", expand=True)

        self.phone_listbox = tk.Listbox(
            list_container,
            bg="#f1f5f9",
            fg="#334155",
            font=("Segoe UI", 11),
            borderwidth=0,
            highlightthickness=0,
            selectbackground="#e0f2fe",
            selectforeground="#0284c7",
            activestyle="none"
        )
        self.phone_listbox.pack(side="left", fill="both", expand=True)
        self.phone_listbox.bind("<<ListboxSelect>>", self.on_select_phone)

        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=self.phone_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.phone_listbox.config(yscrollcommand=scrollbar.set)

    def setup_form(self):
        # Scrollable Form
        self.canvas = tk.Canvas(self.content_frame, bg="white", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.canvas.yview)
        self.form_inner = ttk.Frame(self.canvas, style="Card.TFrame", padding=30)

        self.form_inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.form_inner, anchor="nw", width=700)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Fields
        ttk.Label(self.form_inner, text="Edit Phone Details", style="Header.TLabel").pack(anchor="w", pady=(0, 25))

        self.entries = {}
        
        self.create_section("General Info")
        self.create_entry("Phone Name", "name")
        self.create_entry("Brand", "brand")
        self.create_entry("Price (DZD)", "price")
        
        # Image Picker
        self.create_image_picker()
        
        self.create_entry("Rating (1-5)", "rating")

        self.create_section("Specifications")
        self.create_entry("Screen", "screen")
        self.create_entry("Refresh Rate", "refresh")
        self.create_entry("RAM", "ram")
        self.create_entry("Storage", "storage")
        self.create_entry("Camera", "camera")
        self.create_entry("Battery", "battery")
        self.create_entry("Processor", "processor")
        self.create_entry("Network", "network")
        
        self.create_entry("Special Tag", "tag")

        # Buttons
        btn_frame = ttk.Frame(self.form_inner, padding=(0, 30))
        btn_frame.pack(fill="x")
        ttk.Button(btn_frame, text="Save Changes", style="Primary.TButton", command=self.save_phone).pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Delete Phone", style="Delete.TButton", command=self.delete_phone).pack(side="right", padx=5)

    def create_section(self, title):
        ttk.Label(self.form_inner, text=title, style="SubHeader.TLabel").pack(anchor="w", pady=(20, 10))
        ttk.Separator(self.form_inner, orient="horizontal").pack(fill="x", pady=(0, 10))

    def create_entry(self, label, key):
        frame = ttk.Frame(self.form_inner)
        frame.pack(fill="x", pady=6)
        ttk.Label(frame, text=label, width=15, anchor="w").pack(side="left")
        entry = ttk.Entry(frame, font=("Segoe UI", 10))
        entry.pack(side="left", fill="x", expand=True)
        self.entries[key] = entry

    def create_image_picker(self):
        frame = ttk.Frame(self.form_inner)
        frame.pack(fill="x", pady=6)
        ttk.Label(frame, text="Image", width=15, anchor="w").pack(side="left")
        
        entry = ttk.Entry(frame, font=("Segoe UI", 10))
        entry.pack(side="left", fill="x", expand=True)
        self.entries["image"] = entry
        
        ttk.Button(frame, text="Browse", command=self.browse_image).pack(side="left", padx=(5, 0))

    def browse_image(self):
        filename = filedialog.askopenfilename(
            initialdir=PHOTOS_DIR if os.path.exists(PHOTOS_DIR) else ".",
            title="Select Phone Image",
            filetypes=(("Image files", "*.jpg *.jpeg *.png *.webp"), ("All files", "*.*"))
        )
        if filename:
            # Calculate relative path
            try:
                # If file is inside project, make it relative
                rel_path = os.path.relpath(filename, os.getcwd())
                if not rel_path.startswith(".."):
                     # It's inside the project
                     self.entries["image"].delete(0, tk.END)
                     self.entries["image"].insert(0, rel_path.replace("\\", "/"))
                else:
                    # It's outside, maybe we should copy it? For now, just absolute or ask user
                    # Let's auto-copy to Photos folder if it exists
                    if os.path.exists(PHOTOS_DIR):
                        basename = os.path.basename(filename)
                        dest = os.path.join(PHOTOS_DIR, basename)
                        shutil.copy(filename, dest)
                        self.entries["image"].delete(0, tk.END)
                        self.entries["image"].insert(0, f"{PHOTOS_DIR}/{basename}")
                    else:
                        self.entries["image"].delete(0, tk.END)
                        self.entries["image"].insert(0, filename)
            except Exception as e:
                print(e)
                self.entries["image"].delete(0, tk.END)
                self.entries["image"].insert(0, filename)

    # --- Logic ---

    def parse_js_array(self, content):
        # Improved Regex: Matches content between 'const products = [' and '];' ignoring newlines
        match = re.search(r'const products = \[\s*([\s\S]*?)\];', content)
        if not match:
            print("Regex did not match 'const products = [...]'")
            return []

        inner_content = match.group(1)
        
        # Basic parsing state machine to handle JS object syntax
        # Because `json.loads` fails on unquoted keys (e.g. id: 1)
        # We will iterate through objects separated by commas that are at root level (depth 0)
        
        objects = []
        depth = 0
        current_obj_str = ""
        
        for char in inner_content:
            if char == '{':
                depth += 1
                current_obj_str += char
            elif char == '}':
                depth -= 1
                current_obj_str += char
                if depth == 0:
                    # End of an object
                    objects.append(self.parse_single_js_object(current_obj_str))
                    current_obj_str = ""
            elif depth > 0:
                current_obj_str += char
            # Ignore characters outside of {}
            
        return objects

    def parse_single_js_object(self, obj_str):
        # Helper to extract key-values from a JS object string like { id: 1, name: "..." }
        data = {}
        
        # Simple extraction for known keys
        # id
        m_id = re.search(r'id:\s*(\d+)', obj_str)
        if m_id: data['id'] = int(m_id.group(1))
        
        # name
        m_name = re.search(r'name:\s*"(.*?)"', obj_str)
        if m_name: data['name'] = m_name.group(1)

        # brand
        m_brand = re.search(r'brand:\s*"(.*?)"', obj_str)
        if m_brand: data['brand'] = m_brand.group(1)
        
        # price
        m_price = re.search(r'price:\s*(\d+)', obj_str)
        if m_price: data['price'] = int(m_price.group(1))
        
        # image
        m_img = re.search(r'image:\s*"(.*?)"', obj_str)
        if m_img: data['image'] = m_img.group(1)
        
        # rating
        m_rate = re.search(r'rating:\s*([\d\.]+)', obj_str)
        if m_rate: data['rating'] = float(m_rate.group(1))

        # specs
        data['specs'] = {}
        specs_block_match = re.search(r'specs:\s*\{([\s\S]*?)\}', obj_str)
        if specs_block_match:
            specs_block = specs_block_match.group(1)
            for line in specs_block.split(','):
                line = line.strip()
                if ':' in line:
                    k, v = line.split(':', 1)
                    k = k.strip()
                    v = v.strip().strip('"')
                    data['specs'][k] = v

        # tags
        m_tags = re.search(r'tags:\s*\[(.*?)\]', obj_str)
        if m_tags:
            tags_str = m_tags.group(1)
            tags = [t.strip().strip('"') for t in tags_str.split(',') if t.strip()]
            data['tags'] = tags

        return data

    def load_data(self):
        if not os.path.exists(JS_FILE_PATH):
            messagebox.showerror("Error", "js/script.js not found!")
            return

        with open(JS_FILE_PATH, 'r', encoding='utf-8') as f:
            self.full_js_content = f.read()
        
        self.phones = self.parse_js_array(self.full_js_content)
        self.refresh_list()

    def refresh_list(self):
        self.phone_listbox.delete(0, tk.END)
        for p in self.phones:
            if 'name' in p:
                self.phone_listbox.insert(tk.END, f"{p['name']}")

    def on_select_phone(self, event):
        sel = self.phone_listbox.curselection()
        if not sel: return
        self.current_phone_index = sel[0]
        self.populate_form(self.phones[self.current_phone_index])

    def populate_form(self, p):
        for e in self.entries.values(): e.delete(0, tk.END)
        
        self.entries['name'].insert(0, p.get('name', ''))
        self.entries['brand'].insert(0, p.get('brand', ''))
        self.entries['price'].insert(0, p.get('price', ''))
        self.entries['image'].insert(0, p.get('image', ''))
        self.entries['rating'].insert(0, p.get('rating', ''))
        
        s = p.get('specs', {})
        for k in ['screen', 'refresh', 'ram', 'storage', 'camera', 'battery', 'processor', 'network']:
            self.entries[k].insert(0, s.get(k, ''))
            
        if p.get('tags'):
            self.entries['tag'].insert(0, p['tags'][0])

    def clear_form(self):
        self.current_phone_index = None
        self.phone_listbox.selection_clear(0, tk.END)
        for e in self.entries.values(): e.delete(0, tk.END)
        self.entries['name'].focus()

    def save_phone(self):
        if not self.entries['name'].get():
            messagebox.showwarning("Validation", "Name is required!")
            return

        try:
            p = {
                'id': self.phones[self.current_phone_index]['id'] if self.current_phone_index is not None else self.get_new_id(),
                'name': self.entries['name'].get(),
                'brand': self.entries['brand'].get(),
                'price': int(self.entries['price'].get()),
                'image': self.entries['image'].get(),
                'rating': float(self.entries['rating'].get()),
                'specs': {k: self.entries[k].get() for k in ['screen', 'refresh', 'ram', 'storage', 'camera', 'battery', 'processor', 'network']}
            }
            if self.entries['tag'].get():
                p['tags'] = [self.entries['tag'].get()]

            if self.current_phone_index is not None:
                self.phones[self.current_phone_index] = p
            else:
                self.phones.append(p)
            
            self.write_file()
            self.refresh_list()
            messagebox.showinfo("Success", "Saved successfully!")
        except ValueError:
            messagebox.showerror("Error", "Price and Rating must be numbers!")

    def delete_phone(self):
        if self.current_phone_index is None: return
        if messagebox.askyesno("Delete", "Are you sure?"):
            del self.phones[self.current_phone_index]
            self.write_file()
            self.refresh_list()
            self.clear_form()

    def get_new_id(self):
        if not self.phones: return 1
        return max(x.get('id', 0) for x in self.phones) + 1

    def write_file(self):
        # Generate clean JS array string
        js_parts = ["[\n"]
        for p in self.phones:
            js_parts.append("    {\n")
            js_parts.append(f'        id: {p["id"]},\n')
            js_parts.append(f'        name: "{p["name"]}",\n')
            js_parts.append(f'        brand: "{p["brand"]}",\n')
            js_parts.append(f'        price: {p["price"]},\n')
            js_parts.append(f'        image: "{p["image"]}",\n')
            js_parts.append(f'        rating: {p["rating"]},\n')
            js_parts.append('        specs: {\n')
            for k, v in p['specs'].items():
                js_parts.append(f'            {k}: "{v}",\n')
            js_parts.append('        },\n')
            if 'tags' in p:
                js_parts.append(f'        tags: {json.dumps(p["tags"])},\n')
            js_parts.append("    },\n")
        js_parts.append("];")
        
        new_array_str = "".join(js_parts)
        
        # Replace in file content
        new_content = re.sub(
            r'const products = \[\s*([\s\S]*?)\];', 
            f'const products = {new_array_str}', 
            self.full_js_content
        )
        
        with open(JS_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        self.full_js_content = new_content

if __name__ == "__main__":
    if not os.path.exists(JS_FILE_PATH):
        print(f"File not found: {JS_FILE_PATH}")
    else:
        root = tk.Tk()
        app = PhoneManagerApp(root)
        root.mainloop()
