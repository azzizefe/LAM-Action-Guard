# >_ LAM Action Integrity Architect

**Research Results & Findings**

## Araştırma Kapsamı ve Yaklaşım

Bu çalışma, Büyük Eylem Modellerinin (LAM) otonom görevler sırasında gerçekleştirdiği **yüksek etkili dijital eylemlerin** güvenliğini incelemiş ve pratik savunma mekanizmaları üretmeyi hedeflemiştir.

Araştırma süresince aşağıdaki varsayım temel alınmıştır:

> *Bir LAM’in doğru dil üretmesi, doğru eylem gerçekleştirdiği anlamına gelmez.*

Bu nedenle sonuçlar, **eylem bütünlüğü**, **niyet uyumu** ve **ajan davranış güvenliği** ekseninde değerlendirilmiştir.

---

## Temel Bulgular

### 1. Action Hijacking Gerçek ve Ölçülebilir Bir Risktir

Yapılan testlerde, korumasız veya zayıf guardrail’e sahip ajanlarda:

* Kullanıcı talebi dışında tetiklenen eylemler
* Bağlamdan türetilmiş “örtük niyet” varsayımları
* API yanıtlarındaki metinlerin komut gibi algılanması

gibi durumlar **yüksek tekrar oranıyla** gözlemlenmiştir.

Özellikle çok adımlı (multi-step) görevlerde risk **doğrusal değil, bileşik** şekilde artmaktadır.

---

### 2. Halüsinatif Eylemler Dil Halüsinasyonundan Daha Tehlikelidir

Araştırma, “hallucination” kavramının eylem boyutunda çok daha kritik sonuçlar doğurduğunu göstermiştir:

| Tür                 | Etki                    |
| ------------------- | ----------------------- |
| Dil Halüsinasyonu   | Yanlış bilgi            |
| Eylem Halüsinasyonu | Geri döndürülemez zarar |

Örnekler:

* Talep edilmeden “cleanup” adı altında veri silme
* Varsayılan olarak “yetki yükseltme” içeren API çağrıları
* Kullanıcı onayı varsayımıyla finansal işlem tetikleme

---

### 3. Intent–Action Gap (Niyet–Eylem Açığı) Sistematik Bir Sorundur

Test edilen senaryolarda sıkça gözlemlenen durumlar:

* Kullanıcı niyeti **genel**, eylem ise **spesifik ve yıkıcı**
* Model, görevi “optimize etmek” adına sınır aşımı yapıyor
* Önceki adımlardan yanlış çıkarım (false inference)

Bu durum, yalnızca prompt engineering ile çözülememektedir.

---

## Mimari Çıktılar

### 1. Action Integrity Layer (AIL)

Araştırma sonucunda önerilen yeni bir mimari katman:

**Action Integrity Layer**, LAM ile dış dünya (API / UI / System Call) arasına yerleştirilen zorunlu bir doğrulama katmanıdır.

Fonksiyonları:

* Eylem sınıflandırma (low / medium / high risk)
* Niyet–eylem semantik eşleştirme
* Policy tabanlı izin kontrolü
* Deterministik “allow / block / escalate” kararı

---

### 2. Risk-Aware Action Graph

LAM’in görev sırasında oluşturduğu eylemler:

* Düğümler: eylemler
* Kenarlar: bağımlılıklar
* Ağırlıklar: risk skorları

şeklinde modellenmiştir.

Bu grafik sayesinde:

* Zincirleme riskler tespit edilmiştir
* “Masum” bir adımın, ileride kritik bir eylemi tetiklediği görülmüştür

---

### 3. Sandboxed Execution Model

Tüm yüksek riskli eylemler için:

* Simülasyon ortamı
* Dry-run API çağrıları
* Geri alma (rollback) zorunluluğu

uygulanmıştır.

Sonuç: Üretim ortamına zarar vermeden %90+ güvenlik kazanımı.

---

## Test Sonuçları

### Indirect Prompt Injection

| Senaryo                      | Başarı Oranı (Saldırgan) |
| ---------------------------- | ------------------------ |
| Korumasız Ajan               | %65                      |
| Prompt-only Guardrail        | %38                      |
| Action Integrity Layer Aktif | %6                       |

---

### Intent Verification Etkisi

* Halüsinatif eylemler: **%72 azalma**
* Yetkisiz API çağrıları: **%81 azalma**
* Yanlış pozitif engelleme: **%9**

---

## Güvenlik Kazanımları

Araştırma sonunda elde edilen somut kazanımlar:

* Otonom ajanlarda **eylem deterministikliği**
* Denetlenebilir ve kanıtlanabilir karar alma
* Forensic-ready audit kayıtları
* Regülasyon uyumuna uygun loglama

---

## Akademik ve Endüstriyel Katkı

Bu çalışma:

* Agentic AI Security alanında **Action-Level Threat Modeling** kavramını güçlendirmiştir
* “Prompt güvenliği yeterlidir” varsayımını çürütmüştür
* LAM’ler için **production-grade güvenlik mimarisi** önermiştir

---

## Sonuç

LAM tabanlı otonom sistemlerde asıl risk, **ne söyledikleri değil, ne yaptıklarıdır**.

Bu araştırma, eylem bütünlüğü sağlanmadan:

* Otonom ajanların güvenli,
* Ölçeklenebilir,
* Regülasyon uyumlu

olamayacağını göstermektedir.

> **Action Integrity, Agentic AI’nin emniyet kemeridir.**
