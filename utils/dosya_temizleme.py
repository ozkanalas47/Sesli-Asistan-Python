import os
import glob
from utils.hata_gunlugu import log_hata

def temizle_gecici_dosya(dosya_yolu=None):
    """Belirtilen dosyayı veya tüm geçici dosyaları siler."""
    try:
        os.makedirs("data/temp", exist_ok=True)
        if dosya_yolu and os.path.exists(dosya_yolu):
            os.remove(dosya_yolu)
        else:
            for dosya in glob.glob("data/temp/temp_*.mp3"):
                os.remove(dosya)
    except Exception as e:
        log_hata(f"Geçici dosya temizleme hatası: {str(e)}")