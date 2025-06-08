import os
from datetime import datetime

def log_hata(mesaj):
    """Hata mesajını log dosyasına kaydeder."""
    try:
        os.makedirs("data/logs", exist_ok=True)
        log_dosyasi = f"data/logs/hata_{datetime.now().strftime('%Y%m%d')}.log"
        with open(log_dosyasi, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {mesaj}\n")
    except Exception as e:
        print(f"Log yazma hatası: {str(e)}")  