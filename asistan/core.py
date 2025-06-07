from .komut_analiz import komut_analiz_et
from .ses_isleme import sesi_metne_cevir
from .konusma import konus
from .nlp_model import NLPModel
from islevler.sohbet import sohbet_yap
from islevler.hava_durumu import hava_durumu_sor
from islevler.zaman import hangi_gun, saat, tam_tarih
from islevler.bilgi_sorgu import bilgi_sor
from islevler.not_yonetimi import not_kaydet
from islevler.muzik import muzik_cal
from islevler.hesaplama import hesapla
from utils.hata_gunlugu import log_hata

class SesliAsistan:
    def __init__(self, config):
        """Sesli asistanı başlatır."""
        self.config = config
        self.conversation_history = []
        self.nlp_model = NLPModel(config.get("MODEL_NAME", "google/gemma-2b"))
        self.komut_handler = {
            "selamlaşma": lambda _: "Merhaba! Sana nasıl yardımcı olabilirim?",
            "hava_durumu": hava_durumu_sor,
            "hangi_gün": hangi_gun,
            "saat": saat,
            "tam_tarih": tam_tarih,
            "bilgi_soru": bilgi_sor,
            "sohbet": lambda mesaj: sohbet_yap(mesaj, self.conversation_history, self.nlp_model),
            "not_al": not_kaydet,
            "hesaplama": hesapla,
            "müzik_çal": muzik_cal,
            "çıkış": lambda _: "Görüşürüz!"
        }

    def process_command(self, ui):
        """Sesli komutu işler ve yanıt döndürür."""
        try:
            metin = sesi_metne_cevir()
            if not metin:
                yanit = "Tekrar eder misiniz?"
                ui.append_message("Asistan", yanit)
                konus(yanit, ui)
                return False

            ui.append_message("Kullanıcı", metin)
            intent, ek_bilgi = komut_analiz_et(metin)

            if intent in self.komut_handler:
                yanit = self.komut_handler[intent](ek_bilgi) if ek_bilgi else self.komut_handler[intent]()
            else:
                yanit = "Bunu yapamıyorum. Hava durumu, saat veya bilgi sormayı deneyebilir misin?"

            ui.append_message("Asistan", yanit)
            konus(yanit, ui)
            return intent == "çıkış"  # Çıkış sinyali
        except Exception as e:
            log_hata(f"Komut işlenirken hata: {str(e)}")
            yanit = "Bir hata oluştu, lütfen tekrar deneyin."
            ui.append_message("Asistan", yanit)
            konus(yanit, ui)
            return False