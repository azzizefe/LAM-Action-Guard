# Sızma Testi Otomasyonu (Pentest Automation)

Bu belge, sızma testlerinde kullanılan temel otomasyon tekniklerini ve Unix I/O mimarisini açıklar.

## 🔧 Unix I/O ve Sızma Testleri

Sızma testlerinde Unix I/O mimarisi kritik öneme sahiptir. Veri akışları, pipe'lar ve dosya yönlendirmeleri, araçların zincirlenmesini sağlar.

### File Descriptors (Dosya Tanımlayıcıları)

| FD | Açıklama | Pentest Kullanımı |
|----|----------|-------------------|
| 0 (stdin) | Standart Girdi | Wordlist'lerden okuma |
| 1 (stdout) | Standart Çıktı | Sonuçları pipe'lama |
| 2 (stderr) | Hata Çıktısı | Hata loglarını ayırma |

### Örnek Kullanım
```bash
# Nmap çıktısını grep ile filtreleme
nmap -sV target.com 2>/dev/null | grep "open"

# Çoklu hedef tarama
cat targets.txt | while read ip; do nmap -sS $ip; done
```

## 🔄 TTY vs Pipes

### TTY (Terminal)
- Etkileşimli araçlar için (örn: msfconsole)
- Renk ve format desteği
- Tam ekran uygulamalar

### Pipes (Borular)
- Araç zincirleme için ideal
- Non-blocking I/O
- Büyük veri akışları

```bash
# Pipe örneği: Subdomain keşfi
subfinder -d target.com | httpx | nuclei -t cves/
```

## 📦 Buffering Stratejileri

Sızma testlerinde buffer yönetimi performansı etkiler:

- **Line Buffered:** Her satırda flush (gerçek zamanlı takip)
- **Full Buffered:** Tampon dolunca flush (hız optimizasyonu)
- **Unbuffered:** Anlık yazma (kritik loglar)

```bash
# Unbuffered output için
stdbuf -o0 nmap -sV target.com | tee scan.log

# Python'da unbuffered
python -u scanner.py
```

## 🛠️ Otomasyon Scriptleri

### Recon Otomasyonu
```bash
#!/bin/bash
# Basit recon pipeline
TARGET=$1
echo "[*] Hedef: $TARGET"
subfinder -d $TARGET -o subs.txt
cat subs.txt | httpx -silent | nuclei -severity critical,high
```

### Port Tarama
```bash
# Hızlı port discovery
masscan -p1-65535 $TARGET --rate=10000 -oL ports.txt
cat ports.txt | awk '{print $3}' | nmap -sV -iL -
```

## ⚠️ Dikkat Edilecekler

1. **Permission:** Sadece izinli hedeflerde test yapın
2. **Rate Limiting:** Hedefi boğmayın
3. **Logging:** Tüm aktiviteleri loglayın
4. **Cleanup:** Test sonrası temizlik yapın
