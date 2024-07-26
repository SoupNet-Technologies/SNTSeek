import shodan
import tkinter as tk
from tkinter import ttk
import csv
from bs4 import BeautifulSoup
from tkinter import messagebox

API_KEY = "your key goes here"

api = shodan.Shodan(API_KEY)

def save_to_csv(results):
    """
    Save Shodan search results to a CSV file.
    """
    with open('shodan_results.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["IP", "Port", "OS", "Organization", "Data"])
        for result in results.get('matches', []):
            ip = result.get('ip_str', 'N/A')
            port = result.get('port', 'N/A')
            os = result.get('os', 'N/A')
            org = result.get('org', 'N/A')
            data = result.get('data', 'N/A')
            soup = BeautifulSoup(data, 'html.parser')
            cleaned_data = soup.get_text()
            writer.writerow([ip, port, os, org, cleaned_data])

def display_selected_item(event):
    """
    Display the detailed data of the selected item in the text view.
    """
    item = tree.focus()
    if item:
        values = tree.item(item, 'values')
        data = values[4]
        text_view.delete(1.0, tk.END)
        text_view.insert(tk.END, str(data).replace("More...\n\n", ""))

def perform_search():
    """
    Perform a search using the Shodan API and display results in the treeview.
    """
    query = entry.get().strip()
    if not query:
        messagebox.showwarning("Input Error", "Search query cannot be empty.")
        return
    
    try:
        results = api.search(query)
        save_to_csv(results)
        populate_tree(results)
    except shodan.APIError as e:
        messagebox.showerror("API Error", str(e))

def populate_tree(results):
    """
    Populate the treeview with search results.
    """
    tree.delete(*tree.get_children())
    for result in results.get('matches', []):
        ip = result.get('ip_str', 'N/A')
        port = result.get('port', 'N/A')
        os = result.get('os', 'N/A')
        org = result.get('org', 'N/A')
        data = result.get('data', 'N/A')
        hosts = result.get('hostnames', [])
        isp = result.get('isp', 'N/A')
        sho = result.get('_shodan', {})
        tree.insert("", tk.END, values=(ip, port, os, org, f"More...\n\nHostnames: {hosts}\nData: {data}\nISP: {isp}\nShodan: {sho}"))

def setup_gui():
    """
    Set up the GUI elements.
    """
    window = tk.Tk()
    window.title("SoupNet Technologies SEEK")
    window.geometry("800x600")

    label = tk.Label(window, text="Enter your search query:")
    label.pack(pady=5)

    global entry
    entry = tk.Entry(window, width=50)
    entry.pack(pady=5)

    button = tk.Button(window, text="Search", command=perform_search)
    button.pack(pady=5)

    global tree
    tree = ttk.Treeview(window, columns=("IP", "Port", "OS", "Organization", "Data"), show="headings")
    setup_treeview(tree)
    tree.pack(fill="both", expand=True, pady=5)
    
    global text_view
    text_view = tk.Text(window, height=10)
    text_view.pack(fill="both", expand=True, pady=5)
    setup_textview(text_view)

    window.mainloop()

def setup_treeview(tree):
    """
    Set up the treeview columns and scrollbar.
    """
    tree.heading("IP", text="IP")
    tree.column("IP", width=150, stretch=False)
    tree.heading("Port", text="Port")
    tree.column("Port", width=60, stretch=False)
    tree.heading("OS", text="OS")
    tree.column("OS", width=80, stretch=False)
    tree.heading("Organization", text="Organization")
    tree.column("Organization", width=150, stretch=False)
    tree.heading("Data", text="Data")
    tree.column("Data", width=300)

    treescrollbar = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
    treescrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=treescrollbar.set)
    tree.bind("<Double-1>", display_selected_item)

def setup_textview(text_view):
    """
    Set up the text view and its scrollbar.
    """
    datascrollbar = ttk.Scrollbar(text_view, orient="vertical", command=text_view.yview)
    datascrollbar.pack(side="right", fill="y")
    text_view.configure(yscrollcommand=datascrollbar.set)

if __name__ == "__main__":
    setup_gui()
