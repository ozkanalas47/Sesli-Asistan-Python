from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
import sys
import re
from pathlib import Path
import random

# Proje kök dizinini sys.path'e ekle
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.hata_gunlugu import log_hata
from utils.config import load_config

class NLPModel:
    def __init__(self, model_name="google/gemma-2b-it"):
        """Gemma-2b modelini başlatır."""
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.config = load_config()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Intent mapping - daha hızlı keyword-based analiz
        self.intent_keywords = {
            'selamlaşma': ['merhaba', 'selam', 'hey', 'hi'],
            'hava_durumu': ['hava durumu', 'hava', 'sıcaklık', 'yağmur'],
            'hangi_gün': ['hangi gün', 'bugün günlerden ne'],
            'saat': ['saat kaç', 'kaç saat', 'zaman'],
            'tam_tarih': ['bugün günlerden', 'tarih'],
            'bilgi_soru': ['nedir', 'ne demek', 'kimdir', 'bilgi ver'],
            'not_al': ['not al', 'not kaydet', 'hatırlat'],
            'hesaplama': ['hesapla', 'topla', 'çıkar', 'çarp', 'böl'],
            'müzik_çal': ['müzik çal', 'şarkı çal', 'müzik'],
            'çıkış': ['çık', 'kapat', 'görüşürüz', 'hoşçakal'],
            'sohbet': ['naber', 'nasılsın', 'muhabbet', 'sohbet', 'ne haber']
        }
        # Günlük konuşma için yanıt şablonları
        self.sohbet_templates = [
            "Kanka, naber? Günün nasıl geçti?",
            "Valla buralardayım, sen ne anlatacan?",
            "Hey, ne güzel seni görmek! Ne yapalım?",
            "Nasılsın be, bi’ şeyler mi yapsak?",
            "Ooo, sen nerdesin? Anlat bakalım!"
        ]

    def load(self):
        """Modeli lazy loading ile yükler."""
        if self.model is None or self.tokenizer is None:
            try:
                print("Gemma-2B modeli yükleniyor...")
                
                # Tokenizer yükle
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                
                # Padding token ayarla
                if self.tokenizer.pad_token is None:
                    self.tokenizer.pad_token = self.tokenizer.eos_token
                
                # Model yükle
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    device_map="auto" if self.device == "cuda" else None
                )
                
                if self.device == "cpu":
                    self.model = self.model.to(self.device)
                
                self.model.eval()
                print(f"Model hazır! Device: {self.device}")
                
            except Exception as e:
                log_hata(f"Model yükleme hatası: {str(e)}")
                print(f"Model yükleme hatası: {str(e)}")
                raise

    def generate(self, prompt, max_length=100):
        """Sohbet için metin üretir."""
        try:
            self.load()
            
            # Intent analizi ile sohbet kontrolü
            intent = self.analyze_intent(prompt)
            
            # Sohbet niyeti için özel prompt
            if intent == "sohbet":
                # if-else ile bağlama göre yanıt seçimi
                prompt_lower = prompt.lower()
                if "naber" in prompt_lower or "ne haber" in prompt_lower:
                    base_response = random.choice(self.sohbet_templates[:2])  # Naber için uygun yanıtlar
                elif "nasılsın" in prompt_lower:
                    base_response = random.choice(self.sohbet_templates[3:])  # Nasılsın için uygun yanıtlar
                elif "muhabbet" in prompt_lower or "sohbet" in prompt_lower:
                    base_response = "Tamam kanka, muhabbetin dibine vuralım! Sen neyden bahsetmek istersin?"
                else:
                    base_response = random.choice(self.sohbet_templates)  # Genel samimi yanıt
                
                formatted_prompt = f"""
                Sen arkadaş canlısı, günlük konuşma tarzında bir asistansın. Kullanıcıyla samimi, kanka gibi konuş.
                Kullanıcı: {prompt}
                Asistan: {base_response}
                """
            else:
                # Diğer niyetler için varsayılan prompt
                formatted_prompt = f"Kullanıcı: {prompt}\nAsistan:"
            
            inputs = self.tokenizer(
                formatted_prompt, 
                return_tensors="pt", 
                padding=True, 
                truncation=True,
                max_length=512
            )
            
            if self.device == "cuda":
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=len(inputs['input_ids'][0]) + max_length,
                    min_length=len(inputs['input_ids'][0]) + 10,
                    temperature=0.7,
                    do_sample=True,
                    top_p=0.9,
                    top_k=50,
                    repetition_penalty=1.1,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    num_return_sequences=1
                )
            
            # Cevabı çözümle
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Sadece asistan kısmını al
            response = generated_text.split("Asistan:")[-1].strip()
            
            # Eğer çok kısa ise veya boş ise varsayılan cevap
            if len(response) < 5:
                response = "Anlıyorum, başka nasıl yardımcı olabilirim?"
            
            return response
            
        except Exception as e:
            log_hata(f"Metin üretme hatası: {str(e)}")
            return "Teknik bir sorun oluştu, tekrar deneyin."

    def analyze_intent(self, metin):
        """Hızlı keyword-based intent analizi."""
        try:
            metin_lower = metin.lower()
            
            # En uzun eşleşmeyi bul
            best_match = ("sohbet", 0)
            
            for intent, keywords in self.intent_keywords.items():
                for keyword in keywords:
                    if keyword in metin_lower:
                        score = len(keyword)
                        if score > best_match[1]:
                            best_match = (intent, score)
            
            return best_match[0]
            
        except Exception as e:
            log_hata(f"Intent analizi hatası: {str(e)}")
            return "sohbet"

    def cleanup(self):
        """Bellek temizleme."""
        try:
            if hasattr(self, 'model') and self.model is not None:
                del self.model
            if hasattr(self, 'tokenizer') and self.tokenizer is not None:
                del self.tokenizer
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            print("Model bellekten temizlendi.")
        except Exception as e:
            log_hata(f"Model temizleme hatası: {str(e)}")

if __name__ == "__main__":
    # Test
    try:
        print(f"PyTorch: {torch.__version__}")
        print(f"CUDA mevcut: {torch.cuda.is_available()}")
        
        model = NLPModel()
        
        # Intent testi
        test_commands = [
            "merhaba nasılsın",
            "hava durumu nasıl",
            "saat kaç",
            "müzik çal",
            "hesapla 5 + 3",
            "naber kanka",
            "biraz muhabbet edelim"
        ]
        
        print("\n=== Intent Testleri ===")
        for cmd in test_commands:
            intent = model.analyze_intent(cmd)
            print(f"'{cmd}' -> {intent}")
        
        # Model yükleme ve sohbet testi
        print("\n=== Model Yükleme ve Sohbet Testi ===")
        test_sohbet = [
            "Merhaba, nasılsın?",
            "Naber kanka?",
            "Biraz muhabbet edelim mi?"
        ]
        for cmd in test_sohbet:
            response = model.generate(cmd)
            print(f"Girdi: {cmd} -> Yanıt: {response}")
        
        # Temizleme
        model.cleanup()
        
    except Exception as e:
        print(f"Test hatası: {str(e)}")
        print("Lütfen requirements.txt dosyasındaki kütüphaneleri kontrol edin.")