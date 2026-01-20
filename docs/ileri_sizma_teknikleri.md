# İleri Sızma Testi Teknikleri

Bu belge, profesyonel sızma testlerinde kullanılan ileri seviye teknikleri kapsar.

## 📊 JSON-First Parsing

Modern pentest araçları JSON çıktı üretir. Bu, otomasyon ve entegrasyon için kritiktir.

### Araç Çıktılarını İşleme
```bash
# Nmap JSON çıktısı
nmap -sV target.com -oX - | xq '.nmaprun.host.ports.port'

# Nuclei JSON
nuclei -target http://target.com -json | jq '.info.severity'

# httpx JSON
httpx -l urls.txt -json | jq 'select(.status_code == 200)'
```

### Python ile JSON Parsing
```python
import json
import subprocess

def parse_nuclei_output(target):
    result = subprocess.run(
        ['nuclei', '-target', target, '-json'],
        capture_output=True, text=True
    )
    findings = []
    for line in result.stdout.strip().split('\n'):
        if line:
            finding = json.loads(line)
            findings.append({
                'template': finding['template-id'],
                'severity': finding['info']['severity'],
                'matched': finding.get('matched-at', '')
            })
    return findings
```

---

## 🔍 Stream Analysis

Gerçek zamanlı veri akışı analizi, aktif sızma testlerinde kullanılır.

### Canlı Trafik Analizi
```python
from scapy.all import sniff, TCP

def analyze_packet(pkt):
    if pkt.haslayer(TCP):
        if pkt[TCP].flags == 'S':
            print(f"SYN -> {pkt[IP].dst}:{pkt[TCP].dport}")
        elif pkt[TCP].flags == 'SA':
            print(f"SYN-ACK <- {pkt[IP].src}:{pkt[TCP].sport}")

sniff(filter="tcp", prn=analyze_packet, count=100)
```

### Log Stream Monitoring
```bash
# Gerçek zamanlı log takibi
tail -f /var/log/apache2/access.log | \
    grep --line-buffered "POST" | \
    awk '{print $1, $7}'
```

---

## ⚠️ Error Handling

Profesyonel araçlar sağlam hata yönetimine sahip olmalıdır.

### Python Error Handling
```python
import requests
from requests.exceptions import ConnectionError, Timeout

def safe_request(url, timeout=10):
    try:
        response = requests.get(url, timeout=timeout)
        return {
            'status': 'success',
            'code': response.status_code,
            'body': response.text[:500]
        }
    except Timeout:
        return {'status': 'timeout', 'url': url}
    except ConnectionError:
        return {'status': 'connection_error', 'url': url}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
```

### Bash Error Handling
```bash
#!/bin/bash
set -euo pipefail

trap 'echo "Error on line $LINENO"; exit 1' ERR

scan_target() {
    local target=$1
    if ! ping -c 1 "$target" &>/dev/null; then
        echo "[-] Target unreachable: $target"
        return 1
    fi
    nmap -sS "$target" || return 1
}
```

---

## 🔒 Security Best Practices

### 1. Credential Management
```python
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('SHODAN_API_KEY')
if not API_KEY:
    raise ValueError("SHODAN_API_KEY not set!")
```

### 2. Rate Limiting
```python
import time
from functools import wraps

def rate_limit(calls_per_second):
    min_interval = 1.0 / calls_per_second
    last_call = [0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_call[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(10)  # 10 requests per second
def make_request(url):
    return requests.get(url)
```

### 3. Secure Output Handling
```python
import html
import re

def sanitize_output(data):
    """Prevent XSS in reports"""
    if isinstance(data, str):
        return html.escape(data)
    return data

def redact_sensitive(text):
    """Redact passwords and API keys"""
    patterns = [
        (r'password["\']?\s*[:=]\s*["\']?[\w@#$%^&*]+', 'password=***REDACTED***'),
        (r'api[_-]?key["\']?\s*[:=]\s*["\']?[\w-]+', 'api_key=***REDACTED***'),
    ]
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text
```

---

## 🎯 Entegrasyon Örnekleri

### CI/CD Pipeline'da Güvenlik Taraması
```yaml
# .github/workflows/security.yml
name: Security Scan
on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Nuclei
        run: |
          nuclei -target ${{ secrets.TARGET }} \
                 -severity critical,high \
                 -json > results.json
      - name: Check Results
        run: |
          if [ -s results.json ]; then
            echo "Vulnerabilities found!"
            exit 1
          fi
```

### Slack Notification
```python
import requests

def notify_slack(findings):
    webhook = os.getenv('SLACK_WEBHOOK')
    message = f"🚨 {len(findings)} vulnerabilities found!"
    requests.post(webhook, json={'text': message})
```
