import sys
import os
import platform
import shutil
import json

def check_system():
    """Checks the system environment and dependencies."""
    print("[\u2714] Initiating Self-Check Sequence...")

    # 1. OS Check
    os_name = platform.system()
    print(f"[\u2139] Operating System: {os_name} {platform.release()}")

    # 2. Python Version Check
    py_version = sys.version.split()[0]
    if sys.version_info < (3, 10):
        print(f"[\u274c] Python Version: {py_version} (Requires 3.10+)")
        return False
    else:
        print(f"[\u2705] Python Version: {py_version}")

    # 3. Directory Structure Check
    required_dirs = ["src", "docs", "specs", "src/templates"]
    missing_dirs = []
    base_path = os.getcwd() # Assuming running from root
    
    # Adjust base path if running from src/utils
    if os.path.basename(os.getcwd()) == "utils":
        base_path = os.path.dirname(os.path.dirname(os.getcwd()))

    for d in required_dirs:
        full_path = os.path.join(base_path, d)
        if not os.path.exists(full_path):
            missing_dirs.append(d)
    
    if missing_dirs:
        print(f"[\u26a0] Missing Directories: {', '.join(missing_dirs)}")
    else:
        print("[\u2705] Directory Structure: Verified")

    # 4. Git Check
    if shutil.which("git"):
        print("[\u2705] Git: Installed")
    else:
        print("[\u26a0] Git: Not found (Recommended for versioning)")

    print("[\u2714] Self-Check Completed Successfully.")
    return True

if __name__ == "__main__":
    check_system()
