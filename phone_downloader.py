import sys
import os
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QTextEdit, 
                             QLabel, QFileDialog, QProgressBar, QComboBox)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon
from bs4 import BeautifulSoup
import json

class DownloadThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, phone_name, save_path, image_count):
        super().__init__()
        self.phone_name = phone_name
        self.save_path = save_path
        self.image_count = image_count
        
    def run(self):
        try:
            self.progress.emit(f"🔍 Searching for: {self.phone_name}...")
            
            # Search for phone on GSMArena
            search_url = "https://www.gsmarena.com/results.php3"
            params = {"sQuickSearch": "yes", "sName": self.phone_name}
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, params=params, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find first phone link
            phone_link = soup.select_one('.makers a')
            if not phone_link:
                self.error.emit("❌ Phone not found")
                return
                
            phone_url = "https://www.gsmarena.com/" + phone_link['href']
            self.progress.emit(f"✅ Phone found: {phone_link.text.strip()}")
            
            # Get phone page
            response = requests.get(phone_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find images
            images = []
            
            # Main image
            main_img = soup.select_one('.specs-photo-main img')
            if main_img and main_img.get('src'):
                images.append(main_img['src'])
            
            # Additional images
            thumb_images = soup.select('.specs-photo-item img')
            for img in thumb_images[:self.image_count-1]:
                if img.get('src'):
                    img_url = img['src'].replace('-thumb', '')
                    images.append(img_url)
            
            if not images:
                self.error.emit("❌ No images found")
                return
            
            # Create folder for phone
            phone_folder = os.path.join(self.save_path, self.phone_name.replace(" ", "_"))
            os.makedirs(phone_folder, exist_ok=True)
            
            # Download images
            self.progress.emit(f"📥 Downloading {len(images)} images...")
            
            for idx, img_url in enumerate(images, 1):
                try:
                    if not img_url.startswith('http'):
                        img_url = 'https://www.gsmarena.com/' + img_url
                    
                    img_response = requests.get(img_url, headers=headers, timeout=10)
                    img_response.raise_for_status()
                    
                    ext = img_url.split('.')[-1].split('?')[0]
                    if ext not in ['jpg', 'jpeg', 'png', 'webp']:
                        ext = 'jpg'
                    
                    filename = f"{self.phone_name.replace(' ', '_')}_{idx}.{ext}"
                    filepath = os.path.join(phone_folder, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(img_response.content)
                    
                    self.progress.emit(f"✅ Downloaded image {idx}/{len(images)}")
                    
                except Exception as e:
                    self.progress.emit(f"⚠️ Failed to download image {idx}: {str(e)}")
            
            self.progress.emit(f"✅ Download complete! Images saved in: {phone_folder}")
            self.finished.emit()
            
        except Exception as e:
            self.error.emit(f"❌ Error: {str(e)}")


class PhoneImageDownloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.download_thread = None
        
    def init_ui(self):
        self.setWindowTitle("📱 Phone Images Downloader")
        self.setGeometry(100, 100, 700, 600)
        
        # Light Theme Stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f7;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #d1d1d6;
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #007aff;
            }
            QPushButton {
                background-color: #007aff;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0062cc;
            }
            QPushButton:disabled {
                background-color: #b0b0b0;
                color: #f0f0f0;
            }
            QTextEdit {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #d1d1d6;
                border-radius: 6px;
                padding: 8px;
                font-family: 'Courier New';
                font-size: 12px;
            }
            QComboBox {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #d1d1d6;
                border-radius: 6px;
                padding: 8px;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Title
        title = QLabel("📱 Phone Images Downloader")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1c1c1e; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Phone name input
        layout.addWidget(QLabel("🔍 Phone Name:"))
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("e.g. Samsung Galaxy S24 Ultra")
        layout.addWidget(self.phone_input)
        
        # Image count selector
        layout.addWidget(QLabel("📸 Number of Images:"))
        self.image_count_combo = QComboBox()
        self.image_count_combo.addItems(["1", "2", "3", "5", "10", "15"])
        self.image_count_combo.setCurrentText("5")
        layout.addWidget(self.image_count_combo)
        
        # Save path
        path_layout = QHBoxLayout()
        layout.addWidget(QLabel("📁 Save Path:"))
        self.path_input = QLineEdit()
        self.path_input.setText(os.getcwd())
        self.path_input.setReadOnly(True)
        path_layout.addWidget(self.path_input)
        
        self.browse_btn = QPushButton("📂 Browse")
        self.browse_btn.clicked.connect(self.browse_folder)
        self.browse_btn.setMaximumWidth(100)
        self.browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #e5e5ea;
                color: #333333;
            }
            QPushButton:hover {
                background-color: #d1d1d6;
            }
        """)
        path_layout.addWidget(self.browse_btn)
        layout.addLayout(path_layout)
        
        # Download button
        self.download_btn = QPushButton("⬇️ Download Images")
        self.download_btn.clicked.connect(self.start_download)
        self.download_btn.setMinimumHeight(45)
        self.download_btn.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.download_btn)
        
        # Log area
        layout.addWidget(QLabel("📋 Logs:"))
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)
        
        # Info label
        info = QLabel("💡 This tool uses GSMArena to fetch high-quality phone images.")
        info.setStyleSheet("color: #8e8e93; font-size: 11px;")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)
        
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Save Folder")
        if folder:
            self.path_input.setText(folder)
    
    def log(self, message):
        self.log_text.append(message)
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
    
    def start_download(self):
        phone_name = self.phone_input.text().strip()
        save_path = self.path_input.text()
        
        if not phone_name:
            self.log("❌ Please enter a phone name")
            return
        
        if not os.path.exists(save_path):
            self.log("❌ Save path does not exist")
            return
        
        image_count = int(self.image_count_combo.currentText())
        
        self.download_btn.setEnabled(False)
        self.log(f"\n{'='*50}")
        self.log(f"🚀 Starting download: {phone_name}")
        
        self.download_thread = DownloadThread(phone_name, save_path, image_count)
        self.download_thread.progress.connect(self.log)
        self.download_thread.error.connect(self.on_error)
        self.download_thread.finished.connect(self.on_finished)
        self.download_thread.start()
    
    def on_error(self, message):
        self.log(message)
        self.download_btn.setEnabled(True)
    
    def on_finished(self):
        self.download_btn.setEnabled(True)
        self.log("🎉 Download finished successfully!")


def main():
    app = QApplication(sys.argv)
    
    # Set app font to something clean
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = PhoneImageDownloader()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()