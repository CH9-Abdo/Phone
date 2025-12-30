import sys
import requests
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QLabel, QFileDialog, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class PhoneImageDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('مُحمل صور الهواتف الذكي')
        self.setGeometry(300, 300, 500, 400)

        # العناصر
        self.label = QLabel('أدخل اسم الهاتف (مثلاً: iPhone 15):', self)
        self.search_input = QLineEdit(self)
        self.search_btn = QPushButton('بحث وتحميل الصورة', self)
        self.img_display = QLabel('سيتم عرض المعاينة هنا', self)
        self.img_display.setAlignment(Qt.AlignCenter)
        self.img_display.setStyleSheet("border: 1px solid gray; min-height: 250px;")

        # التصميم Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_btn)
        layout.addWidget(self.img_display)

        self.setLayout(layout)

        # الأحداث
        self.search_btn.clicked.connect(self.fetch_and_download)

    def fetch_and_download(self):
        query = self.search_input.text()
        if not query:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال اسم هاتف!")
            return

        self.search_btn.setText("جاري البحث...")
        self.search_btn.setEnabled(False)
        
        try:
            # استخدام API مجاني للبحث
            search_url = f"https://phone-specs-api.vercel.app/search?query={query}"
            response = requests.get(search_url).json()

            if response['status'] and response['data']['phones']:
                # نأخذ أول نتيجة
                phone_data = response['data']['phones'][0]
                image_url = phone_data['image']
                phone_name = phone_data['phone_name']

                # تحميل الصورة للمعاينة
                img_data = requests.get(image_url).content
                pixmap = QPixmap()
                pixmap.loadFromData(img_data)
                self.img_display.setPixmap(pixmap.scaled(200, 250, Qt.KeepAspectRatio))

                # حفظ الصورة تلقائياً
                file_name = f"{phone_name.replace(' ', '_')}.png"
                with open(file_name, 'wb') as f:
                    f.write(img_data)
                
                QMessageBox.information(self, "نجاح", f"تم حفظ الصورة باسم: {file_name}")
            else:
                QMessageBox.warning(self, "فشل", "لم يتم العثور على صور لهذا الهاتف.")

        except Exception as e:
            QMessageBox.critical(self, "خطأ في الاتصال", f"حدث خطأ: {str(e)}")
        
        self.search_btn.setText("بحث وتحميل الصورة")
        self.search_btn.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PhoneImageDownloader()
    ex.show()
    sys.exit(app.exec_())
