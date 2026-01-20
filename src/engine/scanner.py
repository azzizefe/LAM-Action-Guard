import json
import os
import time

class Scanner:
    def __init__(self, templates_dir="src/templates"):
        self.templates_dir = templates_dir
        self.results = []

    def load_patterns(self, pattern_type):
        """Loads attack patterns from JSON files."""
        file_path = os.path.join(self.templates_dir, f"{pattern_type}_patterns.json")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[\u26a0] Pattern file not found: {file_path}")
            return []

    def scan_target(self, target, scan_type="all"):
        """
        Simulates scanning a target with loaded patterns.
        In a real scenario, this would send HTTP requests.
        """
        print(f"[\u2139] Starting scan on target: {target}")
        
        patterns_to_scan = []
        if scan_type in ["xss", "all"]:
            patterns_to_scan.extend(self.load_patterns("xss"))
        if scan_type in ["sqli", "all"]:
            patterns_to_scan.extend(self.load_patterns("sqli"))

        print(f"[\u2139] Loaded {len(patterns_to_scan)} patterns.")

        for pattern in patterns_to_scan:
            print(f"[\u23f3] Testing: {pattern['name']} ({pattern['id']})...", end="\r")
            time.sleep(0.5) # Simulate network delay
            
            # Mock Detection Logic
            # In real world: if pattern['payload'] in response.text:
            detected = False 
            if "test" in target and pattern['severity'] == "Critical":
                detected = True # Simulate finding critical bugs on test targets

            if detected:
                print(f"[\u2757] VULNERABILITY DETECTED: {pattern['name']}")
                self.results.append({
                    "target": target,
                    "vulnerability": pattern['name'],
                    "payload": pattern['payload'],
                    "severity": pattern['severity']
                })
            else:
                print(f"[\u2705] Clean: {pattern['name']}                            ")

        return self.results

    def generate_report(self):
        """Generates a JSON report of findings."""
        return json.dumps(self.results, indent=2)
