from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from .ui_events import SesDinlemeThread
from utils.hata_gunlugu import log_hata
from datetime import datetime

class SesliAsistanUI(QMainWindow):
    append_message_signal = pyqtSignal(str, str)

    def __init__(self, asistan):
        super().__init__()
        self.asistan = asistan
        self.is_listening = False
        self.thread = None
        self.init_ui()
        self.append_message_signal.connect(self._append_message)

    def init_ui(self):
        """Arayüzü oluşturur."""
        self.setWindowTitle("Sesli Asistan")
        self.setGeometry(100, 100, 900, 700)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setFont(QFont("Arial", 16))
        self.chat_area.setStyleSheet("""
            QTextEdit {
                background-color: #2E2E2E;
                color: #FFFFFF;
                border: 2px solid #4CAF50;
                border-radius: 12px;
                padding: 20px;
                font-size: 18px;
            }
        """)
        self.layout.addWidget(self.chat_area, stretch=5)

        self.button_layout = QHBoxLayout()

        self.listen_button = QPushButton("Sesli Komut")
        self.listen_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #555555;
            }
        """)
        self.listen_button.clicked.connect(self.toggle_listening)
        self.button_layout.addWidget(self.listen_button)

        self.stop_button = QPushButton("Durdur")
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                font-size: 18px;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
        """)
        self.stop_button.clicked.connect(self.stop_listening)
        self.button_layout.addWidget(self.stop_button)

        self.exit_button = QPushButton("Çıkış")
        self.exit_button.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                font-size: 18px;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
        """)
        self.exit_button.clicked.connect(self.close)
        self.button_layout.addWidget(self.exit_button)

        self.layout.addLayout(self.button_layout)

        self.setStyleSheet("background-color: #1E1E1E;")

        # Zaman dilimine göre karşılama mesajı
        current_hour = datetime.now().hour
        if 0 <= current_hour < 5:  # 00:00-05:00
            welcome_message = "Gece yarısı naber kanka? Uykusuzluk mu çekiyon, anlat!"
        elif 5 <= current_hour < 12:  # 05:00-12:00
            welcome_message = "Günaydın kral! Günün enerjisi sende, ne yapalım?"
        elif 12 <= current_hour < 17:  # 12:00-17:00
            welcome_message = "Hey kanka, öğlen molasında mıyız? Ne haber?"
        elif 17 <= current_hour < 22:  # 17:00-22:00
            welcome_message = "Akşam akşam naber? Hadi bi’ şeyler yapalım!"
        else:  # 22:00-00:00
            welcome_message = "Gece kuşu, n’oluyo? Anlat bakalım!"
        self.append_message("Asistan", welcome_message)
        # Karşılama mesajını sesli oku
        try:
            self.asistan.speak(welcome_message, self)
        except Exception as e:
            log_hata(f"Karşılama mesajı seslendirme hatası: {str(e)}")
            self.append_message("Asistan", "Karşılama mesajını seslendiremedim, ama buradayım!")

    def append_message(self, sender, message):
        try:
            self.append_message_signal.emit(sender, message)
        except Exception as e:
            log_hata(f"Mesaj ekleme sinyal hatası: {str(e)}")

    def _append_message(self, sender, message):
        try:
            if sender == "Kullanıcı":
                self.chat_area.append(f"<b style='color: #4CAF50'>{sender}:</b> {message}")
            else:
                self.chat_area.append(f"<b style='color: #FFFFFF'>{sender}:</b> {message}")
            self.chat_area.append("")
            self.chat_area.verticalScrollBar().setValue(self.chat_area.verticalScrollBar().maximum())
        except Exception as e:
            log_hata(f"Mesaj ekleme hatası: {str(e)}")

    def toggle_listening(self):
        try:
            if not self.is_listening:
                self.is_listening = True
                self.listen_button.setText("Dinleniyor...")
                self.listen_button.setStyleSheet("""
                    QPushButton {
                        background-color: #0288d1;
                        color: white;
                        font-size: 18px;
                        padding: 12px 24px;
                        border-radius: 8px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #0277bd;
                    }
                    QPushButton:disabled {
                        background-color: #555555;
                    }
                """)
                self.start_listening()
            else:
                self.stop_listening()
        except Exception as e:
            log_hata(f"Ses dinleme toggle hatası: {str(e)}")
            self.append_message("Asistan", "Bir hata oluştu.")
            self.reset_button()

    def start_listening(self):
        try:
            self.listen_button.setEnabled(False)
            self.append_message("Asistan", "Dinliyorum...")
            self.thread = SesDinlemeThread(self.asistan, self)
            self.thread.command_processed.connect(self.on_command_processed)
            self.thread.start()
        except Exception as e:
            log_hata(f"Ses dinleme başlatma hatası: {str(e)}")
            self.append_message("Asistan", "Ses dinleme başlatılamadı.")
            self.reset_button()

    def stop_listening(self):
        try:
            self.is_listening = False
            if self.thread:
                self.thread.stop()
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.stop()
            self.append_message("Asistan", "Durduruldu.")
            self.reset_button()
        except Exception as e:
            log_hata(f"Durdurma hatası: {str(e)}")
            self.append_message("Asistan", "Durdurma sırasında hata oluştu.")
            self.reset_button()

    def on_command_processed(self, should_exit):
        try:
            if should_exit:
                self.close()
            else:
                self.reset_button()
        except Exception as e:
            log_hata(f"Komut işleme sonrası hata: {str(e)}")
            self.append_message("Asistan", "Bir hata oluştu.")
            self.reset_button()

    def reset_button(self):
        self.is_listening = False
        self.listen_button.setText("Sesli Komut")
        self.listen_button.setEnabled(True)
        self.listen_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)