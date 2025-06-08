from datetime import datetime
from utils.hata_gunlugu import log_hata

def hangi_gun():
    """Haftanın gününü döndürür."""
    try:
        return datetime.now().strftime("Bugün %A")
    except Exception as e:
        log_hata(f"Hangi gün hatası: {str(e)}")
        return "Gün bilgisi alınamadı."

def saat():
    """Saati döndürür."""
    try:
        return datetime.now().strftime("Saat %H:%M")
    except Exception as e:
        log_hata(f"Saat hatası: {str(e)}")
        return "Saat bilgisi alınamadı."

def tam_tarih():
    """Tam tarihi döndürür."""
    try:
        return datetime.now().strftime("%d %B %Y, %A")
    except Exception as e:
        log_hata(f"Tam tarih hatası: {str(e)}")
        return "Tarih bilgisi alınamadı."