# 🛡️ LAM-Action-Guard

![Version](https://img.shields.io/badge/version-0.1.0-blue) ![Status](https://img.shields.io/badge/status-Alpha-orange) ![Focus](https://img.shields.io/badge/focus-Agentic_AI_Security-red)

> **Security guardrails and vulnerability testing scripts optimized for Large Action Models (LAMs).**

**LAM-Action-Guard**, otonom yapay zeka ajanlarının (Agents) gerçekleştirdiği eylemleri (API çağrıları, veri işleme, satın alma) denetleyen ve **"Action Hijacking"** saldırılarını önleyen bir güvenlik katmanıdır.

---

### 🚀 Temel Yetenekler

| Özellik | Açıklama |
| :--- | :--- |
| **🧨 Riskli Eylem Kütüphanesi** | Kritik işlemler (Veri silme, Para transferi) için hazır test senaryoları. |
| **⚖️ Intent Verification** | Kullanıcı niyeti ile Ajanın eylemi arasındaki tutarlılığı matematiksel olarak doğrular. |
| **🕵️‍♂️ Trace Auditing** | Ajanın karar mekanizmasını ve kullandığı araçları (Tools) anlık izler (Log & Monitor). |
| **💉 Indirect Injection Sim** | Web/Döküman tabanlı gizli komutlara karşı ajanın dayanıklılığını test eder. |

---

### 📂 Proje Mimarisi

```text
LAM-ACTION-GUARD/
├── 🛡️ guardrails/       # (CORE) Niyet doğrulama ve eylem filtreleri
├── 🧪 scenarios/        # Saldırı simülasyonları (Injection, Fraud)
├── 📝 tracer/           # Otonom akış izleme ve loglama
├── ⚙️ config/           # İzin verilen eylem politikaları (Policy)
└── 📄 main.py           # Başlatıcı
