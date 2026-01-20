"""
vuln_scanner.py - Python Güvenlik Açığı Tarayıcı
LAM-Action-Guard - Aziz Efe Çırak

Çoklu güvenlik açığı türlerini tarayabilen modüler Python scanner.
"""

import argparse
import json
import sys
import time
import socket
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, urljoin

# Simüle HTTP client (production'da requests kullanılır)
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class Colors:
    """Terminal renkleri"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class VulnScanner:
    """Modüler Güvenlik Açığı Tarayıcı"""

    def __init__(self, target: str, threads: int = 10, timeout: int = 10):
        self.target = target
        self.threads = threads
        self.timeout = timeout
        self.results: List[Dict] = []
        self.start_time = None
        
        # Payload'lar
        self.payloads = {
            'xss': [
                {'id': 'xss_basic', 'payload': '<script>alert(1)</script>', 'severity': 'High'},
                {'id': 'xss_img', 'payload': '<img src=x onerror=alert(1)>', 'severity': 'Medium'},
                {'id': 'xss_svg', 'payload': '<svg/onload=alert(1)>', 'severity': 'Medium'},
                {'id': 'xss_body', 'payload': '<body onload=alert(1)>', 'severity': 'Medium'},
            ],
            'sqli': [
                {'id': 'sqli_or', 'payload': "' OR '1'='1", 'severity': 'Critical'},
                {'id': 'sqli_union', 'payload': "' UNION SELECT 1,2,3--", 'severity': 'Critical'},
                {'id': 'sqli_comment', 'payload': "admin'--", 'severity': 'High'},
                {'id': 'sqli_time', 'payload': "' AND SLEEP(5)--", 'severity': 'Critical'},
            ],
            'lfi': [
                {'id': 'lfi_etc', 'payload': '../../../etc/passwd', 'severity': 'Critical'},
                {'id': 'lfi_null', 'payload': '../../../etc/passwd%00', 'severity': 'Critical'},
                {'id': 'lfi_win', 'payload': '..\\..\\..\\windows\\system32\\config\\sam', 'severity': 'Critical'},
            ],
            'rce': [
                {'id': 'rce_semicolon', 'payload': '; ls -la', 'severity': 'Critical'},
                {'id': 'rce_pipe', 'payload': '| cat /etc/passwd', 'severity': 'Critical'},
                {'id': 'rce_backtick', 'payload': '`id`', 'severity': 'Critical'},
            ]
        }

    def log(self, level: str, message: str):
        """Renkli log çıktısı"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        colors = {
            'INFO': Colors.GREEN,
            'WARN': Colors.YELLOW,
            'ERROR': Colors.RED,
            'VULN': Colors.RED + Colors.BOLD,
            'SCAN': Colors.BLUE
        }
        color = colors.get(level, Colors.RESET)
        print(f"{color}[{level}]{Colors.RESET} [{timestamp}] {message}")

    def banner(self):
        """Banner göster"""
        print(f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════╗
║                                                             ║
║   {Colors.BOLD}LAM-Action-Guard - Vulnerability Scanner{Colors.RESET}{Colors.CYAN}                ║
║   Python Security Testing Tool v1.0                         ║
║   Author: Aziz Efe Çırak                                    ║
║                                                             ║
╚═══════════════════════════════════════════════════════════╝{Colors.RESET}
        """)

    def check_target_reachable(self) -> bool:
        """Hedefin erişilebilir olduğunu kontrol et"""
        try:
            parsed = urlparse(self.target)
            host = parsed.hostname or self.target
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            
            return result == 0
        except Exception:
            return False

    def make_request(self, url: str, method: str = 'GET', data: Optional[Dict] = None) -> Dict:
        """HTTP isteği yap"""
        if HAS_REQUESTS:
            try:
                if method == 'GET':
                    resp = requests.get(url, timeout=self.timeout, verify=False)
                else:
                    resp = requests.post(url, data=data, timeout=self.timeout, verify=False)
                return {
                    'status_code': resp.status_code,
                    'body': resp.text,
                    'headers': dict(resp.headers),
                    'elapsed': resp.elapsed.total_seconds()
                }
            except Exception as e:
                return {'error': str(e)}
        else:
            # Simüle response
            return {
                'status_code': 200,
                'body': '<html><body>Test Response</body></html>',
                'headers': {},
                'elapsed': 0.1
            }

    def detect_vulnerability(self, response: Dict, payload_info: Dict, vuln_type: str) -> Optional[Dict]:
        """Yanıtta güvenlik açığı tespit et"""
        if 'error' in response:
            return None
            
        body = response.get('body', '').lower()
        payload = payload_info['payload'].lower()
        
        # XSS Detection
        if vuln_type == 'xss':
            if payload in body or '<script' in body:
                return {
                    'type': 'XSS',
                    'payload': payload_info['payload'],
                    'severity': payload_info['severity'],
                    'evidence': 'Payload reflected in response'
                }
        
        # SQLi Detection
        elif vuln_type == 'sqli':
            sql_errors = ['sql', 'mysql', 'syntax error', 'oracle', 'postgresql', 'sqlite']
            for error in sql_errors:
                if error in body:
                    return {
                        'type': 'SQL Injection',
                        'payload': payload_info['payload'],
                        'severity': payload_info['severity'],
                        'evidence': f'SQL error detected: {error}'
                    }
        
        # LFI Detection
        elif vuln_type == 'lfi':
            lfi_indicators = ['root:', 'daemon:', '[boot loader]', 'windows']
            for indicator in lfi_indicators:
                if indicator in body:
                    return {
                        'type': 'Local File Inclusion',
                        'payload': payload_info['payload'],
                        'severity': payload_info['severity'],
                        'evidence': f'File content detected: {indicator}'
                    }
        
        # RCE Detection
        elif vuln_type == 'rce':
            rce_indicators = ['uid=', 'gid=', 'drwx', 'total ']
            for indicator in rce_indicators:
                if indicator in body:
                    return {
                        'type': 'Remote Code Execution',
                        'payload': payload_info['payload'],
                        'severity': payload_info['severity'],
                        'evidence': f'Command output detected: {indicator}'
                    }
        
        return None

    def scan_vuln_type(self, vuln_type: str) -> List[Dict]:
        """Belirli bir zafiyet türünü tara"""
        findings = []
        payloads = self.payloads.get(vuln_type, [])
        
        self.log('SCAN', f'{vuln_type.upper()} taraması başlatılıyor ({len(payloads)} payload)')
        
        for payload_info in payloads:
            # URL'ye payload ekle
            test_url = f"{self.target}?test={payload_info['payload']}"
            
            response = self.make_request(test_url)
            vuln = self.detect_vulnerability(response, payload_info, vuln_type)
            
            if vuln:
                vuln['url'] = test_url
                vuln['timestamp'] = datetime.now().isoformat()
                findings.append(vuln)
                self.log('VULN', f"BULUNDU: {vuln['type']} - {payload_info['id']}")
            else:
                print(f"  [·] {payload_info['id']}: Temiz", end='\r')
            
            time.sleep(0.2)  # Rate limiting
        
        return findings

    def scan(self, vuln_types: List[str] = None) -> List[Dict]:
        """Tam tarama başlat"""
        self.banner()
        self.start_time = datetime.now()
        
        if vuln_types is None:
            vuln_types = list(self.payloads.keys())
        
        self.log('INFO', f'Hedef: {self.target}')
        self.log('INFO', f'Tarama türleri: {", ".join(vuln_types)}')
        print()
        
        # Hedef erişilebilirlik kontrolü
        if not self.check_target_reachable():
            self.log('WARN', 'Hedef erişilemez olabilir, yine de tarama yapılıyor...')
        
        # Her zafiyet türünü tara
        for vuln_type in vuln_types:
            findings = self.scan_vuln_type(vuln_type)
            self.results.extend(findings)
            print()  # Boş satır
        
        # Özet
        self._print_summary()
        return self.results

    def _print_summary(self):
        """Tarama özeti"""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        print(f"\n{Colors.CYAN}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}  TARAMA ÖZETİ{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
        print(f"  Hedef: {self.target}")
        print(f"  Süre: {elapsed:.2f} saniye")
        print(f"  Toplam Bulgu: {len(self.results)}")
        
        if self.results:
            critical = sum(1 for r in self.results if r['severity'] == 'Critical')
            high = sum(1 for r in self.results if r['severity'] == 'High')
            print(f"\n  {Colors.RED}🔴 Kritik: {critical}{Colors.RESET}")
            print(f"  {Colors.YELLOW}🟠 Yüksek: {high}{Colors.RESET}")
        else:
            print(f"\n  {Colors.GREEN}✅ Güvenlik açığı bulunamadı{Colors.RESET}")
        
        print(f"{Colors.CYAN}{'='*60}{Colors.RESET}\n")

    def export_json(self, filepath: str):
        """Sonuçları JSON olarak dışa aktar"""
        report = {
            'target': self.target,
            'scan_date': datetime.now().isoformat(),
            'scanner': 'LAM-Action-Guard vuln_scanner.py',
            'total_findings': len(self.results),
            'vulnerabilities': self.results
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.log('INFO', f'Rapor kaydedildi: {filepath}')


def main():
    parser = argparse.ArgumentParser(
        description='LAM-Action-Guard Vulnerability Scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('target', help='Hedef URL (örn: http://example.com)')
    parser.add_argument('-t', '--types', default='all', 
                        help='Zafiyet türleri: xss,sqli,lfi,rce,all')
    parser.add_argument('-o', '--output', help='JSON çıktı dosyası')
    parser.add_argument('--threads', type=int, default=10, help='Thread sayısı')
    parser.add_argument('--timeout', type=int, default=10, help='İstek timeout (saniye)')
    
    args = parser.parse_args()
    
    # Zafiyet türlerini parse et
    if args.types == 'all':
        vuln_types = ['xss', 'sqli', 'lfi', 'rce']
    else:
        vuln_types = [t.strip() for t in args.types.split(',')]
    
    # Scanner oluştur ve çalıştır
    scanner = VulnScanner(
        target=args.target,
        threads=args.threads,
        timeout=args.timeout
    )
    
    results = scanner.scan(vuln_types)
    
    # Rapor
    if args.output:
        scanner.export_json(args.output)
    
    # Exit code
    sys.exit(1 if results else 0)


if __name__ == '__main__':
    main()
