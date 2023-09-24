import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import threading

class PenTestGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("All-in-One PenTest Tool")
        self.geometry("700x500")

        # Notebook Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Scan Tab
        self.scan_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.scan_frame, text="Scan")

        # History Tab (Placeholder for future use)
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="History")

        # Scan Options Frame
        self.options_frame = ttk.LabelFrame(self.scan_frame, text="Scan Options")
        self.options_frame.pack(pady=20, padx=20, fill="x")

        # Scan Type Dropdown
        self.scan_type = tk.StringVar()
        self.scan_type.set("Port Scan")  # default value
        ttk.Label(self.options_frame, text="Scan Type:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        ttk.Combobox(self.options_frame, textvariable=self.scan_type, values=["Port Scan", "Vulnerability Scan"]).grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Target Entry
        ttk.Label(self.options_frame, text="Enter Target:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.target_entry = ttk.Entry(self.options_frame)
        self.target_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Run Button
        ttk.Button(self.options_frame, text="Run Scan", command=self.run_scan).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        ttk.Button(self.options_frame, text="Clear Results", command=self.clear_results).grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Results Textbox
        self.results_text = tk.Text(self.scan_frame, wrap="word", height=10)
        self.results_text.pack(pady=10, fill="both", expand=True)

        # Save Button
        ttk.Button(self.scan_frame, text="Save Results", command=self.save_results).pack(pady=10)

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w")
        self.status_bar.pack(side="bottom", fill="x")

    def validate_input(self):
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showerror("Error", "Please enter a target!")
            return False
        # Add more validation logic if needed
        return True

    def run_scan(self):
        if not self.validate_input():
            return
        self.status_var.set("Scanning...")
        target = self.target_entry.get().strip()
        scan_type = self.scan_type.get()

        # Run scan in a separate thread
        threading.Thread(target=self.execute_scan, args=(target, scan_type)).start()

    def execute_scan(self, target, scan_type):
        # Placeholder logic; replace with actual scan logic
        if scan_type == "Port Scan":
            # Assuming 'port_scan_script.rb' is the Ruby script's name for port scanning
            result = subprocess.run(["ruby", "port_scan_script.rb", target], capture_output=True, text=True).stdout
        elif scan_type == "Vulnerability Scan":
            # Assuming 'vuln_scan_script.lua' is the Lua script's name for vulnerability scanning
            result = subprocess.run(["lua", "vuln_scan_script.lua", target], capture_output=True, text=True).stdout
        else:
            result = "Unknown scan type."

        # Display results in the textbox
        self.results_text.insert(tk.END, result)
        self.status_var.set("Scan completed!")

    def clear_results(self):
        self.results_text.delete(1.0, tk.END)

    def save_results(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write
