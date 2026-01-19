# research.gemini-pro.sources.md

## Proje: LAM Action Integrity Architect - Kaynak Araştırması

Bu belge, Büyük Eylem Modellerinin (LAM) güvenliği, otonom ajanların (Autonomous Agents) riskleri ve doğrulama mekanizmaları üzerine yapılan teknik araştırmaları ve endüstri standartlarını içerir.

### 1. Endüstri Standartları ve Çerçeveler (Industry Standards & Frameworks)

* **OWASP Top 10 for Large Language Model Applications (Sürüm 1.1)**
    * *İlgili Bölümler:* LLM01: Prompt Injection, LLM02: Insecure Output Handling, LLM05: Supply Chain Vulnerabilities.
    * *Proje Bağlamı:* "Riskli Eylem Kütüphanesi" oluşturulurken referans alınacak temel güvenlik açıklarını tanımlar. Özellikle "Action Hijacking" senaryoları için LLM01 ve LLM02 kritiktir.
    * *URL:* https://owasp.org/www-project-top-10-for-large-language-model-applications/

* **NIST AI Risk Management Framework (AI RMF 1.0)**
    * *İlgili Bölümler:* Map, Measure, Manage functions for AI safety.
    * *Proje Bağlamı:* "Niyet-Eylem Doğrulama" (Intent Verification) süreçlerinin standartlara uygun olarak nasıl yönetileceğini belirler.
    * *URL:* https://www.nist.gov/itl/ai-risk-management-framework

### 2. Akademik Makaleler ve Teknik Raporlar (Academic Papers & Technical Reports)

* **"More than you've asked for: A Comprehensive Analysis of Novel Prompt Injection Threats to Application-Integrated Large Language Models"**
    * *Yazarlar:* Greshake, K., et al. (2023)
    * *Proje Bağlamı:* "Indirect Injection Testleri" için temel kaynaktır. Web sitelerine gizlenmiş komutlarla ajanların nasıl manipüle edildiğini (Indirect Prompt Injection) teknik olarak açıklar.
    * *Kaynak:* arXiv:2302.12173

* **"ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs"**
    * *Yazarlar:* Qin, Y., et al. (2023)
    * *Proje Bağlamı:* LAM'lerin API'ları nasıl kullandığını ve "Otonom Akış İzleme" (Tracing) sırasında nelere dikkat edilmesi gerektiğini anlamak için ajanların araç kullanım (tool-use) mantığını inceler.
    * *Kaynak:* arXiv:2307.16789

* **"Jailbroken: How Does LLM Safety Training Fail?"**
    * *Yazarlar:* Wei, A., et al. (2023)
    * *Proje Bağlamı:* Modelin güvenlik sınırlarını aşarak "Riskli Eylemleri" gerçekleştirmesine neden olan manipülasyon tekniklerini analiz eder.
    * *Kaynak:* arXiv:2307.02483

### 3. Teknik Dokümantasyon ve Araçlar (Technical Docs & Tools)

* **NVIDIA NeMo Guardrails Documentation**
    * *Kategori:* Action Guardrails & Sandboxing
    * *Proje Bağlamı:* "Action Guardrails" geliştirmek için kullanılan programlanabilir korkuluk sistemidir. `Colang` kullanarak belirli eylemlerin nasıl engelleneceği konusunda teknik referanstır.
    * *URL:* https://github.com/NVIDIA/NeMo-Guardrails

* **LangChain Security & LangSmith Documentation**
    * *Kategori:* Tracing & Audit
    * *Proje Bağlamı:* "Otonom Akış İzleme" (Tracing) kısmında, ajanın adım adım (Chain of Thought) ne yaptığını izlemek için kullanılan modern mimariyi ve `human-in-the-loop` (insan onaylı işlem) mekanizmalarını açıklar.
    * *URL:* https://python.langchain.com/docs/security/

* **Microsoft Security: "Guidance for securing Large Language Model (LLM) agents"**
    * *Kategori:* Agent Security
    * *Proje Bağlamı:* Ajanların yetkilerinin sınırlandırılması ve "Least Privilege" (En Az Yetki) prensibinin otonom sistemlere uygulanması.
    * *URL:* https://learn.microsoft.com/en-us/security/engineering/securing-llm-agents

### 4. Saldırı Vektörleri ve Kavramlar (Attack Vectors & Concepts)

* **Confused Deputy Problem in AI Agents**
    * *Açıklama:* Bir ajanın, kullanıcının yetkilerini kullanarak (kullanıcının niyeti dışında) saldırganın istediği işlemi yapması durumu.
    * *Proje Bağlamı:* Projenin ana amacı olan "Action Hijacking" (Eylem Gaspı) riskinin teknik literatürdeki karşılığıdır.

* **Hallucinated Function Calls**
    * *Açıklama:* Modelin, var olmayan bir API parametresi uydurması veya yanlış bir fonksiyonu çağırması.
    * *Proje Bağlamı:* "Halüsinatif Eylemleri Engelleme" modülü için temel problem tanımıdır.
