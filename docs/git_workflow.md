# Git Proje Entegrasyonu ve İş Akışı

Bu belge, **LAM-Action-Guard** takımı için önerilen Git iş akışını ve proje entegrasyon stratejilerini tanımlar.

## 🔄 Git Workflow

Projede temiz bir geçmiş ve yönetilebilir bir geliştirme süreci için **Feature Branch** modeli kullanılır.

### Versiyonlama Stratejisi
*   **Araştırma Verileri:** `researchs/` klasöründeki veriler, her önemli bulgudan sonra commit edilerek versiyonlanmalıdır.
*   `main`: Üretime hazır, kararlı kod.
*   `develop`: Geliştirme sürecinin ana dalı.
*   `feature/*`: Yeni özellikler için açılan geçici dallar.

### Otomasyon ile Veri İşleme
Bash scriptleri kullanılarak veri işleme süreçleri Git hook'larına bağlanabilir.
Örnek: `pre-commit` hook'u ile JSON dosyalarının formatını (lint) kontrol etmek.

## 🚀 CI/CD Pipeline Entegrasyonu

Terminal komutlarını kullanarak test ve deployment süreçleri otomatize edilir.

```yaml
# Örnek CI Adımı (Pseudo-code)
steps:
  - name: Run Tests
    run: |
      python src/utils/system_check.py
      python -m unittest discover tests
  - name: Security Scan
    run: |
      python src/main.py --scan --target=http://localhost:3000
```

## 📊 JSON-First Yaklaşımı

API yanıtlarını ve yapılandırma dosyalarını işlerken **JSON-First** yaklaşımı benimsenir. Bu, verilerin type-safe (tür güvenli) olarak işlenmesini ve farklı diller arasında (Bash, Python) kolayca taşınabilmesini sağlar.
