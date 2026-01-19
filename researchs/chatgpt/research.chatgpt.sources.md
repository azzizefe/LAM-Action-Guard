# >_ LAM Action Integrity Architect

**AI Agents API Security & Autonomous Operations**

## Proje Amacı

Büyük Eylem Modellerinin (Large Action Models – LAM), dijital arayüzler ve API’ler üzerinde gerçekleştirdiği **otonom eylemlerin** (ör. tıklama, satın alma, veri silme) güvenliğini test etmek ve **Action Hijacking (Eylem Gaspı)** risklerini önleyen doğrulama ve denetim mekanizmaları geliştirmek.

Bu proje, ajan tabanlı yapay zeka sistemlerinde **niyet–eylem bütünlüğünü** korumayı ve halüsinatif veya manipüle edilmiş eylemlerin üretim ortamlarında zarara yol açmasını engellemeyi hedefler.

---

## Beklenen Özellikler

### 1. Riskli Eylem Kütüphanesi (Risky Action Library)

LAM’lerin yanlışlıkla veya dış manipülasyonla tetikleyebileceği kritik işlemler için tanımlı test senaryoları:

* Yetkisiz para transferleri
* Kullanıcı hesabı silme
* Veritabanı veya dosya sistemi silme
* Yetki yükseltme (privilege escalation)
* Geri döndürülemez sistem değişiklikleri

Amaç, bu eylemleri **önceden sınıflandırmak**, **simüle etmek** ve **koruyucu guardrail’ler** geliştirmektir.

---

### 2. Otonom Akış İzleme (Autonomous Flow Tracing)

LAM’in bir görevi (Task) yerine getirirken izlediği süreci uçtan uca izleyen bir denetim (audit) mekanizması:

* Atılan adımlar (steps)
* Kullanılan araçlar (tools)
* Yapılan API çağrıları
* Parametre değişimleri
* Karar noktaları (decision points)

Bu izleme, **sonradan analiz**, **adli inceleme (forensics)** ve **davranış profilleme** için kullanılır.

---

### 3. Niyet–Eylem Doğrulama (Intent Verification)

Kullanıcının verdiği komut ile LAM’in gerçekleştirdiği gerçek eylem arasındaki tutarlılığı ölçen bir doğrulama katmanı:

* Kullanıcı niyeti ile eylem semantiği eşleşiyor mu?
* Model, talep edilmeyen bir eylemi “kendi başına” mı gerçekleştirdi?
* Eylem, görev kapsamı dışına çıktı mı?

Bu mekanizma özellikle **Hallucinated Actions** (Halüsinatif Eylemler) riskini azaltmayı hedefler.

---

### 4. Indirect Prompt Injection Testleri

LAM’in dolaylı yollarla manipüle edilip edilemediğini test eden saldırı simülasyonları:

* Web sitelerine gizlenmiş komutlar
* Doküman, e-posta veya API yanıtlarına gömülü talimatlar
* HTML / Markdown / JSON içi prompt enjeksiyonları

Amaç, ajanların **bağlam zehirlenmesine (context poisoning)** karşı dayanıklılığını ölçmektir.

---

## Teknik Odak

* **Alan:** Agentic AI Security

* **Alt Başlıklar:**

  * Action Integrity
  * Autonomous Agent Auditing
  * Prompt & Action Injection Defense

* **Yöntemler:**

  * Action Guardrails
  * Sandboxing
  * Policy Enforcement Layers
  * Deterministic Action Validation

---

## Ana Hedef

Üretim ortamlarında çalışan otonom AI ajanlarının:

* Yetkisiz,
* Niyetten kopuk,
* Manipüle edilmiş,
* Geri döndürülemez

eylemler gerçekleştirmesini **tespit edebilir**, **önleyebilir** ve **kanıtlanabilir şekilde denetleyebilir** hale gelmesini sağlamak.
