from sympy import sympify, sin, cos, tan
from utils.hata_gunlugu import log_hata

def hesapla(ifade):
    """Matematiksel ifadeyi hesaplar."""
    try:
        if not ifade:
            return "Hangi hesabı yapayım?"
        sonuc = sympify(ifade, locals={"sin": sin, "cos": cos, "tan": tan})
        return f"Sonuç: {sonuc.evalf()}"
    except Exception as e:
        log_hata(f"Hesaplama hatası: {str(e)}")
        return "Hesaplama başarısız, lütfen geçerli bir ifade girin."