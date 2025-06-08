import os
import pygame.mixer
from utils.hata_gunlugu import log_hata

def muzik_cal():
    """Yerel müzik dosyasını çalar."""
    try:
        muzik_dosyasi = "data/muzikler/ornek_muzik.mp3"
        if not os.path.exists(muzik_dosyasi):
            return "Müzik dosyası bulunamadı."
        pygame.mixer.init()
        pygame.mixer.music.load(muzik_dosyasi)
        pygame.mixer.music.play()
        return "Müzik çalıyor!"
    except Exception as e:
        log_hata(f"Müzik çalma hatası: {str(e)}")
        return "Müzik çalınamadı."

def muzik_durdur():
    """Müzik çalmayı durdurur."""
    try:
        pygame.mixer.init()
        pygame.mixer.music.stop()
        return "Müzik durduruldu."
    except Exception as e:
        log_hata(f"Müzik durdurma hatası: {str(e)}")
        return "Müzik durdurulamadı."