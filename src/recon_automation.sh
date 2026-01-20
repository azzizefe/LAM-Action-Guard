#!/bin/bash
#
# recon_automation.sh - Sızma Testi Keşif Otomasyonu
# LAM-Action-Guard - Aziz Efe Çırak
#

set -euo pipefail

# Renkler
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
banner() {
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════╗"
    echo "║   LAM-Action-Guard - Recon Automation         ║"
    echo "║   Sızma Testi Keşif Scripti v1.0              ║"
    echo "╚═══════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Kullanım bilgisi
usage() {
    echo "Kullanım: $0 -d <domain> [-o <output_dir>]"
    echo ""
    echo "Seçenekler:"
    echo "  -d    Hedef domain (zorunlu)"
    echo "  -o    Çıktı dizini (varsayılan: ./recon_output)"
    echo "  -h    Yardım"
    exit 1
}

# Log fonksiyonu
log() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case $level in
        "INFO")  echo -e "${GREEN}[+]${NC} [$timestamp] $message" ;;
        "WARN")  echo -e "${YELLOW}[!]${NC} [$timestamp] $message" ;;
        "ERROR") echo -e "${RED}[-]${NC} [$timestamp] $message" ;;
        "SCAN")  echo -e "${BLUE}[*]${NC} [$timestamp] $message" ;;
    esac
}

# Subdomain Enumeration
subdomain_enum() {
    local domain=$1
    local output_file=$2
    
    log "SCAN" "Subdomain taraması başlatılıyor: $domain"
    
    # Pasif yöntemler (örnek - gerçek araçlar yoksa simüle et)
    if command -v subfinder &> /dev/null; then
        subfinder -d "$domain" -silent >> "$output_file" 2>/dev/null
    else
        log "WARN" "subfinder bulunamadı, basit DNS sorgusu yapılıyor"
        echo "www.$domain" >> "$output_file"
        echo "mail.$domain" >> "$output_file"
        echo "api.$domain" >> "$output_file"
        echo "admin.$domain" >> "$output_file"
        echo "dev.$domain" >> "$output_file"
    fi
    
    # Sonuçları temizle ve sırala
    sort -u "$output_file" -o "$output_file"
    local count=$(wc -l < "$output_file")
    log "INFO" "Toplam $count subdomain bulundu"
}

# Port Tarama
port_scan() {
    local target=$1
    local output_file=$2
    
    log "SCAN" "Port taraması: $target"
    
    if command -v nmap &> /dev/null; then
        nmap -sS -sV -T4 --top-ports 100 "$target" -oN "$output_file" 2>/dev/null
    else
        log "WARN" "nmap bulunamadı, basit TCP kontrolü yapılıyor"
        for port in 21 22 23 25 80 443 3306 3389 8080; do
            (echo >/dev/tcp/"$target"/"$port") 2>/dev/null && \
                echo "$target:$port OPEN" >> "$output_file"
        done
    fi
}

# HTTP Probe
http_probe() {
    local input_file=$1
    local output_file=$2
    
    log "SCAN" "HTTP servis kontrolü başlatılıyor"
    
    if command -v httpx &> /dev/null; then
        cat "$input_file" | httpx -silent -status-code >> "$output_file" 2>/dev/null
    else
        log "WARN" "httpx bulunamadı, curl ile kontrol yapılıyor"
        while read -r subdomain; do
            for proto in "https" "http"; do
                status=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "$proto://$subdomain" 2>/dev/null || echo "000")
                if [ "$status" != "000" ]; then
                    echo "$proto://$subdomain [$status]" >> "$output_file"
                fi
            done
        done < "$input_file"
    fi
    
    local count=$(wc -l < "$output_file" 2>/dev/null || echo "0")
    log "INFO" "Toplam $count aktif HTTP servisi bulundu"
}

# Dizin Brute Force
dir_bruteforce() {
    local url=$1
    local output_file=$2
    
    log "SCAN" "Dizin taraması: $url"
    
    # Basit wordlist
    local dirs=("admin" "login" "api" "backup" "test" "dev" ".git" "config" "uploads" "wp-admin")
    
    for dir in "${dirs[@]}"; do
        local target_url="$url/$dir"
        local status=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "$target_url" 2>/dev/null || echo "000")
        if [ "$status" == "200" ] || [ "$status" == "301" ] || [ "$status" == "302" ] || [ "$status" == "403" ]; then
            echo "[$status] $target_url" >> "$output_file"
            log "INFO" "Bulundu: [$status] $target_url"
        fi
    done
}

# JSON Rapor Oluştur
generate_json_report() {
    local output_dir=$1
    local domain=$2
    local report_file="$output_dir/report.json"
    
    log "INFO" "JSON rapor oluşturuluyor"
    
    local subdomains=$(cat "$output_dir/subdomains.txt" 2>/dev/null | jq -R -s -c 'split("\n") | map(select(length > 0))' || echo "[]")
    local live_hosts=$(cat "$output_dir/live_hosts.txt" 2>/dev/null | jq -R -s -c 'split("\n") | map(select(length > 0))' || echo "[]")
    
    cat > "$report_file" << EOF
{
    "target": "$domain",
    "scan_date": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "tool": "LAM-Action-Guard Recon",
    "subdomains": $subdomains,
    "live_hosts": $live_hosts,
    "status": "completed"
}
EOF
    
    log "INFO" "Rapor oluşturuldu: $report_file"
}

# Ana fonksiyon
main() {
    banner
    
    local domain=""
    local output_dir="./recon_output"
    
    # Argümanları parse et
    while getopts "d:o:h" opt; do
        case $opt in
            d) domain="$OPTARG" ;;
            o) output_dir="$OPTARG" ;;
            h) usage ;;
            *) usage ;;
        esac
    done
    
    # Domain kontrolü
    if [ -z "$domain" ]; then
        log "ERROR" "Domain belirtilmedi!"
        usage
    fi
    
    # Çıktı dizini oluştur
    mkdir -p "$output_dir"
    
    log "INFO" "Hedef: $domain"
    log "INFO" "Çıktı dizini: $output_dir"
    echo ""
    
    # Taramaları çalıştır
    subdomain_enum "$domain" "$output_dir/subdomains.txt"
    http_probe "$output_dir/subdomains.txt" "$output_dir/live_hosts.txt"
    
    # İlk aktif host üzerinde port tarama
    local first_host=$(head -1 "$output_dir/subdomains.txt" 2>/dev/null)
    if [ -n "$first_host" ]; then
        port_scan "$first_host" "$output_dir/ports.txt"
    fi
    
    # Rapor oluştur
    generate_json_report "$output_dir" "$domain"
    
    echo ""
    log "INFO" "Keşif tamamlandı! Sonuçlar: $output_dir/"
}

# Scripti çalıştır
main "$@"
