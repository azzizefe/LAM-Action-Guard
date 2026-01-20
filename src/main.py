"""
LAM-Action-Guard - Main CLI Entry Point
Enhanced version with advanced scanning capabilities.
"""

import argparse
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src.utils.system_check import check_system
from src.engine.scanner import Scanner
from src.engine.advanced_scanner import AdvancedScanner
from src.utils.report_generator import ReportGenerator


def print_banner():
    """Print application banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ██╗      █████╗ ███╗   ███╗                                ║
║   ██║     ██╔══██╗████╗ ████║                                ║
║   ██║     ███████║██╔████╔██║                                ║
║   ██║     ██╔══██║██║╚██╔╝██║                                ║
║   ███████╗██║  ██║██║ ╚═╝ ██║                                ║
║   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝                                ║
║                                                              ║
║   ACTION-GUARD v1.0.0                                        ║
║   Cybersecurity & Automation Tool                            ║
║   Author: Aziz Efe Çırak                                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    parser = argparse.ArgumentParser(
        description="LAM-Action-Guard - Advanced Security Testing & Automation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  python src/main.py --check                     # Sistem kontrolü
  python src/main.py --scan http://target.com   # Tam tarama
  python src/main.py --scan http://target.com --type xss,sqli
  python src/main.py --scan http://target.com --advanced --report html
        """
    )
    
    # Arguments
    parser.add_argument("--check", action="store_true", 
                        help="Sistem self-check çalıştır")
    parser.add_argument("--scan", type=str, metavar="URL",
                        help="Hedef URL (örn: http://example.com)")
    parser.add_argument("--type", type=str, default="all",
                        help="Tarama türleri: xss, sqli, lfi, cmd, all (virgülle ayır)")
    parser.add_argument("--advanced", action="store_true",
                        help="Gelişmiş tarama motoru kullan")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Detaylı çıktı göster")
    parser.add_argument("--report", type=str, choices=["json", "html", "md"],
                        help="Rapor formatı: json, html, md")
    parser.add_argument("--output", "-o", type=str, default="reports",
                        help="Rapor çıktı dizini (varsayılan: reports)")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Sessiz mod (sadece sonuçları göster)")
    
    args = parser.parse_args()

    # Banner
    if not args.quiet:
        print_banner()

    # 1. System Check
    if args.check:
        print("[ℹ] Sistem Kontrolü Başlatılıyor...\n")
        success = check_system()
        sys.exit(0 if success else 1)

    # 2. Security Scan
    if args.scan:
        # Parse scan types
        if args.type == "all":
            scan_types = ["xss", "sqli", "lfi", "cmd"]
        else:
            scan_types = [t.strip().lower() for t in args.type.split(",")]

        # Adjust templates path
        templates_path = os.path.join(PROJECT_ROOT, "src", "templates")
        
        # Choose scanner
        if args.advanced:
            print("[ℹ] Gelişmiş Tarama Modu Aktif\n")
            scanner = AdvancedScanner(templates_dir=templates_path)
            results = scanner.scan_target(args.scan, scan_types, verbose=args.verbose)
        else:
            print(f"[ℹ] Standart Tarama: {args.scan}\n")
            scanner = Scanner(templates_dir=templates_path)
            results = scanner.scan_target(args.scan, args.type)
        
        # Generate report if requested
        if args.report and results:
            report_gen = ReportGenerator(output_dir=args.output)
            
            if args.report == "json":
                filepath = report_gen.generate_json_report(results, args.scan)
            elif args.report == "html":
                filepath = report_gen.generate_html_report(results, args.scan)
            elif args.report == "md":
                filepath = report_gen.generate_markdown_report(results, args.scan)
            
            print(f"\n[📄] Rapor oluşturuldu: {filepath}")
        
        # Exit code based on findings
        if results:
            critical = sum(1 for r in results if r.get("severity") == "Critical")
            sys.exit(2 if critical > 0 else 1)
        sys.exit(0)

    # Default: Show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
