#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pickle
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.select import Select

def başlat(params):
    """Bir Firefox penceresi açar; ayarları yapar; sonuc.ysk.gov.tr sayfasına
    gider.
    
    Parametre:
        params : Parametre sözlüğü
            "seçim" : Seçim türü; "mv" veya "cb"
            "sandık türü" : "yurtiçi", "cezaevi", "gümrük", "yurtdışı"
            "dizin": Dosyaların kaydedileceği dizin.
    
    Firefox nesnesini döndürür.
    """
    # Parametre değerlerinin doğru olduğundan emin olalım.
    assert(params["seçim"] in ["mv", "cb"])
    assert(params["sandık türü"] in ["yurtiçi", "cezaevi", "gümrük", "yurtdışı"])
    
    # Dosyayı otomatik kaydetmek için profil ayarları
    profil = webdriver.FirefoxProfile()
    profil.set_preference("browser.download.folderList", 2)
    profil.set_preference("browser.download.manager.showWhenStarting", False)
    profil.set_preference("browser.download.dir", params["dizin"])
    profil.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.ms-excel")
    
    # Firefox penceresi aç ve başlangıç sayfasına git.
    # Başka tarayıcılar kullanmak için Selenium belgelerine bakın.
    ffox = webdriver.Firefox(firefox_profile=profil)
    ffox.implicitly_wait(20)
    ffox.get("https://sonuc.ysk.gov.tr")
    return ffox

def sorgulama_aç(ffox, params):
    """Açılış sayfasında uygun seçimler yaparak ilgili sandık sorgulama sayfasını açar.
    Parametrelerde belirtilen seçim türü ve sandık türünü seçer."""
    
    seçim = params["seçim"]
    sandıktürü = params["sandık türü"]
    
    # 2018 seçimlerinin radyo düğmesine tıkla.
    secimbutton_id = "j_id114:secimSorgulamaForm:j_id117:secimSecmeTable:0:secimId"
    secimbutton = ffox.find_element_by_id(secimbutton_id)
    secimbutton.click()
    sleep(1)
    # "Tamam" düğmesine tıkla
    tamambutton_id = "j_id114:secimSorgulamaForm:j_id144"
    tamambutton = ffox.find_element_by_id(tamambutton_id)
    tamambutton.click()
    
    # Sandık sonuçları sorgulaması sayfası açılmış olmalı.
    # Gerekiyorsa CB seçimleri sorgulamasının linkine tıkla.
    if seçim == "cb":
        cblink = ffox.find_element_by_link_text(
                "Cumhurbaşkanı Seçimi Sandık Sonuçları İçin Tıklayınız...")
        cblink.click()
        # Bu tıklama yeni bir pencere açar. Yeni pencereye geç, eskisini kapat.
        yeni_pencere = ffox.window_handles[1]
        ffox.close() # önceki pencereyi kapat
        ffox.switch_to_window(yeni_pencere)
    
    # "Sandık Türü" için uygun radyo düğmesinin ID değerini belirle.
    # Dikkat: MV seçimleri ve CB seçimleri için değerler farklı.
    if seçim == "mv":
        if sandıktürü == "yurtiçi":
            eid="j_id49:j_id51:j_id96:sandikTuruRadio:0"
        if sandıktürü == "cezaevi":
            eid="j_id49:j_id51:j_id96:sandikTuruRadio:1"
        if sandıktürü == "gümrük":
            eid="j_id49:j_id51:j_id96:sandikTuruRadio:2"
        if sandıktürü == "yurtdışı":
            eid="j_id49:j_id51:j_id96:sandikTuruRadio:3"
    if seçim == "cb":
        if sandıktürü == "yurtiçi":
            eid="j_id50:j_id52:j_id97:sandikTuruRadio:0"
        if sandıktürü == "cezaevi":
            eid="j_id50:j_id52:j_id97:sandikTuruRadio:1"
        if sandıktürü == "gümrük":
            eid="j_id50:j_id52:j_id97:sandikTuruRadio:2"
        if sandıktürü == "yurtdışı":
            eid="j_id50:j_id52:j_id97:sandikTuruRadio:3"
            
    sandik_türü_select = ffox.find_element_by_id(eid)
    sandik_türü_select.click()

def seçim_çevresi_seç(ffox, params, sc):
    """Uygun sorgulama sayfasında, belirtilen seçim çevresini menüden seçer.
    
    Parametreler:
        ffox : Firefox nesnesi
        params : Parametre sözlüğü
            "seçim" : Seçim türü; "mv" veya "cb"
            "sandık türü" : "yurtiçi", "cezaevi", "gümrük", "yurtdışı"
            "dizin": Dosyaların kaydedileceği dizin.
        sc : Seçim çevresi (dize)
    
    Değer döndürmez.
    
    Sandık tipine göre aynı fonksiyon ülke ve gümrük seçimi için de kullanılır.
    Öncesinde sorgulama_aç() çalıştırılmış olmalıdır.
    """
    seçim = params["seçim"]
    sandıktürü = params["sandık türü"]
    # Seçim çevresi, gümrük kapısı veya ülke seçimi yapan menünün id değeri
    if seçim == "mv":
        if sandıktürü in ["yurtiçi", "cezaevi"]:
            eid = "j_id49:j_id51:j_id111:cmbSecimCevresi"
        if sandıktürü == "yurtdışı":
            eid = "j_id49:j_id51:j_id148:cmbUlkeAdi"
        if sandıktürü == "gümrük":
            eid = "j_id49:j_id51:j_id136:cmbGumruk"
    if seçim == "cb":
        if sandıktürü in ["yurtiçi", "cezaevi"]:
            eid = "j_id50:j_id52:j_id111:cmbSecimCevresi"
        if sandıktürü == "yurtdışı":
            eid = "j_id50:j_id52:j_id148:cmbUlkeAdi"
        if sandıktürü == "gümrük":
            eid = "j_id50:j_id52:j_id136:cmbGumruk"
    sleep(1)
    secim_cevresi = ffox.find_element_by_id(eid)
    Select(secim_cevresi).select_by_visible_text(sc)

def ilçe_kurulu_seç(ffox, params, ilçe):
    """Uygun sorgulama sayfasında, belirtilen ilçe kurulunu ikinci menüden seçer.
    
    Parametreler:
        ffox : Firefox nesnesi
        params : Parametre sözlüğü
            "seçim" : Seçim türü; "mv" veya "cb"
            "sandık türü" : "yurtiçi", "cezaevi", "gümrük", "yurtdışı"
            "dizin": Dosyaların kaydedileceği dizin.
        ilçe : İlçe kurulu (dize)
    
    Değer döndürmez.
    
    Gümrük sandık türünde kullanılmaz.
    Yurtdışı sandık türünde dış temsilcilik seçer.
    Öncesinde seçim_çevresi_seç() çalıştırılmış olmalıdır.
    """
    seçim = params["seçim"]
    sandıktürü = params["sandık türü"]
    # Seçim çevresinin alt bölümlerinin menüsünün id değeri.
    # Dikkat: Gümrük kapısının alt bölümü yoktur.
    if sandıktürü == "gümrük":
        return
    if seçim == "mv":
        if sandıktürü in ["yurtiçi", "cezaevi"]:
            eid = "j_id49:j_id51:j_id123:cmbIlceSecimKurulu"
        if sandıktürü == "yurtdışı":
            eid = "j_id49:j_id51:j_id160:cmbDisTem"

    if seçim == "cb":
        if sandıktürü in ["yurtiçi", "cezaevi"]:
            eid = "j_id50:j_id52:j_id123:cmbIlceSecimKurulu"
        if sandıktürü == "yurtdışı":
            eid = "j_id50:j_id52:j_id160:cmbDisTem"

    sleep(1)
    ilçe_kurulu = ffox.find_element_by_id(eid)
    ilçe_kurulu_select = Select(ilçe_kurulu)
    ilçe_kurulu_select.select_by_visible_text(ilçe)

def dosya_indir(ffox):
    """Seçim çevresi ve ilçe kurulu belirlendikten sonra dosyayı indirir ve kaydeder.
    Parametre:
        ffox : Firefox nesnesi
    
    Öncesinde seçim_çevresi_seç() ve ilçe_kurulu_seç() çalıştırılmış olmalı.
    """
    sleep(1)
    # "Sorgula" düğmesi tıklanabilir olana kadar bekle
    xpath = "//input[@value='Sorgula']"
    sorgula_button = ffox.find_element_by_xpath(xpath)
    sorgula_button.click()
    
    sleep(2)
    # "Tabloyu Kaydet (Excel)" düğmesinin id kodu
    xpath = "//input[@value='Tabloyu Kaydet (Excel)']"
    kaydet_button = ffox.find_element_by_xpath(xpath)
    kaydet_button.click()
    
    kabul_link = ffox.find_element_by_link_text("Kabul Ediyorum")
    kabul_link.click()
    sleep(2)

def seçim_çevresi_listesi(ffox, params):
    """Uygun sorgulama ekranında ilçe kurulu menüsündeki bütün seçenekleri alır.
    
    Parametreler:
        ffox : Firefox nesnesi
        params : Parametre sözlüğü
            "seçim" : Seçim türü; "mv" veya "cb"
            "sandık türü" : "yurtiçi", "cezaevi", "gümrük", "yurtdışı"
            "dizin": Dosyaların kaydedileceği dizin.
        
    İlçe kurulu menüsündeki seçeneklerin listesini döndürür.
    
    Sandık tipine göre aynı fonksiyon ülke ve gümrük seçimi için de kullanılır.
    Öncesinde sorgulama_aç() çalıştırılmış olmalıdır.    
    """
    seçim = params["seçim"]
    sandıktürü = params["sandık türü"]
    if seçim == "mv":
        if sandıktürü in ["yurtiçi", "cezaevi"]:
            eid = "j_id49:j_id51:j_id111:cmbSecimCevresi"
        if sandıktürü == "yurtdışı":
            eid = "j_id49:j_id51:j_id148:cmbUlkeAdi"
        if sandıktürü == "gümrük":
            eid = "j_id49:j_id51:j_id136:cmbGumruk"
    if seçim == "cb":
        if sandıktürü in ["yurtiçi", "cezaevi"]:
            eid = "j_id50:j_id52:j_id111:cmbSecimCevresi"
        if sandıktürü == "yurtdışı":
            eid = "j_id50:j_id52:j_id148:cmbUlkeAdi"
        if sandıktürü == "gümrük":
            eid = "j_id50:j_id52:j_id136:cmbGumruk"

    sleep(1)
    secim_cevresi_select = Select(ffox.find_element_by_id(eid))
    secim_cevresi_liste = [opt.text for opt in secim_cevresi_select.options][1:]
    return secim_cevresi_liste

def ilçe_kurulu_listesi(ffox, params):
    """Uygun sorgulama ekranında seçim çevresi menüsündeki bütün seçenekleri alır.
    
    Parametreler:
        ffox : Firefox nesnesi
        params : Parametre sözlüğü
            "seçim" : Seçim türü; "mv" veya "cb"
            "sandık türü" : "yurtiçi", "cezaevi", "gümrük", "yurtdışı"
            "dizin": Dosyaların kaydedileceği dizin.
        
    Seçim çevresi menüsündeki seçeneklerin listesini döndürür.
    
    Gümrük sandık türünde kullanılmaz.
    Yurtdışı sandık türünde dış temsilcilik seçer.
    Öncesinde seçim_çevresi_seç() çalıştırılmış olmalıdır.
    """

    seçim = params["seçim"]
    sandıktürü = params["sandık türü"]
    if sandıktürü == "gümrük":
        return []
    if seçim == "mv":
        if sandıktürü in ["yurtiçi", "cezaevi"]:
            eid = "j_id49:j_id51:j_id123:cmbIlceSecimKurulu"
        if sandıktürü == "yurtdışı":
            eid = "j_id49:j_id51:j_id160:cmbDisTem"

    if seçim == "cb":
        if sandıktürü in ["yurtiçi", "cezaevi"]:
            eid = "j_id50:j_id52:j_id123:cmbIlceSecimKurulu"
        if sandıktürü == "yurtdışı":
            eid = "j_id50:j_id52:j_id160:cmbDisTem"

    sleep(1)
    ilçe_kurulu_select = Select(ffox.find_element_by_id(eid))
    ilçe_liste = [opt.text for opt in ilçe_kurulu_select.options][1:]
    return ilçe_liste

def sondurumyaz(il, ilçe, params):
    """İl ve ilçe dizelerinden oluşan ikiliyi diske kaydeder.
    
    Veri dosyaları için kullanılan dizine kaydeder.
    Kaldığımız yeri hatırlamak için kullanılan yardımcı fonksiyon."""
    dizin = params["dizin"]
    with open(dizin+"/son_il_ilce","wb") as f:
        pickle.dump((il,ilçe), f)
    
def sondurumoku(params):
    """İl ve ilçe dizelerinden oluşan ikiliyi diskten okur.
    
    Kaldığımız yeri hatırlamak için kullanılan yardımcı fonksiyon."""

    dizin = params["dizin"]
    try:
        with open(dizin+"/son_il_ilce","rb") as f:
            son_il, son_ilçe = pickle.load(f)
    except FileNotFoundError:
        # Dosya mevcut değilse yeni başlıyoruz demektir; boş dize olarak al.
        son_il, son_ilçe = "",""
    return son_il, son_ilçe

def bütün_sonuçları_al(ffox, params):
    """Otomatik sorgulamayla, belli seçim türü ve sandık tipindeki bütün dosyaları sırayla alır.
    
    Parametreler:
        ffox : Firefox nesnesi
        params : Parametre sözlüğü
            "seçim" : Seçim türü; "mv" veya "cb"
            "sandık türü" : "yurtiçi", "cezaevi", "gümrük", "yurtdışı"
            "dizin": Dosyaların kaydedileceği dizin.

    Değer döndürmez.
     
    Parametrelerde belirtilen seçim türü ve sandık tipiyle çalışır.
    Öncesinde sorgulama_aç() çalıştırılmış olmalıdır.
    Her dosyayı indirdikten sonra kalınan yer kaydedilir. Durdurulup yeniden
    başlatıldığında kaldığı yerin bir sonrasından devam eder."""

    sandıktürü = params["sandık türü"]
    if sandıktürü == "gümrük":
        # Hangi gümrükte kaldık?
        son_gümrük = sondurumoku(params)[0]  # Boş string "" en başta olduğumuzu gösterir.
        gümrükliste = seçim_çevresi_listesi(ffox, params)
        baş = gümrükliste.index(son_gümrük)+1 if son_gümrük else 0
        for gümrük in gümrükliste[baş:]:
            seçim_çevresi_seç(ffox, params, gümrük)
            dosya_indir(ffox)
            print(gümrük)
            # Son işlenen gümrüğü kaydet.
            sondurumyaz(gümrük,"",params)
    else:
        # Hangi seçim çevresinde (il/ülke) ve hangi ilçede (seçim kurulu/elçilik) kaldık?
        son_il, son_ilçe = sondurumoku(params) # Boş string "" en başta olduğumuzu gösterir.
        scliste = seçim_çevresi_listesi(ffox, params)
        baş = scliste.index(son_il) if son_il != "" else 0
        
        for il in scliste[baş:]:
            seçim_çevresi_seç(ffox, params, il)
            ilçeliste = ilçe_kurulu_listesi(ffox, params)
            ilçe_baş = 0
            if son_ilçe in ilçeliste:
                ilçe_baş = ilçeliste.index(son_ilçe)+1
            
            for ilçe in ilçeliste[ilçe_baş:]:
                ilçe_kurulu_seç(ffox, params, ilçe)
                dosya_indir(ffox)
                print(il, ilçe)
                sondurumyaz(il, ilçe,params)

if __name__ == "__main__":
    parametreler = {
            "seçim":"cb",
            "sandık türü": "cezaevi",
            "dizin":"/home/kaan/work/secim2018v2/cbcezaevi"}
    ffox = başlat(parametreler)
    sorgulama_aç(ffox, parametreler)
    
    say = 0
    for sc in seçim_çevresi_listesi(ffox, parametreler):
        seçim_çevresi_seç(ffox, parametreler, sc)
        say += len(ilçe_kurulu_listesi(ffox, parametreler))
    
    print(say)
#    try:
#        bütün_sonuçları_al(ffox, parametreler)
#    except:
#        sonil, sonilçe = sondurumoku(parametreler)
#        print("Bağlantı sorunu! Son kaydedilen: ",sonil, sonilçe)
    ffox.close()
