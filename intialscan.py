#!/usr/bin/env python3

import subprocess
import os
import json
from concurrent.futures import ThreadPoolExecutor

# Define directories (configurable)
DEFAULT_RESULTS_DIR = "results"
DEFAULT_WORDLISTS_DIR = "wordlists"

def get_config_path():
    """
    Allows for a custom configuration file (optional).
    """
    config_path = os.path.join(os.path.expanduser("~"), ".pentest.conf")
    if os.path.isfile(config_path):
        # Parse configuration file (implementation left for customization)
        # You can use libraries like configparser to read and parse settings
        # Update results_dir and wordlists_dir based on config file
        pass
    return config_path

def get_results_dir():
    """
    Provides results directory path, considering configuration.
    """
    config_path = get_config_path()
    if config_path:
        # Use results_dir from config file if present
        pass
    else:
        return DEFAULT_RESULTS_DIR

def get_wordlists_dir():
    """
    Provides wordlists directory path, considering configuration.
    """
    config_path = get_config_path()
    if config_path:
        # Use wordlists_dir from config file if present
        pass
    else:
        return DEFAULT_WORDLISTS_DIR

# Ensure directories exist
results_dir = get_results_dir()
os.makedirs(results_dir, exist_ok=True)
wordlists_dir = get_wordlists_dir()
os.makedirs(wordlists_dir, exist_ok=True)

def run_command(command, output_file):
    """
    Improved error handling and output.
    """
    try:
        with open(output_file, "w") as f:
            completed_process = subprocess.run(command, stdout=f, stderr=subprocess.PIPE)
            if completed_process.returncode != 0:
                print(f"[-] Error running command '{' '.join(command)}': {completed_process.stderr.decode()}")
            else:
                print(f"[+] Command '{' '.join(command)}' completed successfully. Output saved in {output_file}")
    except Exception as e:
        print(f"[-] Error running command '{' '.join(command)}': {e}")

def run_nmap_scan(target):
    print(f"[*] Starting Nmap scan on {target}")
    nmap_command = ["nmap", "-A", "-T4", "--script=vuln", "-oN", os.path.join(results_dir, "nmap_scan.txt"), target]
    run_command(nmap_command, os.path.join(results_dir, "nmap_scan.txt"))

def run_nikto_scan(target):
    print(f"[*] Starting Nikto scan on {target}")
    nikto_command = ["nikto", "-h", target, "-output", os.path.join(results_dir, "nikto_scan.txt")]
    run_command(nikto_command, os.path.join(results_dir, "nikto_scan.txt"))

def run_openvas_scan(target):
    print(f"[*] Starting OpenVAS scan on {target}")
    openvas_command = ["gvm-cli", "socket", "--xml", f"<get_reports/>"]
    run_command(openvas_command, os.path.join(results_dir, "openvas_scan.txt"))

def run_sqlmap_scan(target):
    print(f"[*] Starting SQLMap scan on {target}")
    sqlmap_command = ["sqlmap", "-u", target, "--batch", "--output-dir=./sqlmap_output"]
    run_command(sqlmap_command, os.path.join(results_dir, "sqlmap_report.txt"))

def run_fuzzing_scan(target):
    print(f"[*] Starting Wfuzz scan on {target}")
    wfuzz_command = ["wfuzz", "-c", "-z", f"file,{os.path.join(wordlists_dir, 'common.txt')}", "--hc", "404", target]
    run_command(wfuzz_command, os.path.join(results_dir, "wfuzz_scan.txt"))

def run_hydra_scan(target, service, userlist, passlist):
    print(f"[*] Starting Hydra brute force on {target}")
    hydra_command = ["hydra", "-L", userlist, "-P", passlist, f"{target}", f"{service}", "-o", os.path.join(results_dir, "hydra_results.txt")]
    run_command(hydra_command, os.path.join(results_dir, "hydra_results.txt"))

def run_sslyze_scan(target):
    print(f"[*] Starting SSLyze scan on {target}")
    sslyze_command = ["sslyze", f"--regular", f"{target}"]
    run_command(sslyze_command, os.path.join(results_dir, "sslyze_scan.txt"))

def run_wpscan(target):
    print(f"[*] Starting WPScan on {target}")
    wpscan_command = ["wpscan", "--url", target, "--enumerate", "vp", "-o", os.path.join(results_dir, "wpscan_results.txt")]
    run_command(wpscan_command, os.path.join(results_dir, "wpscan_results.txt"))

def run_sublister_scan(target):
    print(f"[*] Starting Sublist3r scan on {target}")
    sublist3r_command = ["sublist3r", "-d", target, "-o", os.path.join(results_dir, "sublist3r_results.txt")]
    run_command(sublist3r_command, os.path.join(results_dir, "sublist3r_results.txt"))

def run_theharvester_scan(target):
    print(f"[*] Starting theHarvester scan on {target}")
    theharvester_command = ["theHarvester", "-d", target, "-l", "500", "-b", "all", "-f", os.path.join(results_dir, "theharvester_results.html")]
    run_command(theharvester_command, os.path.join(results_dir, "theharvester_results.html"))

def parse_outputs():
    print(f"[*] Parsing outputs")
    report = {}
    files_to_parse = {
        "nmap": "nmap_scan.txt",
        "nikto": "nikto_scan.txt",
        "openvas": "openvas_scan.txt",
        "sqlmap": "sqlmap_report.txt",
        "wfuzz": "wfuzz_scan.txt",
        "hydra": "hydra_results.txt",
        "sslyze": "sslyze_scan.txt",
        "wpscan": "wpscan_results.txt",
        "sublist3r": "sublist3r_results.txt",
        "theharvester": "theharvester_results.html"
    }
    
    for key, file in files_to_parse.items():
        file_path = os.path.join(results_dir, file)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                report[key] = f.read()
        else:
            report[key] = f"{file} not found or scan did not produce output."
    
    with open(os.path.join(results_dir, "final_report.json"), "w") as report_file:
        json.dump(report, report_file, indent=4)
    print(f"[*] Report generated: {os.path.join(results_dir, 'final_report.json')}")

def generate_metasploit_file(target):
    print(f"[*] Generating Metasploit-compatible file")
    metasploit_file_content = f"""# Metasploit
use auxiliary/scanner/http/dir_scanner
set RHOSTS {target}
run
"""
    with open(os.path.join(results_dir, "metasploit.rc"), "w") as msf_file:
        msf_file.write(metasploit_file_content)
    print(f"[*] Metasploit file generated: {os.path.join(results_dir, 'metasploit.rc')}")

def validate_target(target):
    """
    Improved validation with examples.
    """
    if target.startswith("http://") or target.startswith("https://"):
        return True
    elif target.replace(".", "").isdigit():
        # Consider adding further validation for valid IP formats (e.g., using ipaddress library)
        return True
    else:
        print("[-] Invalid target. Please enter a valid IP address or URL (starting with http:// or https://).")
        print("  For example: http://www.example.com, https://192.168.1.100, or 10.0.0.1")
        return False

def main():
    target = input("Enter the target IP or domain (with http:// or https:// if URL): ")

    if not validate_target(target):
        return

    # Check for wordlist files before proceeding
    wordlist_path = os.path.join(wordlists_dir, "common.txt")
    if not os.path.isfile(wordlist_path):
        print(f"[-] Wordlist file '{wordlist_path}' not found! Please make sure it is installed.")
        return

    # Adjust userlist and passlist paths based on your setup
    userlist_path = os.path.join(wordlists_dir, "top-usernames-shortlist.txt")
    passlist_path = os.path.join(wordlists_dir, "top-100.txt")
    if not os.path.isfile(userlist_path) or not os.path.isfile(passlist_path):
        print(f"[-] Userlist or password list file not found! Please make sure they are installed.")
        return

    # Use a thread pool for parallel execution
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(run_nmap_scan, target)
        executor.submit(run_nikto_scan, target)
        executor.submit(run_openvas_scan, target)
        executor.submit(run_sqlmap_scan, target)
        executor.submit(run_fuzzing_scan, target)
        executor.submit(run_hydra_scan, target, "http-post-form", userlist_path, passlist_path) # Adjust service as needed
        executor.submit(run_sslyze_scan, target)
        executor.submit(run_wpscan, target)
        executor.submit(run_sublister_scan, target)
        executor.submit(run_theharvester_scan, target)
    
    parse_outputs()
    generate_metasploit_file(target)

if __name__ == "__main__":
    main()
