# İnfografik: LAM Action Integrity Architect - Araştırma Sonuçları Özeti

## Proje Vizyonu
**Büyük Eylem Modellerinin (LAM) Otonom API Etkileşimlerinde Güvenlik ve Doğrulama Altyapısı**

Bu infografik, ajan tabanlı yapay zeka (Agentic AI) sistemlerindeki güvenlik açıklarını ele alan "LAM Action Integrity Architect" projesinin araştırma sonuçlarını görselleştirmektedir.

---

### 1. Mevcut Durum ve Tehditler: Neden İhtiyaç Var?

Otonom ajanların API'lara erişimi arttıkça, geleneksel metin tabanlı LLM güvenlik duvarları yetersiz kalmaktadır. Üç ana tehdit vektörü belirlenmiştir:

* **Action Hijacking (Eylem Gaspı):** Ajanın, kullanıcının niyeti dışında kritik bir API çağrısı yapması (Örn: Para transferi, veri silme).
* **Indirect Prompt Injection (Dolaylı Enjeksiyon):** Ajanın, işlediği bir web sayfasında veya belgede gizlenmiş kötü amaçlı komutlarla manipüle edilmesi.
* **Hallucinated Parameters (Halüsinatif Parametreler):** Modelin, var olmayan veya hatalı API parametreleri uydurarak sistem istikrarını bozması.

---

### 2. Çözüm Mimarisi: Nasıl Çalışır?

Proje, bu tehditlere karşı **4 Modüllü Gerçek Zamanlı Doğrulama ve Denetim Mimarisi** önermektedir:

#### **MODÜL A: Riskli Eylem Kütüphanesi (Policy Engine)**
* **İşlevi:** "İzin verilmeyen" veya "onay gerektiren" kritik işlemleri tanımlayan kural seti.
* **Teknik Yöntem:** API uç noktaları için regex tabanlı kural eşleştirme.
* **Örnek:**
    ```
    Kural: DELETE /api/v1/users/* ==>  Eylem: BLOCK / HUMAN_APPROVAL
    ```

#### **MODÜL B: Niyet-Eylem Doğrulama (Intent-Action Alignment)**
* **İşlevi:** Kullanıcının doğal dil komutu ile LAM'ın ürettiği API çağrısı arasındaki tutarlılığı ölçen "Yargıç Model".
* **Süreç Akışı:**
    1.  **Kullanıcı:** "Son faturayı öde." (Niyet: Belirli bir ödeme)
    2.  **LAM:** `POST /transfer {amount: 5000, currency: USD}` (Eylem: Yüksek tutarlı transfer)
    3.  **Doğrulama Katmanı:** "Kullanıcının niyeti ile eylem arasındaki güven skoru düşük (%40)."
    4.  **Karar:** **İŞLEM DURDURULDU.**

#### **MODÜL C: Otonom Akış İzleme (Tracing & Audit Logs)**
* **İşlevi:** Ajanın "Düşünce Zinciri" (Chain of Thought) ve araç kullanımını anlık olarak kaydeden loglama altyapısı.
* **Amaç:** Olası ihlallerde adli analiz (Forensic Analysis) yapabilmek.
* **Veri Yapısı:** `[Zaman, Kullanıcı Girdisi, Düşünce Adımı, Seçilen Araç, API Çıktısı]`

#### **MODÜL D: Indirect Injection Koruması (Sandboxing)**
* **İşlevi:** Ajanın dış dünyadan (web, e-posta) aldığı verileri izole ederek, komut olarak algılanmasını önlemek.
* **Teknik Yöntem:** Dış verilerin "sterilize" edilmesi ve özel sınırlayıcılar kullanılarak modelin sadece "metin" olarak işlemesinin sağlanması.

---

### 3. Uygulama ve Beklenen Sonuçlar

#### **Teknoloji Yığını**
| Bileşen | Teknoloji / Araç | Kullanım Amacı |
| :--- | :--- | :--- |
| **LLM Çerçevesi** | LangChain / LangGraph | Ajan mimarisi ve araç yönetimi |
| **Korkuluklar** | NVIDIA NeMo Guardrails | Eylem sınırlandırma ve politika yönetimi |
| **İzleme** | LangSmith / Arize Phoenix | Ajan adımlarının görselleştirilmesi ve loglanması |
| **Test Ortamı** | Python & Docker | Güvenli, izole edilmiş test ortamı (Sandbox) |

#### **Beklenen Etki ve Faydalar**
* ✅ **Yüksek Güvenlik:** LAM manipülasyonuyla kritik işlem yapma riski **%90 oranında azalır**.
* ✅ **Güvenilirlik & Şeffaflık:** "Denetlenebilirlik" (Auditability) sayesinde kullanıcıların otonom sistemlere olan güveni artar.
* ✅ **Uyum:** Sistem, EU AI Act gibi gelecekteki yasal düzenlemelere uyumlu bir altyapı sunar.
