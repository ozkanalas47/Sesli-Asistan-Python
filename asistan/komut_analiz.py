import re
from .nlp_model import NLPModel
from utils.hata_gunlugu import log_hata
from utils.config import load_config

def komut_analiz_et(metin, nlp_model=None):
    """Metni analiz ederek niyet (intent) ve ek bilgi çıkarır."""
    if not metin:
        return None, None

    try:
        # NLP modelini başlat
        if nlp_model is None:
            config = load_config()
            nlp_model = NLPModel(config.get("MODEL_NAME", "google/gemma-2b"))

        # Basit kelime eşleştirme (fallback)
        intent_mapping = {
            "merhaba": "selamlaşma",
            "selam": "selamlaşma",
            "hava durumu": "hava_durumu",
            "müzik çal": "müzik_çal",
            "çık": "çıkış",
            "kapat": "çıkış",
            "hangi gündeyiz": "hangi_gün",
            "saat kaç": "saat",
            "not al": "not_al",
            "hesapla": "hesaplama",
            "bugün günlerden ne": "tam_tarih"
        }

        metin_lower = metin.lower()
        for keyword, intent in intent_mapping.items():
            if keyword in metin_lower:
                if intent == "hava_durumu":
                    sehir = re.sub(r"\b" + keyword + r"\b", "", metin, flags=re.IGNORECASE).strip() or "İstanbul"
                    return intent, sehir
                elif intent in ["not_al", "hesaplama"]:
                    return intent, re.sub(r"\b" + keyword + r"\b", "", metin, flags=re.IGNORECASE).strip()
                return intent, None

        # NLP modeliyle niyet tahmini
        intent = nlp_model.analyze_intent(metin)
        if intent in intent_mapping.values():
            if intent == "hava_durumu":
                sehir = re.search(r"(?:için|de|daki)\s+([A-Za-zÇçĞğİıÖöŞşÜü\s]+)", metin, re.IGNORECASE)
                return intent, sehir.group(1).strip() if sehir else "İstanbul"
            elif intent in ["not_al", "hesaplama"]:
                return intent, metin
            elif intent == "bilgi_soru":
                return intent, metin
            return intent, None

        # Bilgi sorusu veya sohbet fallback
        if any(k in metin_lower for k in ["nedir", "ne demek", "kimdir", "bilgi ver"]):
            return "bilgi_soru", metin
        return "sohbet", metin

    except Exception as e:
        log_hata(f"Komut analizi hatası: {str(e)}")
        return "sohbet", metin