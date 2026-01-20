# LAM-Action-Guard

**Sızma Testi Otomasyon Platformu** - Penetration Testing Automation Framework

LAM-Action-Guard, profesyonel sızma testleri için geliştirilmiş çok dilli (Bash, Python, Go) otomasyon aracıdır.

## 🎯 Özellikler

| Araç | Dil | Açıklama |
|------|-----|----------|
| `recon_automation.sh` | Bash | Keşif otomasyonu (subdomain, port, http probe) |
| `vuln_scanner.py` | Python | Güvenlik açığı tarayıcı (XSS, SQLi, LFI, RCE) |
| `port_scanner.go` | Go | Yüksek performanslı concurrent port tarama |

## 📂 Proje Yapısı

```
lam/
├── project_info.json
├── readme.md
├── requirements.txt
├── docs/
│   ├── sizma_testi_otomasyonu.md      # Unix I/O & Otomasyon
│   ├── guvenlik_dil_karsilastirmasi.md # 5 Dil Karşılaştırması
│   └── ileri_sizma_teknikleri.md       # Advanced Topics
├── specs/
│   └── technical_requirements.md
├── src/
│   ├── recon_automation.sh    # Bash Recon
│   ├── vuln_scanner.py        # Python Scanner
│   ├── port_scanner.go        # Go Fast Scanner
│   ├── main.py                # Ana CLI
│   ├── engine/                # Tarama motorları
│   ├── templates/             # Saldırı şablonları
│   └── utils/                 # Yardımcı modüller
└── tests/
```

## 🚀 Hızlı Başlangıç

### Python Scanner
```bash
python src/vuln_scanner.py http://hedef.com -t xss,sqli -o rapor.json
```

### Bash Recon
```bash
chmod +x src/recon_automation.sh
./src/recon_automation.sh -d hedef.com -o ./output
```

### Go Port Scanner
```bash
cd src
go build -o port_scanner port_scanner.go
./port_scanner -t hedef.com -start 1 -end 1024 -workers 200
```

## 📊 Desteklenen Zafiyet Türleri

- **XSS** - Cross-Site Scripting
- **SQLi** - SQL Injection  
- **LFI** - Local File Inclusion
- **RCE** - Remote Code Execution

## 📚 Dokümantasyon

- [Sızma Testi Otomasyonu](docs/sizma_testi_otomasyonu.md) - Unix I/O ve pipeline
- [Dil Karşılaştırması](docs/guvenlik_dil_karsilastirmasi.md) - Bash/Python/Go/Node/Rust
- [İleri Teknikler](docs/ileri_sizma_teknikleri.md) - JSON parsing, error handling

## ⚠️ Yasal Uyarı

Bu araçlar **yalnızca yasal ve etik sızma testleri** için tasarlanmıştır. Sadece izniniz olan sistemlerde kullanın.

## 👤 Yazar

**Aziz Efe Çırak**

---
*LAM-Action-Guard v1.0.0 - Pentest Automation Platform*
