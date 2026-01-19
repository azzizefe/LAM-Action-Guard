# LAM Action Integrity Architect: Teknik Derinlemesine Analiz Raporu

**Hazırlayan:** Aziz Efe Çırak  
**Tarih:** 19 Ocak 2026  
**Kapsam:** Agentic AI Güvenliği, LAM Mimarisi ve Otonom Koruma Sistemleri

Bu rapor, "LAM Action Integrity Architect" projesinin teknik altyapısını, endüstriyel konumunu ve güvenlik kritiklerini 5 ana başlık altında detaylandırmaktadır.

---

## 1. Temel Çalışma Prensipleri (Core Working Principles)

Bu teknolojinin merkezinde, **Deterministik Olmayan (Non-Deterministic)** LLM çıktıları ile **Deterministik (Kesin)** API uç noktaları arasında bir "Güvenlik Katmanı" (Security Middleware) oluşturmak yatar. Sistem 3 ana fazda çalışır:

### A. Algılama ve Yakalama (Interception Phase)
Geleneksel web güvenliğinin aksine, burada tehdit "dışarıdan içeriye" (gelen trafik) değil, "içeriden dışarıya" (ajanın ürettiği eylem) yöneliktir.
1.  **Kullanıcı Girdisi:** Kullanıcı doğal dilde bir komut verir.
2.  **LLM İşlemesi:** Ajan (Agent), bu komutu analiz eder ve bir "Araç Çağrısı" (Tool Call) üretir.
3.  **Kanca (Hook):** Sistem, bu çağrı API'ye gitmeden *önce* araya girer (Interception).

### B. Anlamsal ve Kural Tabanlı Doğrulama (Hybrid Verification)
Sistem iki farklı doğrulama motorunu paralel çalıştırır:
* **Statik Analiz (Static Analysis):** Regex ve ön tanımlı listeler (Allow/Block Lists) kullanılarak, çağrılan fonksiyonun kritiklik seviyesi kontrol edilir (Örn: `delete_database` fonksiyonu yasaklı mı?).
* **Semantik Analiz (Semantic Analysis):** İkincil bir "Yargıç Model" (Judge Model), kullanıcının *niyeti* ile ajanın ürettiği *eylemi* vektörel uzayda karşılaştırır.
    * *Prensip:* $Sim(Intent, Action) > Threshold$

### C. Karar ve Yürütme (Decision & Execution)
* **Pass:** Güvenlik skoru eşiğin üzerindeyse işlem API'ye iletilir.
* **Block:** İşlem reddedilir ve kullanıcıya güvenlik uyarısı verilir.
* **Human-in-the-Loop (HITL):** Risk skoru "Orta" seviyedeyse, işlem beklemeye alınır ve yetkili bir insandan onay istenir.

---

## 2. En İyi Uygulama Yöntemleri ve Endüstri Standartları (Best Practices & Standards)

Agentic AI güvenliği için kabul görmüş global standartlar şunlardır:

### Endüstri Standartları
* **OWASP Top 10 for LLM Applications (2025 v1.1):**
    * **LLM01 (Prompt Injection):** Sistemin, gizli talimatlarla manipüle edilmesini önlemek için "Girdi Sterilizasyonu" şarttır.
    * **LLM02 (Insecure Output Handling):** Ajanın ürettiği çıktıların, arka uç sistemlerde (Backend) doğrudan çalıştırılmaması, mutlaka bir doğrulama katmanından geçmesi gerekir.
    * **LLM05 (Supply Chain Vulnerabilities):** Kullanılan üçüncü parti ajan kütüphanelerinin (LangChain, AutoGPT vb.) güncel olması.

* **NIST AI Risk Management Framework (AI RMF 1.0):**
    * **Map:** Ajanın erişebileceği tüm API uç noktalarının haritalanması.
    * **Measure:** Halüsinasyon oranlarının ve hatalı eylem sıklığının metriklerle ölçülmesi.
    * **Manage:** Riskli eylemler için otomatik durdurma mekanizmalarının (Kill Switch) devreye alınması.

### Best Practices (En İyi Uygulamalar)
1.  **Least Privilege (En Az Yetki Prensibi):** Ajanlara asla "Admin" veya "Root" yetkisi verilmemelidir. Ajanın API token'ı sadece görevi için gerekli minimum endpoint'lere (örneğin sadece `read_email`, `send_email` değil) erişebilmelidir.
2.  **Sandboxing (Kum Havuzu):** Ajanın çalıştırdığı kodlar (özellikle Python Code Interpreter kullanıyorsa) izole edilmiş Docker konteynerlerinde çalıştırılmalıdır.
3.  **Dual-LLM Pattern:** Doğrulama yapan model ile eylemi üreten model farklı olmalıdır. (Örn: Eylem için GPT-4, Doğrulama için Claude 3 Opus veya özel eğitilmiş küçük bir model).

---

## 3. Benzer Açık Kaynak Projeler ve Rakipler (Competitors & Ecosystem)

Bu proje, hızla büyüyen "AI Security" pazarında yer almaktadır. Mevcut rakipler ve benzer projeler:

| Proje / Ürün | Tür | Odak Noktası | Farkımız (USP) |
| :--- | :--- | :--- | :--- |
| **NVIDIA NeMo Guardrails** | Open Source | Diyalog yönetimi ve konu sınırlaması (Topical Guardrails). | Biz "Eylem" (Action) bütünlüğüne ve API güvenliğine odaklanıyoruz. |
| **Guardrails AI** | Open Source | Pydantic tabanlı yapısal veri doğrulama (XML/JSON validasyonu). | Biz anlamsal (semantic) niyet doğrulaması yapıyoruz. |
| **Lakera Guard** | Ticari (SaaS) | Prompt Injection tespiti üzerine uzmanlaşmış API. | Biz sadece girdiyi değil, *çıktıdaki eylemi* de denetliyoruz. |
| **Rebuff** | Open Source | Çok katmanlı Prompt Injection koruması. | Biz "Agentic" iş akışlarına (Tools/Functions) özel mimari sunuyoruz. |
| **LangSmith (LangChain)** | Platform | Trace ve Debugging. | Biz bir izleme aracı değil, aktif bir "Engelleme" (Prevention) sistemiyiz. |

---

## 4. Kritik Yapılandırma Dosyaları ve Parametreleri

Projenin kalbi, kuralların tanımlandığı yapılandırma dosyalarıdır. Aşağıda örnek bir yapılandırma mimarisi sunulmuştur:

### A. `security_policy.yaml` (Ana Politika Dosyası)
Sistemin genel davranışını belirleyen dosya.

```yaml
system_config:
  mode: "strict" # options: strict, monitor_only, hybrid
  risk_threshold: 0.85 # 0.0 - 1.0 arası (Daha düşük skorlar engellenir)
  max_retries: 2 # Hatalı eylemde ajana kaç kez düzeltme şansı verileceği

action_groups:
  financial:
    risk_level: "high"
    requires_human_approval: true
    allowed_endpoints: ["/api/v1/transfer", "/api/v1/pay"]
  
  informational:
    risk_level: "low"
    requires_human_approval: false
    allowed_endpoints: ["/api/v1/balance", "/api/v1/transactions"]
