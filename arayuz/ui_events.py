from PyQt5.QtCore import QThread, pyqtSignal
from utils.hata_gunlugu import log_hata

class SesDinlemeThread(QThread):
    command_processed = pyqtSignal(bool)  # Komut işlendikten sonra sinyal

    def __init__(self, asistan, ui):
        super().__init__()
        self.asistan = asistan
        self.ui = ui
        self.is_running = True

    def run(self):
        """Ses dinleme işlemini thread içinde çalıştırır."""
        try:
            should_exit = self.asistan.process_command(self.ui)
            self.command_processed.emit(should_exit)
        except Exception as e:
            log_hata(f"Ses dinleme thread hatası: {str(e)}")
            self.ui.append_message("Asistan", "Bir hata oluştu.")
            self.command_processed.emit(False)

    def stop(self):
        """Thread'i durdurur."""
        self.is_running = False
        self.quit()
        self.wait()