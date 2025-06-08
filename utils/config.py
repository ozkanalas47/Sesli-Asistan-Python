import os
from dotenv import load_dotenv
from utils.hata_gunlugu import log_hata

def load_config():
    """Yapılandırma ayarlarını .env dosyasından yükler."""
    try:
        load_dotenv()
        config = {
            "OPENWEATHERMAP_API_KEY": os.getenv("OPENWEATHERMAP_API_KEY", "default_key"),
            "MODEL_NAME": os.getenv("MODEL_NAME", "google/gemma-2b"),
            "HF_TOKEN": os.getenv("HF_TOKEN", ""),
            "DATA_DIR": os.getenv("DATA_DIR", "data/"),
            "TEMP_DIR": os.getenv("TEMP_DIR", "data/temp/"),
            "NOTLAR_DIR": os.getenv("NOTLAR_DIR", "data/notlar/"),
            "MUZIKLER_DIR": os.getenv("MUZIKLER_DIR", "data/muzikler/"),
            "LOGS_DIR": os.getenv("LOGS_DIR", "data/logs/")
        }
        return config
    except Exception as e:
        log_hata(f"Yapılandırma yükleme hatası: {str(e)}")
        return {}