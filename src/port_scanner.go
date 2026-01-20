// port_scanner.go - Go ile Hızlı Port Tarayıcı
// LAM-Action-Guard - Aziz Efe Çırak
//
// Yüksek performanslı, concurrent port tarama aracı

package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"net"
	"os"
	"sort"
	"sync"
	"time"
)

// Port tarama sonucu
type PortResult struct {
	Port    int    `json:"port"`
	State   string `json:"state"`
	Service string `json:"service,omitempty"`
}

// Tarama sonuçları
type ScanResult struct {
	Target    string       `json:"target"`
	ScanDate  string       `json:"scan_date"`
	OpenPorts []PortResult `json:"open_ports"`
	Duration  float64      `json:"duration_seconds"`
}

// Yaygın port servisleri
var commonServices = map[int]string{
	21:    "FTP",
	22:    "SSH",
	23:    "Telnet",
	25:    "SMTP",
	53:    "DNS",
	80:    "HTTP",
	110:   "POP3",
	135:   "MSRPC",
	139:   "NetBIOS",
	143:   "IMAP",
	443:   "HTTPS",
	445:   "SMB",
	993:   "IMAPS",
	995:   "POP3S",
	1433:  "MSSQL",
	1521:  "Oracle",
	3306:  "MySQL",
	3389:  "RDP",
	5432:  "PostgreSQL",
	5900:  "VNC",
	6379:  "Redis",
	8080:  "HTTP-Proxy",
	8443:  "HTTPS-Alt",
	27017: "MongoDB",
}

// Banner
func printBanner() {
	fmt.Println(`
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   LAM-Action-Guard - Port Scanner                         ║
║   Go High-Performance Network Tool v1.0                   ║
║   Author: Aziz Efe Çırak                                  ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝`)
}

// Port tarama işlevi
func scanPort(ctx context.Context, host string, port int, timeout time.Duration) *PortResult {
	address := fmt.Sprintf("%s:%d", host, port)
	
	dialer := net.Dialer{
		Timeout: timeout,
	}
	
	conn, err := dialer.DialContext(ctx, "tcp", address)
	if err != nil {
		return nil
	}
	defer conn.Close()
	
	result := &PortResult{
		Port:  port,
		State: "open",
	}
	
	// Servis adı ekle
	if service, ok := commonServices[port]; ok {
		result.Service = service
	}
	
	return result
}

// Paralel port tarama
func scanPorts(host string, startPort, endPort int, workers int, timeout time.Duration) []PortResult {
	var results []PortResult
	var mu sync.Mutex
	var wg sync.WaitGroup
	
	// Port kanalı oluştur
	portChan := make(chan int, workers)
	ctx := context.Background()
	
	// Worker'ları başlat
	for i := 0; i < workers; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for port := range portChan {
				if result := scanPort(ctx, host, port, timeout); result != nil {
					mu.Lock()
					results = append(results, *result)
					mu.Unlock()
					fmt.Printf("\r[+] Port %d açık (%s)                    \n", result.Port, result.Service)
				}
			}
		}()
	}
	
	// Portları kuyruğa ekle
	totalPorts := endPort - startPort + 1
	fmt.Printf("[*] %s üzerinde %d port taranıyor...\n\n", host, totalPorts)
	
	for port := startPort; port <= endPort; port++ {
		portChan <- port
	}
	close(portChan)
	
	// Tüm worker'ların bitmesini bekle
	wg.Wait()
	
	// Sonuçları sırala
	sort.Slice(results, func(i, j int) bool {
		return results[i].Port < results[j].Port
	})
	
	return results
}

// Sonuçları JSON olarak kaydet
func saveJSON(result ScanResult, filepath string) error {
	data, err := json.MarshalIndent(result, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(filepath, data, 0644)
}

// Özet yazdır
func printSummary(result ScanResult) {
	fmt.Println("\n" + "═══════════════════════════════════════════════════════════")
	fmt.Println("  TARAMA ÖZETİ")
	fmt.Println("═══════════════════════════════════════════════════════════")
	fmt.Printf("  Hedef: %s\n", result.Target)
	fmt.Printf("  Süre: %.2f saniye\n", result.Duration)
	fmt.Printf("  Açık Port Sayısı: %d\n", len(result.OpenPorts))
	
	if len(result.OpenPorts) > 0 {
		fmt.Println("\n  Açık Portlar:")
		for _, p := range result.OpenPorts {
			service := p.Service
			if service == "" {
				service = "unknown"
			}
			fmt.Printf("    - %d/tcp (%s)\n", p.Port, service)
		}
	} else {
		fmt.Println("\n  [!] Açık port bulunamadı")
	}
	fmt.Println("═══════════════════════════════════════════════════════════")
}

func main() {
	// Komut satırı argümanları
	var (
		target    string
		startPort int
		endPort   int
		workers   int
		timeout   int
		output    string
		topPorts  bool
	)
	
	flag.StringVar(&target, "target", "", "Hedef IP veya hostname (zorunlu)")
	flag.StringVar(&target, "t", "", "Hedef (kısa)")
	flag.IntVar(&startPort, "start", 1, "Başlangıç portu")
	flag.IntVar(&endPort, "end", 1024, "Bitiş portu")
	flag.IntVar(&workers, "workers", 100, "Paralel worker sayısı")
	flag.IntVar(&timeout, "timeout", 1, "Bağlantı timeout (saniye)")
	flag.StringVar(&output, "o", "", "JSON çıktı dosyası")
	flag.BoolVar(&topPorts, "top", false, "Sadece top 100 portu tara")
	
	flag.Parse()
	
	// Target kontrolü
	if target == "" {
		if flag.NArg() > 0 {
			target = flag.Arg(0)
		} else {
			printBanner()
			fmt.Println("\nKullanım: port_scanner -t <hedef> [seçenekler]")
			fmt.Println("\nÖrnekler:")
			fmt.Println("  port_scanner -t 192.168.1.1")
			fmt.Println("  port_scanner -t example.com -start 1 -end 65535 -workers 500")
			fmt.Println("  port_scanner -t 10.0.0.1 -top -o results.json")
			os.Exit(1)
		}
	}
	
	printBanner()
	
	// Top ports modu
	if topPorts {
		startPort = 1
		endPort = 1024
	}
	
	// Tarama başlat
	startTime := time.Now()
	
	results := scanPorts(target, startPort, endPort, workers, time.Duration(timeout)*time.Second)
	
	duration := time.Since(startTime).Seconds()
	
	// Sonuç oluştur
	scanResult := ScanResult{
		Target:    target,
		ScanDate:  time.Now().Format(time.RFC3339),
		OpenPorts: results,
		Duration:  duration,
	}
	
	// Özet yazdır
	printSummary(scanResult)
	
	// JSON kaydet
	if output != "" {
		if err := saveJSON(scanResult, output); err != nil {
			fmt.Printf("\n[!] JSON kaydetme hatası: %v\n", err)
		} else {
			fmt.Printf("\n[+] Sonuçlar kaydedildi: %s\n", output)
		}
	}
}
