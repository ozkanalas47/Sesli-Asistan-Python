import speech_recognition as sr
from utils.hata_gunlugu import log_hata

def sesi_metne_cevir():
    """Sesli girişi metne çevirir."""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Dinliyorum...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            metin = recognizer.recognize_google(audio, language="tr-TR")
            print(f"Anladım: {metin}")
            return metin.lower()
    except sr.UnknownValueError:
        log_hata("Ses anlaşılamadı")
        return None
    except sr.RequestError as e:
        log_hata(f"Ses tanıma servisi hatası: {str(e)}")
        return None
    except Exception as e:
        log_hata(f"Ses işleme hatası: {str(e)}")
        return None