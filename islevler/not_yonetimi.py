import os
from datetime import datetime
from utils.hata_gunlugu import log_hata

def not_kaydet(not_metni):
    """Notu dosyaya kaydeder."""
    try:
        if not not_metni:
            return "Not olarak ne yazayım?"
        os.makedirs("data/notlar", exist_ok=True)
        with open("data/notlar/notlar.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()}: {not_metni}\n")
        return "Not alındı!"
    except Exception as e:
        log_hata(f"Not kaydetme hatası: {str(e)}")
        return "Not kaydedilemedi."

def notlari_goster():
    """Kayıtlı notları döndürür."""
    try:
        if not os.path.exists("data/notlar/notlar.txt"):
            return "Henüz hiç not alınmamış."
        with open("data/notlar/notlar.txt", "r", encoding="utf-8") as f:
            notlar = f.readlines()
        return "\n".join(notlar[-5:]) or "Not bulunamadı."
    except Exception as e:
        log_hata(f"Not gösterme hatası: {str(e)}")
        return "Notlar gösterilemedi."