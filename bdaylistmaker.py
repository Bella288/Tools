import os
import json
import tkinter as tk
from tkinter import messagebox, simpledialog

def load_data(path):
    try:
        with open(path, "r") as blist:
            return json.load(blist)
    except FileNotFoundError:
        return []

def save_data(path, data):
    with open(path, "w") as blist:
        json.dump(data, blist, indent=4)

def add_item():
    item = simpledialog.askstring("Input", "What do you want to add?")
    if item:
        item = item.title()
        if item in blist_lines:
            messagebox.showinfo("Info", f"{item} is already in the list.")
        else:
            blist_lines.append(item)
            update_listbox()
            save_data(path, blist_lines)
            messagebox.showinfo("Success", f"Successfully added {item} to your list.")

def delete_item():
    try:
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            item = blist_lines.pop(index)
            update_listbox()
            save_data(path, blist_lines)
            messagebox.showinfo("Success", f"Successfully removed {item}.")
        else:
            messagebox.showinfo("Info", "Please select an item to delete.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def view_items():
    listbox.delete(0, tk.END)
    for item in blist_lines:
        listbox.insert(tk.END, item)

def update_listbox():
    listbox.delete(0, tk.END)
    for item in blist_lines:
        listbox.insert(tk.END, item)

def on_closing():
    save_data(path, blist_lines)
    root.destroy()

# Initialize the main window
root = tk.Tk()
root.title("Birthday List")

# Set up the path and load the data
path = os.path.join(os.path.expanduser("~"), "Documents", "bday_list_py.json")
blist_lines = load_data(path)

# Create and place the listbox
listbox = tk.Listbox(root, width=50, height=15)
listbox.pack(pady=20)

# Add the items to the listbox
update_listbox()

# Create and place the buttons
frame = tk.Frame(root)
frame.pack(pady=20)

add_button = tk.Button(frame, text="Add Item", command=add_item)
add_button.pack(side=tk.LEFT, padx=10)

delete_button = tk.Button(frame, text="Delete Item", command=delete_item)
delete_button.pack(side=tk.LEFT, padx=10)

view_button = tk.Button(frame, text="View Items", command=view_items)
view_button.pack(side=tk.LEFT, padx=10)

exit_button = tk.Button(frame, text="Save and Exit", command=on_closing)
exit_button.pack(side=tk.LEFT, padx=10)

# Configure the window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter event loop
root.mainloop()