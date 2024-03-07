import shodan
import tkinter as tk
from tkinter import ttk
import csv
from bs4 import BeautifulSoup

api = shodan.Shodan(API_KEY)

API_KEY = "your key goes here"

def save_to_csv(results):
    with open('shodan_results.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["IP", "Port", "OS", "Organization", "Data"])
        for result in results['matches']:
            ip, port, os, org, data = result['ip_str'], result['port'], result['os'], result['org'], result['data']
            soup = BeautifulSoup(data, 'html.parser')
            cleaned_data = soup.get_text()
            writer.writerow([ip, port, os, org, cleaned_data])

def display_selected_item(event):
    item = tree.focus()
    values = tree.item(item, 'values')
    data = values[4]
    text_view.delete(1.0, tk.END)
    text_view.insert(tk.END, str(data).replace("More...\n\n", ""))

def perform_search():
    query = entry.get()
    try:
        results = api.search(query)
        save_to_csv(results)
        tree.delete(*tree.get_children())
        for result in results['matches']:
            ip, port, os, org, data = result['ip_str'], result['port'], result['os'], result['org'], result['data']
            hosts, isp, sho = result['hostnames'], result['isp'], result['_shodan']
            tree.insert("", tk.END, values=(ip, port, os, org, "More...\n\nHostnames: " + str(hosts) + "\nData: " + data + "\nISP: " + isp + "\nShodan: " + str(sho)))

    except shodan.APIError as e:
        tree.delete(*tree.get_children())
        tree.insert("", tk.END, values=("Error", "", "", str(e)))

window = tk.Tk()
window.title("SoupNet Technologies SEEK")
window.geometry("800x400")

label = tk.Label(window, text="Enter your search query:")
label.pack()
entry = tk.Entry(window)
entry.pack()

button = tk.Button(window, text="Search", command=perform_search)
button.pack()

tree = ttk.Treeview(window, columns=("IP", "Port", "OS", "Organization", "Data"), show="headings")
tree.heading("IP", text="IP")
tree.column("IP", width=100, stretch=False)
tree.heading("Port", text="Port")
tree.column("Port", width=60, stretch=False)
tree.heading("OS", text="OS")
tree.column("OS", width=80)
tree.heading("Organization", text="Organization")
tree.heading("Data", text="Data")
tree.column("Data", width=80, stretch=False)
tree.pack(fill="both", expand=True)
treescrollbar = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
treescrollbar.pack(side="right", fill="y")
tree.configure(yscrollcommand=treescrollbar.set)
tree.bind("<Double-1>", display_selected_item)

text_view = tk.Text(window, height=10)
text_view.pack(fill="both", expand=True)
datascrollbar = ttk.Scrollbar(text_view, orient="vertical", command=text_view.yview)
datascrollbar.pack(side="right", fill="y")
text_view.configure(yscrollcommand=datascrollbar.set)

window.mainloop()
