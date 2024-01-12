# This Code Made by D3F417
# Github : https://github.com/mss-d3f417
# Don't Copy Script KIDI 

import sys
import os
import PyPDF2
import requests
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from plyer import notification

class PDFLockApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Locker | D3F417")
        self.setGeometry(100, 100, 800, 600)

        self.setStyleSheet("background-color: transparent;")

        background_image_url = 'https://uploadkon.ir/uploads/154312_24Arcane.jpg'
        background_image_path = os.path.join(os.getenv('APPDATA'), 'PDFLockApp-D3f417', 'background_image.jpg')

        if not os.path.exists(background_image_path):
            try:
                response = requests.get(background_image_url)
                os.makedirs(os.path.dirname(background_image_path), exist_ok=True)
                with open(background_image_path, 'wb') as img_file:
                    img_file.write(response.content)
            except Exception as e:
                print(f"Error downloading image: {e}")

        background_label = QLabel(self)
        background_label.setGeometry(0, 0, 800, 600)
        pixmap = QPixmap(background_image_path)
        pixmap = pixmap.scaled(QSize(800, 600), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        background_label.setPixmap(pixmap)

        layout = QVBoxLayout()

        self.title_label = QLabel("<h1 style='color: #ffffff; font-weight: bold;'>PDF Locker | D3F417</h1>")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        self.pdf_path_label = QLabel("Select a PDF file:")
        self.pdf_path_label.setStyleSheet("color: #ffffff; font-size: 14px;")
        layout.addWidget(self.pdf_path_label)

        self.pdf_path = QTextEdit()
        self.pdf_path.setStyleSheet("color: #ffffff; font-size: 12px; font-weight: bold;")
        layout.addWidget(self.pdf_path)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_pdf)
        self.browse_button.setStyleSheet("color: #ffffff; background-color: #8c47b7 ; font-weight: bold;")
        layout.addWidget(self.browse_button)

        self.password_label = QLabel("Enter the password to lock the PDF:")
        self.password_label.setStyleSheet("color: #ffffff; font-size: 14px;")
        layout.addWidget(self.password_label)

        self.password = QTextEdit()
        self.password.setPlaceholderText("Enter password here...")
        self.password.setStyleSheet("color: #ffffff; font-size: 12px; font-weight: bold;")
        layout.addWidget(self.password)

        self.lock_button = QPushButton("Lock PDF")
        self.lock_button.clicked.connect(self.lock_pdf)
        self.lock_button.setStyleSheet("color: #ffffff; background-color: #3084f2; font-weight: bold;")
        layout.addWidget(self.lock_button)

        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        self.setLayout(layout)

        self.populate_files()

    def browse_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF file", "", "PDF files (*.pdf);;All Files (*)")
        if file_path:
            self.pdf_path.setPlainText(file_path)

    def lock_pdf(self):
        input_pdf = self.pdf_path.toPlainText()
        password = self.password.toPlainText()

        if not input_pdf or not password:
            QMessageBox.warning(self, "Warning", "Please enter both PDF file path and password.")
        else:
            try:
                with open(input_pdf, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    pdf_writer = PyPDF2.PdfWriter()

                    for page_num in range(len(pdf_reader.pages)):
                        pdf_writer.add_page(pdf_reader.pages[page_num])

                    pdf_writer.encrypt(password)

                    with open(input_pdf, 'wb') as output_file:
                        pdf_writer.write(output_file)

                success_message = "<h2 style='color:#28A745; font-weight: bold;'>PDF locked successfully.</h2>"
                self.display_html(success_message)

                # Show system notification
                notification_title = "PDF Locker"
                notification_message = "PDF locked successfully."
                notification.notify(
                    title=notification_title,
                    message=notification_message,
                    app_icon=None,
                    timeout=10,
                )

            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def populate_files(self):
        pass

    def display_html(self, html_content):
        self.web_view.setHtml(html_content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFLockApp()
    window.show()
    sys.exit(app.exec_())