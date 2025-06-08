import requests
from functools import lru_cache
from utils.hata_gunlugu import log_hata
from utils.config import load_config

@lru_cache(maxsize=100)
def hava_durumu_sor(sehir="İstanbul"):
    """Hava durumu bilgisi alır (önbellekli)."""
    try:
        config = load_config()
        api_key = config.get("OPENWEATHERMAP_API_KEY", "default_key")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={sehir}&appid={api_key}&lang=tr&units=metric"
        response = requests.get(url, timeout=5).json()
        
        if response.get("cod") == 200:
            temp = response["main"]["temp"]
            desc = response["weather"][0]["description"]
            return f"{sehir} için hava {desc}, sıcaklık {temp}°C"
        else:
            log_hata(f"Hava durumu hatası: {response.get('message', 'Bilinmeyen hata')}")
            return f"{sehir} için hava durumu alınamadı."
    except requests.RequestException as e:
        log_hata(f"Hava durumu API hatası: {str(e)}")
        return "Hava durumu servisi şu anda çalışmıyor."
    except Exception as e:
        log_hata(f"Hava durumu genel hata: {str(e)}")
        return "Hava durumu bilgisi alınamadı."