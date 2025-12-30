import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import json
import os
import re
import shutil

# File Configuration
JS_FILE_PATH = os.path.join("js", "script.js")
PHOTOS_DIR = "Photos"

class ModernButton(tk.Canvas):
    def __init__(self, parent, text, command, bg_color="#0ea5e9", hover_color="#0284c7", **kwargs):
        super().__init__(parent, height=40, highlightthickness=0, **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text = text
        
        self.configure(bg=bg_color, cursor="hand2")
        self.create_rounded_rect(0, 0, kwargs.get('width', 100), 40, radius=8, fill=bg_color)
        self.text_id = self.create_text(
            0, 0, text=text, fill="white", 
            font=("Segoe UI", 10, "bold"), anchor="center"
        )
        
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Configure>", self._on_configure)
        
    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]
        return self.create_polygon(points, smooth=True, **kwargs)
        
    def _on_configure(self, event):
        self.coords(self.text_id, event.width/2, event.height/2)
        
    def _on_click(self, event):
        if self.command:
            self.command()
            
    def _on_enter(self, event):
        self.itemconfig(1, fill=self.hover_color)
        
    def _on_leave(self, event):
        self.itemconfig(1, fill=self.bg_color)

class ImagePreviewWindow(tk.Toplevel):
    def __init__(self, parent, image_path):
        super().__init__(parent)
        self.title("Image Preview 🖼️")
        self.geometry("600x600")
        self.configure(bg="#ffffff")
        
        # Header
        header = tk.Frame(self, bg="#f8fafc", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="Product Image Preview",
            font=("Segoe UI", 16, "bold"),
            fg="#1e293b",
            bg="#f8fafc"
        ).pack(side="left", padx=20, pady=15)
        
        close_btn = tk.Button(
            header,
            text="✕",
            font=("Segoe UI", 14, "bold"),
            bg="#ef4444",
            fg="white",
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.destroy
        )
        close_btn.pack(side="right", padx=15)
        
        # Image container
        container = tk.Frame(self, bg="#ffffff")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.image_label = tk.Label(container, bg="#f1f5f9", text="Loading image...", fg="#64748b")
        self.image_label.pack(fill="both", expand=True)
        
        # Load image
        self.load_image(image_path)
        
    def load_image(self, path):
        try:
            if os.path.exists(path):
                img = Image.open(path)
                # Resize to fit
                img.thumbnail((550, 550), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.image_label.configure(image=photo, text="")
                self.image_label.image = photo
            else:
                self.image_label.configure(text=f"Image not found:\n{path}", fg="#ef4444")
        except Exception as e:
            self.image_label.configure(text=f"Error loading image:\n{str(e)}", fg="#ef4444")

class PhoneManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smartphone Manager 📱")
        self.root.geometry("1300x850")
        
        # Light theme colors
        self.colors = {
            'bg': '#f8fafc',              # Light gray background
            'sidebar': '#ffffff',         # White sidebar
            'card': '#ffffff',            # White cards
            'input_bg': '#f1f5f9',        # Light input background
            'primary': '#0ea5e9',         # Sky blue
            'primary_hover': '#0284c7',   # Darker blue
            'success': '#10b981',         # Green
            'danger': '#ef4444',          # Red
            'warning': '#f59e0b',         # Orange
            'text': '#1e293b',            # Dark text
            'text_secondary': '#64748b',  # Gray text
            'border': '#e2e8f0',          # Light border
            'hover': '#f1f5f9'            # Hover background
        }
        
        self.root.configure(bg=self.colors['bg'])

        # Data
        self.phones = []
        self.current_phone_index = None
        self.full_js_content = ""
        self.current_image_path = None

        # Create UI
        self.create_ui()
        self.load_data()

    def create_ui(self):
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill="both", expand=True)
        
        # Header bar
        self.create_header(main_container)
        
        # Content area
        content = tk.Frame(main_container, bg=self.colors['bg'])
        content.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left Sidebar (Product List)
        self.create_sidebar(content)
        
        # Middle Form Area
        self.create_form_area(content)
        
        # Right Preview Area
        self.create_preview_area(content)

    def create_header(self, parent):
        header = tk.Frame(parent, bg=self.colors['card'], height=70)
        header.pack(fill="x", padx=20, pady=(20, 10))
        header.pack_propagate(False)
        
        # Add shadow effect
        shadow = tk.Frame(parent, bg=self.colors['border'], height=1)
        shadow.place(x=20, y=89, relwidth=0.94)
        
        # Title with icon
        title_frame = tk.Frame(header, bg=self.colors['card'])
        title_frame.pack(side="left", padx=25, pady=15)
        
        tk.Label(
            title_frame, 
            text="📱", 
            font=("Segoe UI", 28),
            bg=self.colors['card']
        ).pack(side="left", padx=(0, 10))
        
        title_text = tk.Frame(title_frame, bg=self.colors['card'])
        title_text.pack(side="left")
        
        tk.Label(
            title_text, 
            text="Smartphone Manager", 
            font=("Segoe UI", 20, "bold"),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(anchor="w")
        
        tk.Label(
            title_text, 
            text="Manage your product catalog", 
            font=("Segoe UI", 9),
            fg=self.colors['text_secondary'],
            bg=self.colors['card']
        ).pack(anchor="w")
        
        # Stats area
        stats_frame = tk.Frame(header, bg=self.colors['input_bg'])
        stats_frame.pack(side="right", padx=20)
        
        tk.Label(
            stats_frame,
            text="📊",
            font=("Segoe UI", 16),
            bg=self.colors['input_bg']
        ).pack(side="left", padx=(15, 5), pady=10)
        
        stats_inner = tk.Frame(stats_frame, bg=self.colors['input_bg'])
        stats_inner.pack(side="left", padx=(0, 15), pady=10)
        
        self.stats_label = tk.Label(
            stats_inner,
            text="0 Products",
            font=("Segoe UI", 13, "bold"),
            fg=self.colors['text'],
            bg=self.colors['input_bg']
        )
        self.stats_label.pack()
        
        tk.Label(
            stats_inner,
            text="in catalog",
            font=("Segoe UI", 8),
            fg=self.colors['text_secondary'],
            bg=self.colors['input_bg']
        ).pack()

    def create_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=self.colors['sidebar'], width=320)
        sidebar.pack(side="left", fill="both", padx=(0, 10))
        sidebar.pack_propagate(False)
        
        # Add border
        border = tk.Frame(sidebar, bg=self.colors['border'], width=1)
        border.pack(side="right", fill="y")
        
        # Sidebar header
        sidebar_header = tk.Frame(sidebar, bg=self.colors['sidebar'], height=70)
        sidebar_header.pack(fill="x", padx=20, pady=(15, 10))
        sidebar_header.pack_propagate(False)
        
        tk.Label(
            sidebar_header,
            text="📋 Product List",
            font=("Segoe UI", 15, "bold"),
            fg=self.colors['text'],
            bg=self.colors['sidebar']
        ).pack(side="left", pady=10)
        
        # New button
        new_btn = ModernButton(
            sidebar_header, 
            text="+ New",
            command=self.clear_form,
            bg_color=self.colors['success'],
            hover_color="#059669",
            width=90
        )
        new_btn.pack(side="right", pady=10)
        
        # Search box
        search_frame = tk.Frame(sidebar, bg=self.colors['input_bg'], height=45)
        search_frame.pack(fill="x", padx=20, pady=(0, 15))
        search_frame.pack_propagate(False)
        
        tk.Label(
            search_frame,
            text="🔍",
            font=("Segoe UI", 14),
            bg=self.colors['input_bg'],
            fg=self.colors['text_secondary']
        ).pack(side="left", padx=(12, 5))
        
        self.search_entry = tk.Entry(
            search_frame,
            font=("Segoe UI", 11),
            bg=self.colors['input_bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['primary'],
            relief="flat",
            bd=0
        )
        self.search_entry.pack(side="left", fill="both", expand=True, padx=(0, 12))
        self.search_entry.insert(0, "Search products...")
        self.search_entry.bind("<FocusIn>", self._on_search_focus_in)
        self.search_entry.bind("<FocusOut>", self._on_search_focus_out)
        self.search_entry.bind("<KeyRelease>", self._on_search)
        
        # Listbox
        list_container = tk.Frame(sidebar, bg=self.colors['sidebar'])
        list_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.phone_listbox = tk.Listbox(
            list_container,
            bg=self.colors['sidebar'],
            fg=self.colors['text'],
            font=("Segoe UI", 11),
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=self.colors['border'],
            highlightcolor=self.colors['primary'],
            selectbackground=self.colors['primary'],
            selectforeground="white",
            activestyle="none",
            relief="flat"
        )
        self.phone_listbox.pack(side="left", fill="both", expand=True)
        self.phone_listbox.bind("<<ListboxSelect>>", self.on_select_phone)
        
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=self.phone_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.phone_listbox.config(yscrollcommand=scrollbar.set)

    def create_form_area(self, parent):
        form_container = tk.Frame(parent, bg=self.colors['card'])
        form_container.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Add border
        border = tk.Frame(form_container, bg=self.colors['border'], width=1)
        border.pack(side="right", fill="y")
        
        # Canvas for scrolling
        self.canvas = tk.Canvas(form_container, bg=self.colors['card'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_container, orient="vertical", command=self.canvas.yview)
        
        self.form_inner = tk.Frame(self.canvas, bg=self.colors['card'])
        
        self.form_inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.form_inner, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Enable mousewheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Form content
        self.create_form_content()

    def create_preview_area(self, parent):
        preview_container = tk.Frame(parent, bg=self.colors['card'], width=300)
        preview_container.pack(side="right", fill="both")
        preview_container.pack_propagate(False)
        
        # Header
        header = tk.Frame(preview_container, bg=self.colors['card'], height=70)
        header.pack(fill="x", padx=20, pady=(15, 10))
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🖼️ Image Preview",
            font=("Segoe UI", 15, "bold"),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(anchor="w", pady=10)
        
        # Image display area
        image_frame = tk.Frame(preview_container, bg=self.colors['input_bg'], relief="flat", bd=0)
        image_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        self.preview_label = tk.Label(
            image_frame, 
            text="No image selected\n\n📷\n\nSelect a product to see its image",
            font=("Segoe UI", 11),
            fg=self.colors['text_secondary'],
            bg=self.colors['input_bg'],
            justify="center"
        )
        self.preview_label.pack(fill="both", expand=True, padx=2, pady=2)
        
        # View full size button
        self.view_btn = ModernButton(
            preview_container,
            text="🔍 View Full Size",
            command=self.view_full_image,
            bg_color=self.colors['primary'],
            hover_color=self.colors['primary_hover'],
            width=260
        )
        self.view_btn.pack(padx=20, pady=(0, 20))

    def create_form_content(self):
        # Header
        header = tk.Frame(self.form_inner, bg=self.colors['card'])
        header.pack(fill="x", padx=25, pady=(20, 25))
        
        tk.Label(
            header,
            text="✏️ Product Details",
            font=("Segoe UI", 18, "bold"),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(anchor="w")
        
        tk.Label(
            header,
            text="Fill in the information below to add or edit a product",
            font=("Segoe UI", 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['card']
        ).pack(anchor="w", pady=(5, 0))
        
        self.entries = {}
        
        # General Info
        self.create_section("General Information", "ℹ️")
        self.create_modern_entry("Product Name *", "name", "e.g., iPhone 15 Pro")
        self.create_modern_entry("Brand *", "brand", "e.g., Apple")
        self.create_modern_entry("Price (DZD) *", "price", "e.g., 150000")
        self.create_image_picker()
        self.create_modern_entry("Rating (1-5) *", "rating", "e.g., 4.5")
        
        # Specifications
        self.create_section("Technical Specifications", "⚙️")
        specs_grid = tk.Frame(self.form_inner, bg=self.colors['card'])
        specs_grid.pack(fill="x", padx=25, pady=(0, 10))
        
        left_col = tk.Frame(specs_grid, bg=self.colors['card'])
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        right_col = tk.Frame(specs_grid, bg=self.colors['card'])
        right_col.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        self.create_compact_entry(left_col, "Screen", "screen", "6.7\" AMOLED")
        self.create_compact_entry(right_col, "Refresh Rate", "refresh", "120Hz")
        self.create_compact_entry(left_col, "RAM", "ram", "8GB")
        self.create_compact_entry(right_col, "Storage", "storage", "256GB")
        self.create_compact_entry(left_col, "Camera", "camera", "48MP Triple")
        self.create_compact_entry(right_col, "Battery", "battery", "5000mAh")
        
        self.create_modern_entry("Processor", "processor", "e.g., Snapdragon 8 Gen 2")
        self.create_modern_entry("Network", "network", "e.g., 5G")
        
        # Additional
        self.create_section("Additional Information", "🏷️")
        self.create_modern_entry("Special Tag", "tag", "e.g., Flagship, Budget, Gaming")
        
        # Action buttons
        self.create_action_buttons()

    def create_section(self, title, icon=""):
        section = tk.Frame(self.form_inner, bg=self.colors['card'])
        section.pack(fill="x", padx=25, pady=(25, 15))
        
        title_frame = tk.Frame(section, bg=self.colors['card'])
        title_frame.pack(fill="x")
        
        tk.Label(
            title_frame,
            text=f"{icon}  {title}",
            font=("Segoe UI", 13, "bold"),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(side="left")
        
        separator = tk.Frame(section, bg=self.colors['border'], height=2)
        separator.pack(fill="x", pady=(8, 0))

    def create_modern_entry(self, label, key, placeholder=""):
        container = tk.Frame(self.form_inner, bg=self.colors['card'])
        container.pack(fill="x", padx=25, pady=7)
        
        tk.Label(
            container,
            text=label,
            font=("Segoe UI", 10, "bold"),
            fg=self.colors['text'],
            bg=self.colors['card'],
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        entry_frame = tk.Frame(container, bg=self.colors['input_bg'], height=42)
        entry_frame.pack(fill="x")
        entry_frame.pack_propagate(False)
        
        entry = tk.Entry(
            entry_frame,
            font=("Segoe UI", 11),
            bg=self.colors['input_bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['primary'],
            relief="flat",
            bd=0
        )
        entry.pack(fill="both", expand=True, padx=12, pady=8)
        
        if placeholder:
            entry.insert(0, placeholder)
            entry.config(fg=self.colors['text_secondary'])
            entry.bind("<FocusIn>", lambda e: self._clear_placeholder(e, placeholder))
            entry.bind("<FocusOut>", lambda e: self._restore_placeholder(e, placeholder))
        
        self.entries[key] = entry

    def create_compact_entry(self, parent, label, key, placeholder=""):
        container = tk.Frame(parent, bg=self.colors['card'])
        container.pack(fill="x", pady=7)
        
        tk.Label(
            container,
            text=label,
            font=("Segoe UI", 10, "bold"),
            fg=self.colors['text'],
            bg=self.colors['card'],
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        entry_frame = tk.Frame(container, bg=self.colors['input_bg'], height=42)
        entry_frame.pack(fill="x")
        entry_frame.pack_propagate(False)
        
        entry = tk.Entry(
            entry_frame,
            font=("Segoe UI", 11),
            bg=self.colors['input_bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['primary'],
            relief="flat",
            bd=0
        )
        entry.pack(fill="both", expand=True, padx=12, pady=8)
        
        if placeholder:
            entry.insert(0, placeholder)
            entry.config(fg=self.colors['text_secondary'])
            entry.bind("<FocusIn>", lambda e: self._clear_placeholder(e, placeholder))
            entry.bind("<FocusOut>", lambda e: self._restore_placeholder(e, placeholder))
        
        self.entries[key] = entry

    def create_image_picker(self):
        container = tk.Frame(self.form_inner, bg=self.colors['card'])
        container.pack(fill="x", padx=25, pady=7)
        
        tk.Label(
            container,
            text="Product Image *",
            font=("Segoe UI", 10, "bold"),
            fg=self.colors['text'],
            bg=self.colors['card'],
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        entry_frame = tk.Frame(container, bg=self.colors['input_bg'])
        entry_frame.pack(fill="x")
        
        entry = tk.Entry(
            entry_frame,
            font=("Segoe UI", 11),
            bg=self.colors['input_bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['primary'],
            relief="flat",
            bd=0
        )
        entry.pack(side="left", fill="both", expand=True, padx=12, pady=8)
        entry.bind("<KeyRelease>", self._on_image_change)
        self.entries["image"] = entry
        
        browse_btn = ModernButton(
            entry_frame,
            text="📁 Browse",
            command=self.browse_image,
            bg_color=self.colors['warning'],
            hover_color="#d97706",
            width=110
        )
        browse_btn.pack(side="right", padx=8, pady=4)

    def create_action_buttons(self):
        btn_container = tk.Frame(self.form_inner, bg=self.colors['card'])
        btn_container.pack(fill="x", padx=25, pady=(30, 25))
        
        save_btn = ModernButton(
            btn_container,
            text="💾 Save Changes",
            command=self.save_phone,
            bg_color=self.colors['primary'],
            hover_color=self.colors['primary_hover'],
            width=160
        )
        save_btn.pack(side="right", padx=5)
        
        delete_btn = ModernButton(
            btn_container,
            text="🗑️ Delete Product",
            command=self.delete_phone,
            bg_color=self.colors['danger'],
            hover_color="#b91c1c",
            width=160
        )
        delete_btn.pack(side="right", padx=5)

    # Event handlers
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _clear_placeholder(self, event, placeholder):
        widget = event.widget
        if widget.get() == placeholder:
            widget.delete(0, tk.END)
            widget.config(fg=self.colors['text'])

    def _restore_placeholder(self, event, placeholder):
        widget = event.widget
        if not widget.get():
            widget.insert(0, placeholder)
            widget.config(fg=self.colors['text_secondary'])

    def _on_search_focus_in(self, event):
        if self.search_entry.get() == "Search products...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg=self.colors['text'])

    def _on_search_focus_out(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search products...")
            self.search_entry.config(fg=self.colors['text_secondary'])

    def _on_search(self, event):
        search_term = self.search_entry.get().lower()
        if search_term == "search products...":
            self.refresh_list()
            return
        
        self.phone_listbox.delete(0, tk.END)
        for p in self.phones:
            name = p.get('name', '').lower()
            brand = p.get('brand', '').lower()
            if search_term in name or search_term in brand:
                self.phone_listbox.insert(tk.END, f"{p['name']} - {p['brand']}")

    def _on_image_change(self, event):
        self.update_preview()

    def browse_image(self):
        filename = filedialog.askopenfilename(
            initialdir=PHOTOS_DIR if os.path.exists(PHOTOS_DIR) else ".",
            title="Select Phone Image",
            filetypes=(("Image files", "*.jpg *.jpeg *.png *.webp"), ("All files", "*.*"))
        )
        if filename:
            try:
                rel_path = os.path.relpath(filename, os.getcwd())
                if not rel_path.startswith(".."):
                    self.entries["image"].delete(0, tk.END)
                    self.entries["image"].insert(0, rel_path.replace("\\", "/"))
                    self.entries["image"].config(fg=self.colors['text'])
                else:
                    if os.path.exists(PHOTOS_DIR):
                        basename = os.path.basename(filename)
                        dest = os.path.join(PHOTOS_DIR, basename)
                        shutil.copy(filename, dest)
                        self.entries["image"].delete(0, tk.END)
                        self.entries["image"].insert(0, f"{PHOTOS_DIR}/{basename}")
                        self.entries["image"].config(fg=self.colors['text'])
                    else:
                        self.entries["image"].delete(0, tk.END)
                        self.entries["image"].insert(0, filename)
                        self.entries["image"].config(fg=self.colors['text'])
                self.update_preview()
            except Exception as e:
                print(e)
                self.entries["image"].delete(0, tk.END)
                self.entries["image"].insert(0, filename)
                self.entries["image"].config(fg=self.colors['text'])

    def update_preview(self):
        image_path = self.entries["image"].get()
        
        if not image_path or image_path.startswith("e.g.,"):
            self.preview_label.configure(
                image="",
                text="No image selected\n\n📷\n\nSelect a product to see its image"
            )
            self.current_image_path = None
            return
        
        try:
            if os.path.exists(image_path):
                self.current_image_path = image_path
                img = Image.open(image_path)
                img.thumbnail((260, 260), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.preview_label.configure(image=photo, text="")
                self.preview_label.image = photo
            else:
                self.preview_label.configure(
                    image="",
                    text=f"❌ Image not found\n\n{os.path.basename(image_path)}"
                )
                self.current_image_path = None
        except Exception as e:
            self.preview_label.configure(
                image="",
                text=f"⚠️ Error loading image\n\n{str(e)}"
            )
            self.current_image_path = None

    def view_full_image(self):
        if self.current_image_path and os.path.exists(self.current_image_path):
            ImagePreviewWindow(self.root, self.current_image_path)
        else:
            messagebox.showwarning("No Image", "Please select a valid image first!")

    # Data handling
    def parse_js_array(self, content):
        match = re.search(r'const products = \[\s*([\s\S]*?)\];', content)
        if not match:
            return []

        inner_content = match.group(1)
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
                    objects.append(self.parse_single_js_object(current_obj_str))
                    current_obj_str = ""
            elif depth > 0:
                current_obj_str += char
        
        return objects

    def parse_single_js_object(self, obj_str):
        data = {}
        
        m_id = re.search(r'id:\s*(\d+)', obj_str)
        if m_id: data['id'] = int(m_id.group(1))
        
        m_name = re.search(r'name:\s*"(.*?)"', obj_str)
        if m_name: data['name'] = m_name.group(1)

        m_brand = re.search(r'brand:\s*"(.*?)"', obj_str)
        if m_brand: data['brand'] = m_brand.group(1)
        
        m_price = re.search(r'price:\s*(\d+)', obj_str)
        if m_price: data['price'] = int(m_price.group(1))
        
        m_img = re.search(r'image:\s*"(.*?)"', obj_str)
        if m_img: data['image'] = m_img.group(1)
        
        m_rate = re.search(r'rating:\s*([\d\.]+)', obj_str)
        if m_rate: data['rating'] = float(m_rate.group(1))

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
        self.update_stats()

    def refresh_list(self):
        self.phone_listbox.delete(0, tk.END)
        for p in self.phones:
            if 'name' in p and 'brand' in p:
                self.phone_listbox.insert(tk.END, f"{p['name']} - {p['brand']}")
        self.update_stats()

    def update_stats(self):
        count = len(self.phones)
        self.stats_label.config(text=f"{count} Product{'s' if count != 1 else ''}")

    def on_select_phone(self, event):
        sel = self.phone_listbox.curselection()
        if not sel: return
        self.current_phone_index = sel[0]
        self.populate_form(self.phones[self.current_phone_index])

    def populate_form(self, p):
        for e in self.entries.values(): 
            e.delete(0, tk.END)
            e.config(fg=self.colors['text'])
        
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
        
        self.update_preview()

    def clear_form(self):
        self.current_phone_index = None
        self.phone_listbox.selection_clear(0, tk.END)
        for e in self.entries.values():
            e.delete(0, tk.END)
            e.config(fg=self.colors['text'])
        self.preview_label.configure(
            image="",
            text="No image selected\n\n📷\n\nSelect a product to see its image"
        )
        self.current_image_path = None

    def save_phone(self):
        name = self.entries['name'].get()
        if not name or name.startswith("e.g.,"):
            messagebox.showwarning("Validation", "Product name is required!")
            return

        try:
            price_val = self.entries['price'].get()
            rating_val = self.entries['rating'].get()
            
            if price_val.startswith("e.g.,") or rating_val.startswith("e.g.,"):
                messagebox.showwarning("Validation", "Please fill in all required fields!")
                return
            
            p = {
                'id': self.phones[self.current_phone_index]['id'] if self.current_phone_index is not None else self.get_new_id(),
                'name': name,
                'brand': self.entries['brand'].get(),
                'price': int(price_val),
                'image': self.entries['image'].get(),
                'rating': float(rating_val),
                'specs': {}
            }
            
            for k in ['screen', 'refresh', 'ram', 'storage', 'camera', 'battery', 'processor', 'network']:
                val = self.entries[k].get()
                if val and not val.startswith("e.g.,") and not val.startswith("6.7"):
                    p['specs'][k] = val
            
            tag_val = self.entries['tag'].get()
            if tag_val and not tag_val.startswith("e.g.,"):
                p['tags'] = [tag_val]

            if self.current_phone_index is not None:
                self.phones[self.current_phone_index] = p
            else:
                self.phones.append(p)
            
            self.write_file()
            self.refresh_list()
            messagebox.showinfo("Success", "Product saved successfully! ✅")
        except ValueError:
            messagebox.showerror("Error", "Price and Rating must be valid numbers!")

    def delete_phone(self):
        if self.current_phone_index is None: 
            messagebox.showwarning("Warning", "Please select a product first!")
            return
        if messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this product?\n\nThis action cannot be undone."):
            del self.phones[self.current_phone_index]
            self.write_file()
            self.refresh_list()
            self.clear_form()
            messagebox.showinfo("Deleted", "Product deleted successfully!")

    def get_new_id(self):
        if not self.phones: return 1
        return max(x.get('id', 0) for x in self.phones) + 1

    def write_file(self):
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

    