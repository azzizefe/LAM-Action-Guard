# LAM Action Integrity Architect (Sızma Testi ve Ajan Güvenlik Mimarisi)

**Versiyon:** 1.0.0
**Yazar:** Aziz Efe Çırak
**Durum:** ✅ Tamamlandı (Production Ready)
**Kategori:** Agentic AI Security, Pentest Automation, DevSecOps

---

## 📖 Proje Özeti ve Teknik Vizyon

**LAM Action Integrity Architect**, yapay zeka ajanlarının (AI Agents) otonom eylemlerini güvence altına almak ve klasik sızma testi süreçlerini modern bir "Action Model" mimarisine dönüştürmek için tasarlanmış kapsamlı bir güvenlik platformudur.

Bu proje, sadece bir sızma testi aracı değildir; **Deterministik Olmayan (Non-Deterministic)** LLM çıktıları ile **Deterministik (Kesin)** sistem komutları arasında çalışan, gerçek zamanlı bir **"Güvenlik Katmanı" (Security Middleware)** olarak görev yapar. Ajanların veya güvenlik uzmanlarının gerçekleştireceği eylemleri "yakalar", "analiz eder" ve "güvenli bir şekilde" yürütür.

Proje, üç farklı programlama dilinin (**Python, Bash, Go**) en güçlü yönlerini birleştirerek hibrit ve yüksek performanslı bir ekosistem sunar.

---

## 🏗️ Mimari Derinlik ve Bileşenler

Sistem, monolitik bir yapı yerine, her biri kendi alanında uzmanlaşmış mikro-araçlardan oluşan modüler bir mimariye sahiptir.

### 1. The Core Brain (Python & Engine Layer)
Sistemin karar verici mekanizmasıdır.
*   **Modül:** `src/main.py` ve `src/engine/`
*   **İşlev:** CLI tabanlı yönetim, argüman işleme ve diğer alt modüllerin orkestrasyonu.
*   **Gelişmiş Tarama Motoru (`advanced_scanner.py`):**
    *   **Çoklu Vektör Analizi:** Sadece tek bir açık türüne odaklanmaz; XSS, SQL Injection, LFI (Local File Inclusion) ve RCE (Remote Code Execution) zafiyetlerini aynı anda tarar.
    *   **Pattern Matching:** `src/templates/` altındaki JSON tabanlı saldırı şablonlarını kullanarak dinamik ve genişletilebilir bir test süreci yürütür.
    *   **Zeka:** Basit string eşleşmesinin ötesinde, yanıttaki hata mesajlarını, dönen HTTP statü kodlarını ve zaman gecikmelerini (Time-Based SQLi) analiz eder.

### 2. The Speed Layer (Go & Network Layer)
Sistemin hız gerektiren operasyonları için tasarlanmıştır.
*   **Modül:** `src/port_scanner.go`
*   **Teknoloji:** Golang'in **Goroutines** ve **Channels** özelliklerini kullanır.
*   **Performans:** Saniyeler içinde binlerce portu tarayabilme kapasitesine sahiptir (Concurrent Scanning).
*   **Kullanım:** Hedef sistemin "nabzını" ölçer, erişilebilir servisleri belirler ve güvenlik testlerinin boşa gitmemesi için ön kontrol sağlar.

### 3. The Automation Layer (Bash & Unix I/O)
Sistemin işletim sistemi seviyesindeki gözü ve kulağıdır.
*   **Modül:** `src/recon_automation.sh`
*   **Felsefe:** Unix I/O prensipleri (Pipes, Streams, Redirections).
*   **Yetenekler:** 
    *   **Reconnaissance (Keşif):** Subdomain'leri bulur, canlı hostları (`httpx` mantığıyla) ayıklar.
    *   **Entegrasyon:** `curl`, `nmap` ve diğer Unix araçlarını zincirleme bağlayarak karmaşık iş akışlarını tek komuta indirger.

---

## �️ Teknik Yetenekler ve Kapsam

Platform, aşağıdaki güvenlik alanlarında aktif koruma ve test yeteneği sunar:

### A. Web Uygulama Güvenliği (Application Security)
*   **XSS (Cross-Site Scripting):** Kullanıcı oturumlarını çalabilecek script enjeksiyonlarını tespit eder.
*   **SQL Injection (SQLi):** Veritabanı sızıntısına yol açabilecek kritik sorgu hatalarını (Union-based, Boolean-based) yakalar.
*   **LFI (Local File Inclusion):** Sunucu üzerindeki hassas dosyalara (`/etc/passwd`, `boot.ini`) erişim denemelerini simüle eder.
*   **RCE (Command Injection):** İşletim sistemi seviyesinde komut çalıştırma açıklarını test eder.

### B. Altyapı Güvenliği (Infrastructure Security)
*   **Port & Servis Keşfi:** Açık kapıları ve arkasında çalışan servisleri (SSH, FTP, HTTP) tanımlar.
*   **Subdomain Haritalama:** Hedef organizasyonun dijital ayak izini çıkarır.

### C. Otonom Kontrol (Self-Governance)
*   **Self-Check Mekanizması:** Sistem her başlatıldığında kendi bütünlüğünü (`project_info.json`, bağımlılıklar, dizin yapısı) kontrol eder (`src/utils/system_check.py`).
*   **Raporlama:** İnsan müdahalesine gerek kalmadan, tüm bulguları HTML, JSON ve Markdown formatlarında raporlar.

---

## 📂 Bilgi Bankası ve Dokümantasyon

Proje, sadece koddan ibaret değildir; aynı zamanda derinlemesine bir teknik bilgi bankası içerir:

1.  **Sızma Testi Otomasyonu (`docs/sizma_testi_otomasyonu.md`):** Unix I/O, File Descriptors ve buffer stratejileri üzerine akademik düzeyde bilgi.
2.  **Dil Karşılaştırması (`docs/guvenlik_dil_karsilastirmasi.md`):** Neden Go? Neden Python? Hangi dil hangi güvenlik görevinde kullanılmalı?
3.  **İleri Teknikler (`docs/ileri_sizma_teknikleri.md`):** JSON-First parsing, stream analizi ve güvenli kodlama pratikleri.

---

## 💻 Nasıl Çalıştırılır?

Proje "Plug-and-Play" (Tak ve Çalıştır) mantığıyla tasarlanmıştır.

### 1. Kurulum
```bash
git clone https://github.com/aziz-efe/lam-action-integrity.git
pip install -r requirements.txt
# Go modülünü derle
go build -o src/port_scanner.exe src/port_scanner.go
```

### 2. Otonom Tarama Başlatma
```bash
# Tam Kapsamlı Tarama (XSS, SQLi, LFI, RCE)
python src/main.py --scan http://hedef-sistem.com --type all --advanced --report html
```

### 3. Sadece Keşif (Recon)
```bash
./src/recon_automation.sh -d hedef-sistem.com
```

### 4. Yüksek Hızlı Port Tarama
```bash
./src/port_scanner.exe -t hedef-sistem.com -top
```

---

**LAM Action Integrity Architect**, modern sızma testi süreçlerini "Ajan Tabanlı" (Agentic) bir geleceğe hazırlayan, sağlam temellere dayalı bir mühendislik çalışmasıdır.
