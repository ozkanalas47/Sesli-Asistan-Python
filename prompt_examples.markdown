# Sesli Asistan Prompt Örnekleri

Bu dosya, sesli asistanın işlevlerini tetiklemek için kullanılabilecek doğal dil komut (prompt) örneklerini içerir. Komutları sesli olarak söylerken net ve doğal ifadeler kullanabilirsiniz. Her bölüm, asistanın bir işlevine karşılık gelir.

## 1. Sohbet Yapma
Asistanla günlük, arkadaş canlısı bir sohbet başlatmak için:
- Merhaba, nasılsın?
- Selam kanka, günün nasıl geçti?
- Nasılsın, biraz muhabbet edelim mi?
- Bugün hava nasıl sence?
- Benden sana bir soru: En sevdiğin renk ne?
- Hey, neler yapıyorsun?
- Canın sıkılıyor mu, biraz laflayalım!

## 2. Hava Durumu Sorgulama
Belirli bir şehir için hava durumu bilgisi almak için:
- Hava durumu İstanbul
- Bugün Ankara’da hava nasıl?
- İzmir için hava durumu söyler misin?
- Antalya’da hava nasıl?
- Yarın İstanbul’da hava durumu ne olacak?
- Bursa’nın havası nasıl?
- Adana’da bugün hava kaç derece?

## 3. Zaman Bilgisi
Saat, gün veya tam tarih bilgisi için:
- Saat kaç?
- Bugün günlerden ne?
- Tam tarih ne?
- Hangi gündeyiz?
- Şu an saat kaç?
- Yarın hangi gün?
- Bugün ayın kaçı?

## 4. Bilgi Sorgulama (Wikipedia)
Genel bilgi veya belirli bir konuda bilgi almak için:
- Atatürk kimdir?
- Python nedir?
- Türkiye’nin başkenti neresi?
- Blockchain hakkında bilgi ver.
- Kuantum fiziği ne demek?
- İstanbul’un tarihi hakkında bilgi ver.
- Yapay zeka nedir?

## 5. Not Yönetimi
Not kaydetmek, listelemek veya silmek için:
- Not al: Yarın markete git, ekmek al.
- Not yaz: Toplantı notları, saat 14:00.
- Notları göster.
- Notlarım neler?
- Not ekle: Cuma günü proje teslimi.
- Tüm notları sil.
- Son notu göster.

## 6. Müzik Çalma
Müzik çalmak, durdurmak veya tür seçmek için:
- Müzik çal pop.
- Rock müzik çal.
- Online müzik pop çal.
- Müzik durdur.
- Şarkıyı kapat.
- Klasik müzik aç.
- Türkçe pop çal.

## 7. Haber Okuma
Güncel haberleri almak için:
- Haber oku.
- Son haberler neler?
- Haberleri söyle.
- Bugünün haberlerini oku.
- Türkiye’den haberler var mı?
- Dünya haberlerini anlat.
- Spor haberleri oku.

## 8. Matematiksel Hesaplama
Basit matematiksel işlemler için:
- Hesapla 2 artı 2.
- 3 çarpı 5 kaç eder?
- Hesapla 10 bölü 2.
- 7 eksi 4 ne yapar?
- 15’in karekökü kaç?
- 8 artı 9 eksi 2 kaç eder?
- Yüzde 20’si 50’nin ne kadar?

## 9. Fıkra Anlatma
Eğlenceli fıkralar veya espriler için:
- Fıkra anlat.
- Bana bir espri yap.
- Komik bir şeyler söyle.
- Bir fıkra daha anlat.
- En komik esprini yap.
- Karadeniz fıkrası anlat.
- Çocuk fıkrası söyler misin?

## 10. Çıkış
Asistanı kapatmak için:
- Çıkış.
- Kapat.
- Görüşürüz.
- Uygulamayı kapat.
- Bitti, çık.
- Sonlandır.
- Güle güle.

## Test İçin Örnek Komut Dizisi
Bu diziyi sırayla test ederek asistanın tüm işlevlerini kontrol edebilirsiniz:
1. "Merhaba, nasılsın?" → Sohbet başlatır.
2. "Saat kaç?" → Saati söyler.
3. "Hava durumu İstanbul" → İstanbul’un hava durumunu söyler.
4. "Not al: Yarın markete git." → Not kaydeder.
5. "Notları göster." → Kayıtlı notları listeler.
6. "Hesapla 5 artı 3." → Matematiksel hesaplama yapar.
7. "Fıkra anlat." → Bir fıkra anlatır.
8. "Haber oku." → Güncel haberleri okur.
9. "Çıkış." → Uygulamayı kapatır.

## Notlar
- Komutlar doğal dilde verilebilir, ancak net ifadeler kullanmak niyet analizini kolaylaştırır.
- Hatırlatıcılar için zaman formatı: "bugün/yarın saat" (örneğin, "Bugün 14:00 toplantı").
- Modelin yanıt kalitesini artırmak için `nlp_model.py`’deki prompt şablonlarını inceleyin.
- Hatalar için `data/logs/hata_20250525.log` dosyasını kontrol edin.
- İnternet bağlantısı, hava durumu, haber ve Wikipedia sorguları için gereklidir.
