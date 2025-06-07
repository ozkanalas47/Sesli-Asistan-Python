import os
from gtts import gTTS
import pygame
from utils.hata_gunlugu import log_hata
from utils.dosya_temizleme import temizle_gecici_dosya

def konus(metin, ui):
    """Metni sese çevirir ve oynatır."""
    try:
        if not metin:
            return

        # Geçici ses dosyası
        ses_dosyasi = "data/temp/temp_konusma.mp3"
        os.makedirs("data/temp", exist_ok=True)

        # gTTS ile ses dosyası oluştur
        tts = gTTS(text=metin, lang="tr")
        tts.save(ses_dosyasi)

        # pygame ile sesi oynat
        pygame.mixer.init()
        pygame.mixer.music.load(ses_dosyasi)
        pygame.mixer.music.play()

        # Ses çalarken bekle
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Ses dosyasını temizle
        pygame.mixer.quit()
        temizle_gecici_dosya(ses_dosyasi)

    except Exception as e:
        log_hata(f"Konuşma hatası: {str(e)}")
        ui.append_message("Asistan", "Sesli yanıt üretilemedi.")