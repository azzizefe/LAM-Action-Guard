# LAM-Action-Guard Sistem Mimarisi

Bu belge, sistemin yüksek seviyeli mimarisini ve bileşenler arası etkileşimi açıklar.

## Genel Bakış

Sistem, modüler bir yapı üzerine inşa edilmiştir. Ana kontrolcü (`main.py`), kullanıcı girdilerini alır ve ilgili alt modüllere (Scanner, Automation Scripts) yönlendirir.

## Bileşenler

### 1. Core Engine (Çekirdek)
*   **Görevi:** İş akışını yönetmek, konfigürasyonu yüklemek ve modülleri başlatmak.
*   **Dosya:** `src/main.py`

### 2. Security Scanner (Tarama Motoru)
*   **Görevi:** Hedef sistem üzerinde güvenlik testleri gerçekleştirmek.
*   **Girdiler:** Şablon dosyaları (`src/templates/*.json`), Hedef URL.
*   **Dosya:** `src/engine/scanner.py`

### 3. Automation Layer (Otomasyon Katmanı)
*   **Görevi:** Veri toplama ve sistem kontrolü.
*   **Bileşenler:**
    *   `src/scripts/bash_automation.sh` (Bash tabanlı veri işleme)
    *   `src/utils/system_check.py` (Self-Check mekanizması)

## Veri Akışı

1.  **Kullanıcı** CLI üzerinden komut verir.
2.  **Main Controller** komutu işler ve config'i yükler.
3.  Eğer **Security Scan** istenmişse:
    *   Scanner başlatılır.
    *   Templates klasöründen `xss` veya `sqli` desenleri yüklenir.
    *   Hedefe istekler gönderilir ve yanıtlar analiz edilir.
4.  Sonuçlar raporlanır (JSON/Console).
