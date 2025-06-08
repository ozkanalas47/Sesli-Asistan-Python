import os
from utils.hata_gunlugu import log_hata
from utils.config import load_config

def check_api_keys():
    """API anahtarlarının varlığını kontrol eder."""
    try:
        config = load_config()
        required_keys = ["OPENWEATHERMAP_API_KEY"]
        missing_keys = [key for key in required_keys if not config.get(key)]
        if missing_keys:
            log_hata(f"Eksik API anahtarları: {missing_keys}")
            return False, f"Eksik API anahtarları: {', '.join(missing_keys)}"
        return True, "API anahtarları mevcut."
    except Exception as e:
        log_hata(f"API anahtar kontrol hatası: {str(e)}")
        return False, "API anahtarları kontrol edilemedi."

def check_dependencies():
    """Gerekli kütüphanelerin yüklü olduğunu kontrol eder."""
    try:
        import speech_recognition
        import gtts
        import pygame
        import requests
        import wikipedia
        import sympy
        import transformers
        return True, "Tüm bağımlılıklar yüklü."
    except ImportError as e:
        log_hata(f"Bağımlılık eksik: {str(e)}")
        return False, f"Bağımlılık eksik: {str(e)}"