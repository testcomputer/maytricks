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
        ttk.Combobox(self.options_frame, textvariable=self.scan_type, values=["Nmap Scan", "Gobuster Scan", "Sn1per Scan"]).grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Target Entry
        ttk.Label(self.options_frame, text="Enter Target:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.target_entry = ttk.Entry(self.options_frame)
        self.target_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Run Button
        ttk.Button(self.options_frame, text="Run Scan", command=self.run_scan).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        ttk.Button(self.options_frame, text="Clear Results", command=self.clear_results).grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Results Textbox
        self.results_text = tk.Text(self, wrap="word", height=10)
        self.results_text.pack(pady=10, fill="both", expand=True)

    def run_scan(self):
        target = self.target_entry.get().strip()
        scan_type = self.scan_type.get()

        # Run scan in a separate thread
        threading.Thread(target=self.execute_scan, args=(target, scan_type)).start()

    def execute_scan(self, target, scan_type):
        if scan_type == "Nmap Scan":
            result = subprocess.run(["nmap", target], capture_output=True, text=True).stdout
        elif scan_type == "Gobuster Scan":
            # Modify the command as per your requirements
            result = subprocess.run(["gobuster", "dir", "-u", target], capture_output=True, text=True).stdout
        elif scan_type == "Sn1per Scan":
            # Modify the command as per your requirements
            result = subprocess.run(["sniper", target], capture_output=True, text=True).stdout
        else:
            result = "Unknown scan type."

        # Display results in the textbox
        self.results_text.insert(tk.END, result)

    def clear_results(self):
        self.results_text.delete(1.0, tk.END)

if __name__ == "__main__":
    app = PenTestGUI()
    app.mainloop()
