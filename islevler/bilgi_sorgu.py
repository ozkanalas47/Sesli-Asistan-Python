import wikipedia
import re
from utils.hata_gunlugu import log_hata

def bilgi_sor(soru):
    """Wikipedia'dan bilgi sorgular."""
    try:
        wikipedia.set_lang("tr")
        sorgu = re.sub(r"\b(nedir|ne demek|kimdir|bilgi ver)\b", "", soru, flags=re.IGNORECASE).strip()
        if not sorgu:
            return "Ne hakkında bilgi almak istiyorsun?"
        summary = wikipedia.summary(sorgu, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError:
        log_hata("Wikipedia'da birden fazla sonuç bulundu.")
        return "Lütfen daha spesifik bir sorgu girin."
    except wikipedia.exceptions.PageError:
        log_hata(f"Wikipedia sayfası bulunamadı: {sorgu}")
        return "Bu konuda bilgi bulamadım."
    except Exception as e:
        log_hata(f"Bilgi sorgu hatası: {str(e)}")
        return "Bilgi alınamadı, lütfen tekrar deneyin."