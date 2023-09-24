import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading

class PenTestGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("All-in-One PenTest Tool")
        self.geometry("700x500")

        # Scan Options Frame
        self.options_frame = ttk.LabelFrame(self, text="Scan Options")
        self.options_frame.pack(pady=20, padx=20, fill="x")

        # Scan Type Dropdown
        self.scan_type = tk.StringVar()
        self.scan_type.set("Nmap Scan")  # default value
        ttk.Label(self.options_frame, text="Scan Type:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.scan_type_combobox = ttk.Combobox(self.options_frame, textvariable=self.scan_type, values=["Nmap Scan", "Gobuster Scan", "Sn1per Scan"])
        self.scan_type_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.scan_type_combobox.bind("<<ComboboxSelected>>", self.update_sub_options)

        # Sub-options Dropdown
        self.sub_option = tk.StringVar()
        ttk.Label(self.options_frame, text="Sub Option:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.sub_option_combobox = ttk.Combobox(self.options_frame, textvariable=self.sub_option)
        self.sub_option_combobox.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Target Entry
        ttk.Label(self.options_frame, text="Enter Target:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.target_entry = ttk.Entry(self.options_frame)
        self.target_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Run Button
        ttk.Button(self.options_frame, text="Run Scan", command=self.run_scan).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        ttk.Button(self.options_frame, text="Clear Results", command=self.clear_results).grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Results Textbox
        self.results_text = tk.Text(self, wrap="word", height=10)
        self.results_text.pack(pady=10, fill="both", expand=True)

    def update_sub_options(self, event):
        scan_type = self.scan_type.get()
        if scan_type == "Nmap Scan":
            self.sub_option_combobox['values'] = ["Quick Scan", "Full Scan", "Service Version Detection", "OS Detection", "Aggressive Scan"]
        elif scan_type == "Gobuster Scan":
            self.sub_option_combobox['values'] = ["Directory Scan", "File Scan", "DNS Subdomain Brute-forcing"]
        elif scan_type == "Sn1per Scan":
            self.sub_option_combobox['values'] = ["Basic Scan", "Full Scan", "Domain Scan"]
        self.sub_option.set(self.sub_option_combobox['values'][0])

    def run_scan(self):
        target = self.target_entry.get().strip()
        scan_type = self.scan_type.get()
        sub_option = self.sub_option.get()

        # Run scan in a separate thread
        threading.Thread(target=self.execute_scan, args=(target, scan_type, sub_option)).start()

    def execute_scan(self, target, scan_type, sub_option):
        if scan_type == "Nmap Scan":
            nmap_path = "/usr/bin/nmap"
            if sub_option == "Quick Scan":
                result = subprocess.run([nmap_path, "-F", target], capture_output=True, text=True).stdout
            elif sub_option == "Full Scan":
                result = subprocess.run([nmap_path, target], capture_output=True, text=True).stdout
            # ... [Add other Nmap options here]
        elif scan_type == "Gobuster Scan":
            gobuster_path = "/usr/bin/gobuster"
            if sub_option == "Directory Scan":
                result = subprocess.run([gobuster_path, "dir", "-u", target], capture_output=True, text=True).stdout
            elif sub_option == "File Scan":
                result = subprocess.run([gobuster_path, "file", "-u", target], capture_output=True, text=True).stdout
            elif sub_option == "DNS Subdomain Brute-forcing":
                result = subprocess.run([gobuster_path, "dns", "-d", target], capture_output=True, text=True).stdout
            else:
                result = "Unknown Gobuster scan type."
        elif scan_type == "Sn1per Scan":
            sniper_path = "/usr/bin/sniper"
            if sub_option == "Basic Scan":
                result = subprocess.run([sniper_path, "-t", target, "-m", "basic"], capture_output=True, text=True).stdout
            elif sub_option == "Full Scan":
                result = subprocess.run([sniper_path, "-t", target, "-m", "full"], capture_output=True, text=True).stdout
            elif sub_option == "Domain Scan":
                result = subprocess.run([sniper_path, "-t", target, "-m", "domain"], capture_output=True, text=True).stdout
            else:
                result = "Unknown Sn1per scan type."
        else:
            result = "Unknown scan type."

        # Display results in the textbox
        self.results_text.insert(tk.END, result)

    def clear_results(self):
        self.results_text.delete(1.0, tk.END)

if __name__ == "__main__":
    app = PenTestGUI()
    app.mainloop()
