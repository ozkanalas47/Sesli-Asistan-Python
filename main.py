import sys
from PyQt5.QtWidgets import QApplication
from asistan.core import SesliAsistan
from arayuz.ui import SesliAsistanUI
from utils.config import load_config
from utils.hata_gunlugu import log_hata

def main():
    """Uygulamayı başlatır."""
    try:
        # Yapılandırmayı yükle
        config = load_config()
        print("Yapılandırma yüklendi.")
        
        # PyQt5 uygulamasını başlat
        app = QApplication(sys.argv)
        print("PyQt5 uygulaması başlatıldı.")
        
        # Sesli asistan ve UI sınıflarını başlat
        asistan = SesliAsistan(config)
        print("SesliAsistan başlatıldı.")
        window = SesliAsistanUI(asistan)
        print("SesliAsistanUI başlatıldı.")
        
        # Pencereyi göster
        window.show()
        print("Pencere gösterildi.")
        
        # Uygulamayı çalıştır
        sys.exit(app.exec_())
    except Exception as e:
        log_hata(f"Uygulama başlatılırken hata: {str(e)}")
        print(f"Hata oluştu: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()