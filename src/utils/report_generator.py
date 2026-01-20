"""
LAM-Action-Guard Report Generator
Generates detailed reports in multiple formats.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any

class ReportGenerator:
    """Generates security scan reports in various formats."""

    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        self._ensure_output_dir()

    def _ensure_output_dir(self) -> None:
        """Create output directory if it doesn't exist."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _generate_filename(self, format_type: str) -> str:
        """Generate a timestamped filename."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.output_dir, f"scan_report_{timestamp}.{format_type}")

    def generate_json_report(self, scan_results: List[Dict], target: str) -> str:
        """Generate a JSON report."""
        report = {
            "metadata": {
                "tool": "LAM-Action-Guard",
                "version": "1.0.0",
                "scan_date": datetime.now().isoformat(),
                "target": target
            },
            "summary": {
                "total_vulnerabilities": len(scan_results),
                "critical": sum(1 for r in scan_results if r.get("severity") == "Critical"),
                "high": sum(1 for r in scan_results if r.get("severity") == "High"),
                "medium": sum(1 for r in scan_results if r.get("severity") == "Medium"),
                "low": sum(1 for r in scan_results if r.get("severity") == "Low")
            },
            "vulnerabilities": scan_results
        }
        
        filepath = self._generate_filename("json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return filepath

    def generate_markdown_report(self, scan_results: List[Dict], target: str) -> str:
        """Generate a Markdown report."""
        lines = [
            "# LAM-Action-Guard Güvenlik Raporu",
            "",
            f"**Hedef:** {target}",
            f"**Tarih:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Özet",
            "",
            f"- **Toplam Güvenlik Açığı:** {len(scan_results)}",
            "",
            "## Detaylı Bulgular",
            ""
        ]

        if not scan_results:
            lines.append("✅ Herhangi bir güvenlik açığı tespit edilmedi.")
        else:
            for i, vuln in enumerate(scan_results, 1):
                severity_emoji = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}.get(vuln.get("severity", ""), "⚪")
                lines.extend([
                    f"### {i}. {vuln.get('vulnerability', 'Unknown')}",
                    "",
                    f"- **Severity:** {severity_emoji} {vuln.get('severity', 'N/A')}",
                    f"- **Target:** `{vuln.get('target', 'N/A')}`",
                    f"- **Payload:** `{vuln.get('payload', 'N/A')}`",
                    ""
                ])

        filepath = self._generate_filename("md")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        
        return filepath

    def generate_html_report(self, scan_results: List[Dict], target: str) -> str:
        """Generate an HTML report."""
        critical = sum(1 for r in scan_results if r.get("severity") == "Critical")
        high = sum(1 for r in scan_results if r.get("severity") == "High")
        
        vuln_rows = ""
        for vuln in scan_results:
            severity_class = vuln.get("severity", "").lower()
            vuln_rows += f"""
            <tr class="{severity_class}">
                <td>{vuln.get('vulnerability', 'N/A')}</td>
                <td>{vuln.get('severity', 'N/A')}</td>
                <td><code>{vuln.get('payload', 'N/A')}</code></td>
            </tr>
            """

        html_content = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>LAM-Action-Guard Raporu</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; margin: 20px; background: #0d1117; color: #c9d1d9; }}
        h1 {{ color: #58a6ff; }}
        .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
        .stat {{ padding: 15px 25px; border-radius: 8px; background: #161b22; }}
        .stat.critical {{ border-left: 4px solid #f85149; }}
        .stat.high {{ border-left: 4px solid #f0883e; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #30363d; }}
        th {{ background: #161b22; }}
        tr.critical {{ background: rgba(248, 81, 73, 0.1); }}
        tr.high {{ background: rgba(240, 136, 62, 0.1); }}
        code {{ background: #21262d; padding: 2px 6px; border-radius: 4px; }}
    </style>
</head>
<body>
    <h1>🛡️ LAM-Action-Guard Güvenlik Raporu</h1>
    <p><strong>Hedef:</strong> {target} | <strong>Tarih:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    
    <div class="summary">
        <div class="stat critical"><strong>{critical}</strong> Kritik</div>
        <div class="stat high"><strong>{high}</strong> Yüksek</div>
        <div class="stat"><strong>{len(scan_results)}</strong> Toplam</div>
    </div>
    
    <table>
        <thead><tr><th>Güvenlik Açığı</th><th>Önem</th><th>Payload</th></tr></thead>
        <tbody>{vuln_rows if vuln_rows else '<tr><td colspan="3">✅ Güvenlik açığı bulunamadı</td></tr>'}</tbody>
    </table>
</body>
</html>"""

        filepath = self._generate_filename("html")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
