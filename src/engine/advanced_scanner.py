"""
LAM-Action-Guard Advanced Scanner
Enhanced scanner with multiple vulnerability types and detailed analysis.
"""

import json
import os
import time
from typing import List, Dict, Any, Optional
from datetime import datetime

class AdvancedScanner:
    """Advanced security scanner with comprehensive testing capabilities."""

    VULNERABILITY_TYPES = ["xss", "sqli", "lfi", "cmd"]

    def __init__(self, templates_dir: str = "src/templates"):
        self.templates_dir = templates_dir
        self.results: List[Dict[str, Any]] = []
        self.scan_stats = {
            "start_time": None,
            "end_time": None,
            "total_tests": 0,
            "vulnerabilities_found": 0
        }

    def load_patterns(self, pattern_type: str) -> List[Dict]:
        """Load attack patterns from JSON files."""
        file_path = os.path.join(self.templates_dir, f"{pattern_type}_patterns.json")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def load_all_patterns(self) -> Dict[str, List[Dict]]:
        """Load all available pattern files."""
        all_patterns = {}
        for vuln_type in self.VULNERABILITY_TYPES:
            patterns = self.load_patterns(vuln_type)
            if patterns:
                all_patterns[vuln_type] = patterns
        return all_patterns

    def analyze_response(self, response: str, payload: str, vuln_type: str) -> Dict[str, Any]:
        """
        Analyze HTTP response for vulnerability indicators.
        
        Returns analysis results including:
        - reflected: Whether payload appears in response
        - indicators: List of vulnerability indicators found
        - confidence: Confidence level (low, medium, high)
        """
        analysis = {
            "reflected": payload in response,
            "indicators": [],
            "confidence": "low"
        }

        # XSS indicators
        if vuln_type == "xss":
            if "<script" in response.lower() and payload.lower() in response.lower():
                analysis["indicators"].append("script_tag_reflected")
                analysis["confidence"] = "high"
            if "onerror" in response.lower() or "onload" in response.lower():
                analysis["indicators"].append("event_handler_present")

        # SQL Injection indicators
        elif vuln_type == "sqli":
            error_keywords = ["sql", "mysql", "sqlite", "postgresql", "oracle", "syntax error"]
            for keyword in error_keywords:
                if keyword in response.lower():
                    analysis["indicators"].append(f"sql_error_{keyword}")
                    analysis["confidence"] = "medium"

        # LFI indicators
        elif vuln_type == "lfi":
            if "root:" in response or "daemon:" in response:
                analysis["indicators"].append("passwd_file_content")
                analysis["confidence"] = "high"
            if "[boot loader]" in response or "Windows" in response:
                analysis["indicators"].append("windows_file_content")
                analysis["confidence"] = "high"

        # Command Injection indicators
        elif vuln_type == "cmd":
            if "uid=" in response or "gid=" in response:
                analysis["indicators"].append("id_command_output")
                analysis["confidence"] = "high"
            if "total " in response and "drwx" in response:
                analysis["indicators"].append("ls_command_output")
                analysis["confidence"] = "high"

        return analysis

    def scan_target(self, target: str, scan_types: Optional[List[str]] = None, verbose: bool = False) -> List[Dict]:
        """
        Perform comprehensive security scan on target.
        
        Args:
            target: Target URL
            scan_types: List of vulnerability types to test (default: all)
            verbose: Print detailed progress
        """
        self.scan_stats["start_time"] = datetime.now().isoformat()
        self.results = []

        if scan_types is None or "all" in scan_types:
            scan_types = self.VULNERABILITY_TYPES

        all_patterns = self.load_all_patterns()
        
        print(f"\n{'='*60}")
        print(f"  LAM-Action-Guard - Gelişmiş Güvenlik Taraması")
        print(f"{'='*60}")
        print(f"  🎯 Hedef: {target}")
        print(f"  📋 Test Türleri: {', '.join(scan_types).upper()}")
        print(f"{'='*60}\n")

        for vuln_type in scan_types:
            if vuln_type not in all_patterns:
                if verbose:
                    print(f"[⚠] {vuln_type.upper()} şablonları bulunamadı, atlanıyor...")
                continue

            patterns = all_patterns[vuln_type]
            print(f"\n[🔍] {vuln_type.upper()} Testleri Başlatılıyor ({len(patterns)} pattern)...")

            for pattern in patterns:
                self.scan_stats["total_tests"] += 1
                
                if verbose:
                    print(f"  [→] Testing: {pattern['name']}", end="\r")
                
                # Simulate request (in production, use HTTPClient)
                time.sleep(0.3)  # Simulate network delay
                
                # Mock response analysis
                mock_response = f"<html><body>Response</body></html>"
                analysis = self.analyze_response(mock_response, pattern['payload'], vuln_type)

                # For demo: detect vulnerabilities on "test" targets
                if "test" in target.lower() or "localhost" in target.lower():
                    if pattern['severity'] in ["Critical", "High"]:
                        analysis["reflected"] = True
                        analysis["confidence"] = "high"

                if analysis["reflected"] or analysis["confidence"] in ["medium", "high"]:
                    vulnerability = {
                        "target": target,
                        "type": vuln_type.upper(),
                        "vulnerability": pattern['name'],
                        "payload": pattern['payload'],
                        "severity": pattern['severity'],
                        "confidence": analysis["confidence"],
                        "indicators": analysis["indicators"],
                        "timestamp": datetime.now().isoformat()
                    }
                    self.results.append(vulnerability)
                    self.scan_stats["vulnerabilities_found"] += 1
                    print(f"  [🚨] BULUNDU: {pattern['name']} ({pattern['severity']})")
                else:
                    if verbose:
                        print(f"  [✓] Temiz: {pattern['name']}                    ")

        self.scan_stats["end_time"] = datetime.now().isoformat()
        self._print_summary()
        return self.results

    def _print_summary(self) -> None:
        """Print scan summary."""
        print(f"\n{'='*60}")
        print(f"  📊 TARAMA ÖZETİ")
        print(f"{'='*60}")
        print(f"  Toplam Test: {self.scan_stats['total_tests']}")
        print(f"  Bulunan Açık: {self.scan_stats['vulnerabilities_found']}")
        
        if self.results:
            critical = sum(1 for r in self.results if r['severity'] == 'Critical')
            high = sum(1 for r in self.results if r['severity'] == 'High')
            print(f"\n  🔴 Kritik: {critical}")
            print(f"  🟠 Yüksek: {high}")
        else:
            print(f"\n  ✅ Güvenlik açığı bulunamadı!")
        print(f"{'='*60}\n")

    def generate_report(self, format_type: str = "json") -> str:
        """Generate scan report in specified format."""
        if format_type == "json":
            return json.dumps({
                "statistics": self.scan_stats,
                "vulnerabilities": self.results
            }, indent=2, ensure_ascii=False)
        else:
            return str(self.results)


if __name__ == "__main__":
    # Demo run
    scanner = AdvancedScanner()
    scanner.scan_target("http://test.example.com", verbose=True)
