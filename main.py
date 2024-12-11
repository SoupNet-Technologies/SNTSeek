import shodan
import tkinter as tk
from tkinter import ttk
import csv
from bs4 import BeautifulSoup
from tkinter import messagebox
import os
from dotenv import load_dotenv

class ShodanGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("SNT Seek")
        self.master.geometry("1000x700")

        load_dotenv()
        self.API_KEY = os.getenv("SHODAN_API_KEY")
        if not self.API_KEY:
            messagebox.showerror("API Key Error", "Shodan API key not found. Please set SHODAN_API_KEY in your environment variables.") # MARK: hi (:
            self.master.destroy()
            return

        self.api = shodan.Shodan(self.API_KEY)

        self.create_widgets()

    def create_widgets(self):
        search_frame = tk.Frame(self.master) # MARK: Search frame
        search_frame.pack(pady=10)

        label = tk.Label(search_frame, text="Enter your search query:")
        label.pack(side=tk.LEFT, padx=5)

        self.entry = tk.Entry(search_frame, width=50)
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind("<Return>", lambda event: self.perform_search())

        search_button = tk.Button(search_frame, text="Search", command=self.perform_search)
        search_button.pack(side=tk.LEFT, padx=5)

        results_frame = tk.Frame(self.master) # MARK: Results frame
        results_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(results_frame, columns=("IP", "Port", "Hostnames", "Organization", "ISP"), show="headings")
        self.setup_treeview()
        self.tree.pack(side=tk.LEFT, fill="both", expand=True)

        treescrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.tree.yview)
        treescrollbar.pack(side=tk.LEFT, fill="y")
        self.tree.configure(yscrollcommand=treescrollbar.set)

        details_frame = tk.Frame(self.master) # MARK: Details frame
        details_frame.pack(fill="both", expand=True, padx=10, pady=5)

        detail_label = tk.Label(details_frame, text="Details:")
        detail_label.pack(anchor="w")

        self.text_view = tk.Text(details_frame, height=15)
        self.text_view.pack(fill="both", expand=True)

        textscrollbar = ttk.Scrollbar(self.text_view, orient="vertical", command=self.text_view.yview)
        textscrollbar.pack(side="right", fill="y")
        self.text_view.configure(yscrollcommand=textscrollbar.set)

        button_frame = tk.Frame(self.master) # MARK: Buttons frame
        button_frame.pack(pady=5)

        save_button = tk.Button(button_frame, text="Save Results", command=self.save_results, state=tk.DISABLED)
        save_button.pack()
        self.save_button = save_button  # keep reference to enable/disable

        self.status_var = tk.StringVar()
        self.status_label = tk.Label(self.master, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_treeview(self): # MARK: setup_treeview
        self.tree.heading("IP", text="IP")
        self.tree.column("IP", width=150, stretch=False)
        self.tree.heading("Port", text="Port")
        self.tree.column("Port", width=60, stretch=False)
        self.tree.heading("Hostnames", text="Hostnames")
        self.tree.column("Hostnames", width=200, stretch=False)
        self.tree.heading("Organization", text="Organization")
        self.tree.column("Organization", width=200, stretch=False)
        self.tree.heading("ISP", text="ISP")
        self.tree.column("ISP", width=200, stretch=False)

        self.tree.bind("<<TreeviewSelect>>", self.display_selected_item)

    def perform_search(self): # MARK: perform_search
        query = self.entry.get().strip()
        if not query:
            messagebox.showwarning("Input Error", "Search query cannot be empty.")
            return

        self.status_var.set("Searching...")
        self.master.update_idletasks()
        try:
            results = self.api.search(query)
            self.populate_tree(results)
            self.results = results  # Store results for saving
            self.save_button.config(state=tk.NORMAL)
            self.status_var.set(f"Search completed: {results['total']} results found.")
        except shodan.APIError as e:
            messagebox.showerror("API Error", str(e))
            self.status_var.set("Error occurred during search.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("Error occurred during search.")

    def populate_tree(self, results): # MARK: populate_tree
        self.tree.delete(*self.tree.get_children())
        for result in results.get('matches', []):
            ip = result.get('ip_str', 'N/A')
            port = result.get('port', 'N/A')
            hostnames = ', '.join(result.get('hostnames', []))
            org = result.get('org', 'N/A')
            isp = result.get('isp', 'N/A')
            item_id = self.tree.insert("", tk.END, values=(ip, port, hostnames, org, isp))
            self.tree.set(item_id, 'data', result)

    def display_selected_item(self, event): # MARK: display_selected_item
        selected_item = self.tree.selection()
        if selected_item:
            item_id = selected_item[0]
            result = self.tree.set(item_id, 'data')
            if result:
                import ast
                result = ast.literal_eval(result)

                data = result.get('data', '')
                cleaned_data = BeautifulSoup(data, 'html.parser').get_text()

                details = [
                    f"IP: {result.get('ip_str', 'N/A')}",
                    f"Port: {result.get('port', 'N/A')}",
                    f"Hostnames: {', '.join(result.get('hostnames', []))}",
                    f"Organization: {result.get('org', 'N/A')}",
                    f"ISP: {result.get('isp', 'N/A')}",
                    f"Location: {self.format_location(result.get('location', {}))}",
                    f"\nBanner Data:\n{cleaned_data}"
                ]

                self.text_view.delete(1.0, tk.END)
                self.text_view.insert(tk.END, '\n'.join(details))

    def format_location(self, location): # MARK: format_location
        components = []
        if 'city' in location and location['city']:
            components.append(location['city'])
        if 'region_code' in location and location['region_code']:
            components.append(location['region_code'])
        if 'country_name' in location and location['country_name']:
            components.append(location['country_name'])
        return ', '.join(components) if components else 'N/A'

    def save_results(self): # MARK: save_results
        from tkinter.filedialog import asksaveasfilename
        file_path = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")], title="Save results as")
        if not file_path:
            return
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["IP", "Port", "Hostnames", "Organization", "ISP", "Location", "Data"])
                for result in self.results.get('matches', []):
                    ip = result.get('ip_str', 'N/A')
                    port = result.get('port', 'N/A')
                    hostnames = ', '.join(result.get('hostnames', []))
                    org = result.get('org', 'N/A')
                    isp = result.get('isp', 'N/A')
                    location = self.format_location(result.get('location', {}))
                    data = result.get('data', '')
                    cleaned_data = BeautifulSoup(data, 'html.parser').get_text()
                    writer.writerow([ip, port, hostnames, org, isp, location, cleaned_data])
            messagebox.showinfo("Success", f"Results saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Save Error", f"An error occurred while saving: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShodanGUI(root)
    root.mainloop()