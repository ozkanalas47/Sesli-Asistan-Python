Sesli Asistan
Türkçe sesli komutlarla çalışan bir asistan uygulaması. Hava durumu, saat, not alma, müzik çalma, Wikipedia sorguları ve sohbet gibi işlevler sunar. PyQt5 ile kullanıcı arayüzü ve Gemma-2b ile doğal dil işleme entegrasyonu içerir.
Özellikler

Sesli komut tanıma (speech_recognition)
Metni sese çevirme (gTTS, pygame)
Hava durumu sorgulama (OpenWeatherMap API)
Saat, tarih ve gün bilgisi
Wikipedia bilgi sorgulama
Not alma ve gösterme
Yerel müzik çalma/durdurma
Matematiksel hesaplama (sympy)
Türkçe sohbet (Gemma-2b)
Modern PyQt5 arayüzü

Kurulum

Bağımlılıkları yükleyin:
pip install -r requirements.txt


.env dosyasını yapılandırın:.env dosyasına OpenWeatherMap API anahtarınızı ekleyin:
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key


Uygulamayı çalıştırın:
python main.py



Kullanım

Uygulamayı başlatın, PyQt5 arayüzü açılır.
"Başlat" butonuna tıklayın ve sesli komut verin (örneğin, "Hava durumu İstanbul", "Saat kaç", "Not al: toplantı yarın").
Komutlar:
Selamlaşma: "Merhaba", "Selam"
Hava durumu: "Hava durumu [şehir]"
Zaman: "Saat kaç", "Hangi gündeyiz", "Bugün günlerden ne"
Bilgi sorgu: "[Konu] nedir", "[Kişi] kimdir"
Not alma: "Not al: [metin]"
Müzik: "Müzik çal", "Müzik durdur"
Hesaplama: "Hesapla [ifade]"
Sohbet: "Fıkra anlat", "Konu aç" veya serbest konuşma
Çıkış: "Çık", "Kapat"



Dosya Yapısı
sesli_asistan/
├── main.py
├── asistan/
├── islevler/
├── arayuz/
├── utils/
├── data/
│   ├── notlar/
│   ├── muzikler/
│   ├── logs/
│   ├── temp/
├── requirements.txt
├── .env
├── README.md

Notlar

Geçici ses dosyaları data/temp/ dizininde saklanır ve otomatik temizlenir.
Loglar data/logs/ dizininde tutulur.
Notlar data/notlar/notlar.txt dosyasına kaydedilir.
Müzik dosyaları data/muzikler/ dizinine yerleştirilmelidir.
