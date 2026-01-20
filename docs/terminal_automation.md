# Terminal Automation & Unix I/O Rehberi

Bu belge, projenin terminal otomasyonu yeteneklerinin teknik altyapısını ve dil karşılaştırmalarını içerir.

## 🖥️ Unix I/O Architecture

Unix sistemlerinde her şey bir dosyadır ve I/O işlemleri **File Descriptors** üzerinden yönetilir.

*   **File Descriptors (0/1/2):**
    *   `0`: Standard Input (stdin)
    *   `1`: Standard Output (stdout)
    *   `2`: Standard Error (stderr)
*   **TTY vs Pipes:** Terminal (TTY) etkileşimli kullanım içindir, Pipe'lar (`|`) ise süreçler arası veri akışı sağlar.
*   **Buffering Strategies:** Performans için verilerin bellekte tutulup toplu yazılması (Buffered) veya anlık yazılması (Unbuffered).

## 🆚 5 Dil Karşılaştırması

Terminal otomasyonunda kullanılan popüler dillerin karşılaştırması:

| Dil | Yöntem | Açıklama |
| :--- | :--- | :--- |
| **Bash** | Process Subst. | Hızlı, native Unix komutları, boru hatları (pipes) için ideal. |
| **Python** | asyncio | Güçlü kütüphane desteği, okunabilir, asenkron G/Ç işlemleri. |
| **Go** | Goroutines | Yüksek performanslı eşzamanlılık, tekil binary çıktısı. |
| **Node.js** | Streams | Event-driven mimari, büyük veri akışları için verimli. |
| **Rust** | Tokio | Bellek güvenliği, sıfır maliyetli soyutlamalar, yüksek performans. |

## 🚀 İleri Konular (Advanced Topics)

*   **JSON-First Parsing:** Terminal çıktılarının metin yerine JSON olarak üretilmesi ve işlenmesi (`jq` gibi araçlarla).
*   **Stream Analysis:** Veri akışlarının gerçek zamanlı analizi.
*   **Error Handling:** Exit kodlarının (0-255) doğru yönetimi ve hata yakalama.
*   **Security Best Practices:** Hassas verilerin (env vars) korunması, `eval` kullanımından kaçınma.
