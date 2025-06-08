import random
from utils.hata_gunlugu import log_hata

def sohbet_yap(mesaj, conversation_history, nlp_model):
    """Gemma-2b ile sohbet yanıtı üretir."""
    try:
        if not mesaj:
            return "Ne hakkında konuşmak istersin?"

        if "fıkra" in mesaj.lower():
            fikralar = [
                "Tavuk neden yolu geçti? Karşı tarafa geçmek için tabii!",
                "Matematik kitabı neden üzgündü? Çünkü çok problemi vardı!"
            ]
            return random.choice(fikralar)

        if "konu aç" in mesaj.lower():
            konular = ["Favori filmin nedir?", "Hafta sonu ne yapmayı planlıyorsun?", "En sevdiğin yemek hangisi?"]
            return random.choice(konular)

        prompt = f"""Sen dostça ve yardımsever bir Türkçe asistanısın. Kullanıcının mesajına kısa, doğal ve net bir yanıt ver.
Geçmiş konuşma:
{''.join(conversation_history[-4:])}
Kullanıcı: {mesaj}
Asistan:"""

        conversation_history.append(f"Kullanıcı: {mesaj}")
        yanit = nlp_model.generate(prompt)
        yanit = yanit.split("Asistan:")[-1].strip().split('\n')[0].split('.')[0]
        
        conversation_history.append(f"Asistan: {yanit}")
        return yanit or "Anladım ama cevap veremiyorum"
    except Exception as e:
        log_hata(f"Sohbet hatası: {str(e)}")
        return "Sohbet sırasında bir hata oluştu."