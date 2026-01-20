#!/bin/bash

# data_processor.sh
# Veri toplama ve işleme otomasyonu
# JSON-first yaklaşımı ile çıktı üretir.

set -e # Hata durumunda dur

echo_json() {
    local message="$1"
    local status="$2"
    echo "{\"message\": \"$message\", \"status\": \"$status\", \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}"
}

echo "Starting Data Processing..."

# Örnek: Log dosyalarını bul ve satır sayısını say
LOG_DIR="./logs"
OUTPUT_FILE="data_summary.json"

if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
    # Demo amaçlı dummy log oluştur
    echo "Sample log entry 1" > "$LOG_DIR/app.log"
    echo "Sample log entry 2" >> "$LOG_DIR/app.log"
fi

TOTAL_LOGS=$(find "$LOG_DIR" -type f | wc -l)
echo_json "Found logs" "processing"

# Process Substitution ile logları oku
while read -r log_file; do
    LINE_COUNT=$(wc -l < "$log_file")
    # JSON array elemanı gibi formatlayabiliriz (Basit örnek)
    echo "Processed $log_file: $LINE_COUNT lines" > /dev/null
done < <(find "$LOG_DIR" -type f)

# Sonuç üret
echo_json "Data processing complete" "success"

# JSON çıktısını dosyaya yaz (jq varsa formatla)
if command -v jq &> /dev/null; then
    echo_json "Processing finished" "completed" | jq . > "$OUTPUT_FILE"
else
    echo_json "Processing finished" "completed" > "$OUTPUT_FILE"
fi

echo "Output saved to $OUTPUT_FILE"
