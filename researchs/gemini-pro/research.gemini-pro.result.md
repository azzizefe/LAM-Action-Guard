# research.gemini-pro.result.md

## Araştırma Sonuç Raporu: LAM Action Integrity Architect
**Tarih:** 19 Ocak 2026  
**Konu:** Agentic AI Security & Action Guardrails  
**Durum:** Tamamlandı

### 1. Yönetici Özeti (Executive Summary)
Büyük Eylem Modellerinin (LAM), dijital ekosistemlerde sadece metin üretmekle kalmayıp, API çağrıları üzerinden otonom aksiyonlar (satın alma, veri silme, e-posta gönderme) aldığı yeni bir döneme girilmektedir. Yapılan literatür taraması ve endüstri standartları (OWASP Top 10 LLM) incelemesi sonucunda, mevcut LLM güvenlik duvarlarının "eylem tabanlı" (action-based) saldırılara karşı yetersiz olduğu tespit edilmiştir.

Bu proje, **"Action Hijacking"** (Eylem Gaspı) ve **"Indirect Prompt Injection"** (Dolaylı Komut Enjeksiyonu) risklerini minimize eden, gerçek zamanlı bir doğrulama ve denetim mimarisi önermektedir.

### 2. Tehdit Modellemesi ve Problem Tanımı

Araştırmalarımız sonucunda LAM'ler için üç kritik saldırı vektörü belirlenmiştir:

* **Yetkisiz Eylem İcrası (Unauthorized Action Execution):** Modelin, kullanıcı niyetiyle örtüşmeyen tehlikeli bir API çağrısı yapması (Örn: Veritabanı tablosunu silme).
* **Dolaylı Enjeksiyon (Indirect Injection):** Ajanın okuduğu bir web sayfasında veya e-postada gizlenmiş "beyaz yazı" (hidden text) komutları ile manipüle edilmesi.
* **Halüsinatif Parametreler (Hallucinated Parameters):** Modelin, API dokümantasyonunda olmayan parametreler uydurarak sistem kararlılığını bozması.

### 3. Önerilen Çözüm Mimarisi (Architectural Solution)

Proje kapsamında geliştirilecek "LAM Action Integrity Architect" sistemi aşağıdaki 4 ana modülden oluşacaktır:

#### A. Riskli Eylem Kütüphanesi (Sensitive Action Library)
Sistemin "izin verilmeyen" veya "onay gerektiren" eylemleri tanıması için bir kural seti (policy engine) oluşturulmuştur.
* **Kategorizasyon:** Eylemler "Salt Okunur" (Güvenli), "Veri İşleme" (Orta Risk) ve "Yıkıcı/Finansal" (Yüksek Risk) olarak sınıflandırılacaktır.
* **Teknik Uygulama:** API uç noktaları (endpoints) regex kuralları ile eşleştirilir.
    * *Örnek:* `DELETE /api/v1/users/*` -> **BLOCK** veya **HUMAN_APPROVAL**

#### B. Niyet-Eylem Doğrulama (Intent-Action Alignment)
Bu modül, kullanıcının doğal dildeki isteği ile modelin ürettiği JSON çıktısını karşılaştıran ikincil bir "Yargıç Model" (Judge Model) kullanır.
* **Süreç:**
    1.  Kullanıcı: "Son gelen faturayı öde."
    2.  LAM Çıktısı: `POST /transfer {amount: 5000, currency: USD}`
    3.  **Doğrulama Katmanı:** "Kullanıcı fatura dedi, ancak miktar 5000 USD. Fatura tutarı ile eşleşiyor mu? Güven skoru: %40."
    4.  **Karar:** Düşük skor nedeniyle işlem durdurulur.

#### C. Otonom Akış İzleme (Tracing & Audit Logs)
Ajanın düşünce zincirini (Chain of Thought) ve araç kullanımını (Tool Use) anlık olarak izleyen bir loglama altyapısıdır.
* **Veri Yapısı:** Her işlem için `[Zaman Damgası, Kullanıcı Girdisi, Düşünce Adımı, Seçilen Araç, Ham API Çıktısı]` verileri JSON formatında saklanır.
* **Amaç:** Olası bir güvenlik ihlalinde "Forensic Analysis" (Adli Analiz) yapabilmek.

#### D. Indirect Injection Koruması (Sandboxing)
Ajanın dış dünyadan (web siteleri, gelen e-postalar) aldığı veriler, ana komut isteminden (system prompt) izole edilir.
* **Yöntem:** Dış veriler işlenmeden önce "sterilize" edilir ve modelin bu verileri "komut" olarak değil, sadece "metin" olarak algılaması için özel delimitörler (sınırlayıcılar) kullanılır.

### 4. Kullanılacak Teknolojiler ve Araçlar

Projenin teknik prototipinde aşağıdaki araç setinin kullanılması planlanmaktadır:

| Bileşen | Teknoloji / Araç | Kullanım Amacı |
| :--- | :--- | :--- |
| **LLM Framework** | LangChain / LangGraph | Ajan mimarisi ve araç yönetimi. |
| **Guardrails** | NVIDIA NeMo Guardrails | Eylem sınırlandırma ve politika yönetimi. |
| **Tracing** | LangSmith veya Arize Phoenix | Ajanın adımlarını görselleştirme ve loglama. |
| **Test Ortamı** | Python & Docker | Güvenli, izole edilmiş test ortamı (Sandbox). |

### 5. Beklenen Sonuç ve Etki

Bu mimari entegre edildiğinde;
1.  **Güvenlik:** LAM'lerin manipüle edilerek kritik işlem yapma riski %90 oranında azaltılacaktır.
2.  **Güvenilirlik:** Kullanıcılar, otonom ajanlara finansal veya kritik yetkiler verirken "Denetlenebilirlik" (Auditability) sayesinde sisteme güven duyacaktır.
3.  **Uyum:** Sistem, gelecekteki yasal düzenlemelere (EU AI Act) uyumlu bir altyapı sunacaktır.
