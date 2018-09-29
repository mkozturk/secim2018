# secim2018
24 Haziran 2018 seçimlerinin sandık sonuçlarını sonuc.ysk.gov.tr sayfasından otomatik olarak indiren bir program.

Python ve Selenium kullanır. Başka seçim sonuçlarına ulaşmak için kaynak kodunun sorgulama sayfası ayrıntılarına göre değiştirilmesi gerekir.

Temel kullanım:

```python
import secim2018

# Parametreler
parametreler = {
  "seçim" : "cb",  # "mv" veya "cb"
  "sandık türü" : "yurtiçi",  # "yurtiçi", "yurtdışı", "gümrük" veya "cezaevi"
  "dizin" : "secim2018/cbyurtiçi"  # dosyaların kaydedileceği dizin
  }  
 
 ffox = secim2018.başlat(parametreler)  # Firefox penceresi açar, ana sayfaya gider.
 secim2018.sorgulama_aç(ffox, parametreler) # Seçim ve sandık türüne göre sorgulama sayfasını hazırlar.
 
 # Tek bir dosyayı indirmek için
 secim2018.seçim_çevresi_seç(ffox, parametreler, "ADANA")
 secim2018.ilçe_kurulu_seç(ffox, parametreler, "ALADAĞ")
 secim2018.dosya_indir(ffox)
 
 # Bütün dosyaları sırayla indirmek için
 secim2018.bütün_sonuçları_al(ffox, parametreler)
  ```
