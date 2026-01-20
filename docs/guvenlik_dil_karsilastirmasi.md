# Güvenlik Araçları Dil Karşılaştırması

Bu belge, sızma testi araçları geliştirmek için kullanılan programlama dillerini karşılaştırır.

## 📊 Dil Karşılaştırma Tablosu

| Özellik | Bash | Python | Go | Node.js | Rust |
|---------|------|--------|-----|---------|------|
| **Hız** | Orta | Orta | Yüksek | Orta | Çok Yüksek |
| **Öğrenme** | Kolay | Kolay | Orta | Kolay | Zor |
| **Kütüphane** | Az | Çok | Orta | Çok | Orta |
| **Dağıtım** | Native | Bağımlı | Tek Binary | Bağımlı | Tek Binary |

---

## 🐚 Bash (Process Substitution)

**Avantajlar:**
- Native Unix entegrasyonu
- Hızlı prototipleme
- Pipe-based workflow

**Pentest Kullanımı:**
```bash
#!/bin/bash
# Recon script
for sub in $(subfinder -d $1 -silent); do
    echo $sub | httpx -silent
done | nuclei -t cves/
```

**Örnek Araçlar:** Masscan wrapper, Nmap otomasyonu, Log parser

---

## 🐍 Python (asyncio)

**Avantajlar:**
- Zengin kütüphane ekosistemi (requests, scapy, pwntools)
- Hızlı geliştirme
- Cross-platform

**Pentest Kullanımı:**
```python
import asyncio
import aiohttp

async def scan_url(session, url, payload):
    async with session.get(url + payload) as resp:
        return await resp.text()

async def main():
    payloads = ["' OR '1'='1", "<script>alert(1)</script>"]
    async with aiohttp.ClientSession() as session:
        tasks = [scan_url(session, target, p) for p in payloads]
        results = await asyncio.gather(*tasks)
```

**Örnek Araçlar:** SQLMap, Burp extensions, Custom exploits

---

## 🦫 Go (Goroutines)

**Avantajlar:**
- Yüksek performans concurrency
- Tek binary dağıtım
- Düşük bellek kullanımı

**Pentest Kullanımı:**
```go
package main

import (
    "fmt"
    "net"
    "sync"
)

func scanPort(host string, port int, wg *sync.WaitGroup) {
    defer wg.Done()
    addr := fmt.Sprintf("%s:%d", host, port)
    conn, err := net.Dial("tcp", addr)
    if err == nil {
        fmt.Printf("[OPEN] %s\n", addr)
        conn.Close()
    }
}

func main() {
    var wg sync.WaitGroup
    for port := 1; port <= 1024; port++ {
        wg.Add(1)
        go scanPort("target.com", port, &wg)
    }
    wg.Wait()
}
```

**Örnek Araçlar:** Nuclei, httpx, subfinder, ffuf

---

## 📦 Node.js (Streams)

**Avantajlar:**
- Event-driven mimari
- Büyük veri stream'leri
- NPM ekosistemi

**Pentest Kullanımı:**
```javascript
const { Transform } = require('stream');
const axios = require('axios');

const filterOpen = new Transform({
    transform(chunk, encoding, callback) {
        const line = chunk.toString();
        if (line.includes('200')) {
            this.push(line);
        }
        callback();
    }
});

// Stream-based subdomain checker
```

---

## 🦀 Rust (Tokio)

**Avantajlar:**
- Memory safety garantisi
- C-seviyesi performans
- Zero-cost abstractions

**Pentest Kullanımı:**
```rust
use tokio::net::TcpStream;
use std::net::SocketAddr;

async fn check_port(addr: SocketAddr) -> bool {
    TcpStream::connect(addr).await.is_ok()
}
```

**Örnek Araçlar:** RustScan, feroxbuster

---

## 🎯 Hangi Dili Seçmeli?

| Senaryo | Önerilen Dil |
|---------|--------------|
| Hızlı script | Bash |
| Exploit geliştirme | Python |
| Performans kritik araç | Go / Rust |
| Web fuzzing | Go |
| Ağ araçları | Rust |
