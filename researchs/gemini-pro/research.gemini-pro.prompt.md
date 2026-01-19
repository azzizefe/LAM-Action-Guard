
# research.gemini-fast.prompt.md

## Araştırma Süreci ve Kullanılan Promptlar
**Proje:** LAM Action Integrity Architect  
**Model:** Gemini 1.5 Pro / Flash  

Bu belge, "Large Action Models" (LAM) güvenliği üzerine yapılan araştırma sırasında kullanılan yapılandırılmış sorguları (promptları) içerir.

### Aşama 1: Literatür Taraması ve Kavramsal Çerçeve
*Amaç: Temel kavramları, riskleri ve mevcut literatürü belirlemek.*

> **Prompt 1:**
> "Büyük Eylem Modelleri (Large Action Models - LAM) ve Ajan Tabanlı Yapay Zeka (Agentic AI) sistemlerinde görülen temel güvenlik risklerini analiz et. Özellikle 'Action Hijacking', 'Indirect Prompt Injection' ve 'Hallucinated Actions' kavramlarını teknik detaylarıyla açıkla. Bu konuda OWASP veya NIST tarafından yayınlanmış güncel standartlar var mı?"

> **Prompt 2:**
> "LLM'lerin web siteleri veya e-postalar üzerinden gelen gizli komutlarla (hidden prompts) manipüle edilmesini konu alan akademik makaleleri listele. Özellikle 'Indirect Injection' saldırıları ve buna karşı önerilen savunma mekanizmaları (sandboxing, human-in-the-loop) hakkında bilgi ver."

### Aşama 2: Teknik Çözüm ve Araç Araştırması
*Amaç: Teorik risklere karşı pratik, uygulanabilir teknolojiler bulmak.*

> **Prompt 3:**
> "Otonom yapay zeka ajanlarının (AI Agents) API çağrılarını denetlemek ve kısıtlamak için kullanılan 'Guardrails' teknolojilerini araştır. NVIDIA NeMo Guardrails ve LangChain Security modüllerinin 'Action Integrity' (Eylem Bütünlüğü) sağlamak için nasıl yapılandırıldığını, kod örnekleri veya mimari şemalar üzerinden açıkla."

> **Prompt 4:**
> "Bir yapay zeka ajanının, kullanıcının asıl niyeti (Intent) ile gerçekleştirmek üzere olduğu eylem (Action) arasındaki tutarlılığı ölçen bir 'Doğrulama Mekanizması' (Intent-Action Verification) nasıl tasarlanır? Bu sistemde 'Least Privilege' (En Az Yetki) prensibi nasıl uygulanır?"

### Aşama 3: Sentez ve Raporlama
*Amaç: Toplanan bilgileri bir proje önerisine dönüştürmek.*

> **Prompt 5:**
> "Yukarıdaki araştırmalara dayanarak, 'LAM Action Integrity Architect' adlı bir güvenlik projesi için teknik bir sonuç raporu oluştur. Rapor şu başlıkları içermeli:
> 1. Yönetici Özeti (Executive Summary)
> 2. Tehdit Modellemesi (Action Hijacking ve Injection riskleri)
> 3. Önerilen Çözüm Mimarisi (Riskli Eylem Kütüphanesi, Tracing, Guardrails)
> 4. Kullanılacak Teknolojiler (LangSmith, NeMo, Docker)
> Raporu akademik ve profesyonel bir dille yaz."
