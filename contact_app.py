import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel

file_path = os.path.join(os.path.expanduser("~"), "Documents", "contacts.json")

def load():
    if not os.path.exists(file_path):
        open(file_path, "w").close()  # Create an empty file if it doesn't exist
        items = []
    else:
        with open(file_path, "r") as file:
            try:
                items = json.load(file)
            except json.JSONDecodeError:  # Handle the case where the file is empty or not a valid JSON
                items = []
    return items

def save(items):
    # Sort the items by Last Name
    items.sort(key=lambda x: x.get("Last Name", "").lower())
    with open(file_path, "w") as file:
        json.dump(items, file, indent=4)

def add_contact(root):
    def submit():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        phone_numbers = phone_entry.get().split(", ")
        emails = email_entry.get().split(", ")
        bd = bd_entry.get() or "Unknown"
        website = website_entry.get() or "None"
        note = note_entry.get() or "None"
        rel = rel_entry.get()

        item = {
            "First Name": first_name,
            "Last Name": last_name,
            "Phone Numbers": phone_numbers if phone_numbers and phone_numbers[0] else ["None"],
            "Emails": emails if emails and emails[0] else ["None"],
            "Birthday": bd,
            "Website": website,
            "Note": note,
            "Relationship": rel
        }

        add_bonus = True
        while add_bonus:
            to_do = simpledialog.askstring("Add Field", "Do you want to add another field? (Y/N)").upper()
            if to_do == "N":
                add_bonus = False
            else:
                title = simpledialog.askstring("Add Field", "Enter the field title, make sure to capitalize as you see fit!")
                entry = simpledialog.askstring("Add Field", f"Enter the value of the field '{title}'")
                item[title] = entry

        items = load()
        items.append(item)
        save(items)
        messagebox.showinfo("Success", "Contact added successfully!")
        add_window.destroy()

    add_window = Toplevel(root)
    add_window.title("Add Contact")

    tk.Label(add_window, text="First Name:").grid(row=0, column=0, padx=5, pady=5)
    first_name_entry = tk.Entry(add_window)
    first_name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(add_window, text="Last Name:").grid(row=1, column=0, padx=5, pady=5)
    last_name_entry = tk.Entry(add_window)
    last_name_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(add_window, text="Phone Numbers (comma separated):").grid(row=2, column=0, padx=5, pady=5)
    phone_entry = tk.Entry(add_window)
    phone_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(add_window, text="Emails (comma separated):").grid(row=3, column=0, padx=5, pady=5)
    email_entry = tk.Entry(add_window)
    email_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(add_window, text="Birthday (MM/DD/YYYY):").grid(row=4, column=0, padx=5, pady=5)
    bd_entry = tk.Entry(add_window)
    bd_entry.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(add_window, text="Website:").grid(row=5, column=0, padx=5, pady=5)
    website_entry = tk.Entry(add_window)
    website_entry.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(add_window, text="Note:").grid(row=6, column=0, padx=5, pady=5)
    note_entry = tk.Entry(add_window)
    note_entry.grid(row=6, column=1, padx=5, pady=5)

    tk.Label(add_window, text="Relationship:").grid(row=7, column=0, padx=5, pady=5)
    rel_entry = tk.Entry(add_window)
    rel_entry.grid(row=7, column=1, padx=5, pady=5)

    submit_button = tk.Button(add_window, text="Submit", command=submit)
    submit_button.grid(row=8, columnspan=2, pady=10)

def edit_contact(root):
    items = load()
    if not items:
        messagebox.showinfo("Info", "No contacts to edit.")
        return

    global selected_index
    selected_index = None

    def submit_edit():
        if selected_index is not None:
            selected_contact = items[selected_index]
            selected_contact["First Name"] = first_name_entry.get()
            selected_contact["Last Name"] = last_name_entry.get()
            selected_contact["Phone Numbers"] = phone_entry.get().split(", ") if phone_entry.get() else ["None"]
            selected_contact["Emails"] = email_entry.get().split(", ") if email_entry.get() else ["None"]
            selected_contact["Birthday"] = bd_entry.get() or "Unknown"
            selected_contact["Website"] = website_entry.get() or "None"
            selected_contact["Note"] = note_entry.get() or "None"
            selected_contact["Relationship"] = rel_entry.get()

            save(items)
            messagebox.showinfo("Success", "Contact edited successfully!")
            edit_window.destroy()
        else:
            messagebox.showwarning("Warning", "No contact selected.")

    def on_select(event):
        global selected_index
        selected_indices = contact_listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            selected_contact = items[selected_index]
            first_name_entry.delete(0, tk.END)
            first_name_entry.insert(0, selected_contact.get("First Name", ""))
            last_name_entry.delete(0, tk.END)
            last_name_entry.insert(0, selected_contact.get("Last Name", ""))
            phone_entry.delete(0, tk.END)
            phone_entry.insert(0, ", ".join(selected_contact.get("Phone Numbers", ["None"])))
            email_entry.delete(0, tk.END)
            email_entry.insert(0, ", ".join(selected_contact.get("Emails", ["None"])))
            bd_entry.delete(0, tk.END)
            bd_entry.insert(0, selected_contact.get("Birthday", "Unknown"))
            website_entry.delete(0, tk.END)
            website_entry.insert(0, selected_contact.get("Website", "None"))
            note_entry.delete(0, tk.END)
            note_entry.insert(0, selected_contact.get("Note", "None"))
            rel_entry.delete(0, tk.END)
            rel_entry.insert(0, selected_contact.get("Relationship", ""))

    edit_window = Toplevel(root)
    edit_window.title("Edit Contact")

    contact_listbox = tk.Listbox(edit_window, height=10, width=50)
    contact_listbox.pack(pady=10)
    for contact in items:
        contact_listbox.insert(tk.END, f"{contact.get('First Name', 'Unknown')} {contact.get('Last Name', 'Unknown')}")

    contact_listbox.bind('<<ListboxSelect>>', on_select)

    tk.Label(edit_window, text="First Name:").pack(padx=5, pady=5)
    first_name_entry = tk.Entry(edit_window)
    first_name_entry.pack(padx=5, pady=5)

    tk.Label(edit_window, text="Last Name:").pack(padx=5, pady=5)
    last_name_entry = tk.Entry(edit_window)
    last_name_entry.pack(padx=5, pady=5)

    tk.Label(edit_window, text="Phone Numbers (comma separated):").pack(padx=5, pady=5)
    phone_entry = tk.Entry(edit_window)
    phone_entry.pack(padx=5, pady=5)

    tk.Label(edit_window, text="Emails (comma separated):").pack(padx=5, pady=5)
    email_entry = tk.Entry(edit_window)
    email_entry.pack(padx=5, pady=5)

    tk.Label(edit_window, text="Birthday (MM/DD/YYYY):").pack(padx=5, pady=5)
    bd_entry = tk.Entry(edit_window)
    bd_entry.pack(padx=5, pady=5)

    tk.Label(edit_window, text="Website:").pack(padx=5, pady=5)
    website_entry = tk.Entry(edit_window)
    website_entry.pack(padx=5, pady=5)

    tk.Label(edit_window, text="Note:").pack(padx=5, pady=5)
    note_entry = tk.Entry(edit_window)
    note_entry.pack(padx=5, pady=5)

    tk.Label(edit_window, text="Relationship:").pack(padx=5, pady=5)
    rel_entry = tk.Entry(edit_window)
    rel_entry.pack(padx=5, pady=5)

    submit_button = tk.Button(edit_window, text="Submit", command=submit_edit)
    submit_button.pack(pady=10)

def remove_contact(root):
    items = load()
    if not items:
        messagebox.showinfo("Info", "No contacts to remove.")
        return

    def confirm_remove():
        selected_indices = contact_listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            removed_contact = items.pop(selected_index)
            save(items)
            messagebox.showinfo("Success", f"Contact '{removed_contact.get('First Name', 'Unknown')} {removed_contact.get('Last Name', 'Unknown')}' removed successfully.")
            remove_window.destroy()

    remove_window = Toplevel(root)
    remove_window.title("Remove Contact")

    contact_listbox = tk.Listbox(remove_window, height=10, width=50)
    contact_listbox.pack(pady=10)
    for contact in items:
        contact_listbox.insert(tk.END, f"{contact.get('First Name', 'Unknown')} {contact.get('Last Name', 'Unknown')}")

    remove_button = tk.Button(remove_window, text="Remove", command=confirm_remove)
    remove_button.pack(pady=10)

def view_contact(root):
    items = load()
    if not items:
        messagebox.showinfo("Info", "No contacts to view.")
        return

    def display_contact():
        selected_indices = contact_listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            selected_contact = items[selected_index]
            contact_info = (
                f"First Name: {selected_contact.get('First Name', 'Unknown')}\n"
                f"Last Name: {selected_contact.get('Last Name', 'Unknown')}\n"
                f"Phone Numbers: {', '.join(selected_contact.get('Phone Numbers', ['None']))}\n"
                f"Emails: {', '.join(selected_contact.get('Emails', ['None']))}\n"
                f"Birthday: {selected_contact.get('Birthday', 'Unknown')}\n"
                f"Website: {selected_contact.get('Website', 'None')}\n"
                f"Note: {selected_contact.get('Note', 'None')}\n"
                f"Relationship: {selected_contact.get('Relationship', '')}\n"
                f"Related People: {selected_contact.get('Related People', '')}\n"
                f"Sexuality: {selected_contact.get('Sexuality', '')}\n"
            )
            messagebox.showinfo("Contact Info", contact_info)

    view_window = Toplevel(root)
    view_window.title("View Contact")

    contact_listbox = tk.Listbox(view_window, height=10, width=50)
    contact_listbox.pack(pady=10)
    for contact in items:
        contact_listbox.insert(tk.END, f"{contact.get('First Name', 'Unknown')} {contact.get('Last Name', 'Unknown')}")

    view_button = tk.Button(view_window, text="View", command=display_contact)
    view_button.pack(pady=10)

def mainloop():
    root = tk.Tk()
    root.title("Contact Manager")

    frame = tk.Frame(root)
    frame.pack(pady=20)

    add_button = tk.Button(frame, text="Add Contact", command=lambda: add_contact(root))
    add_button.grid(row=0, column=0, padx=10, pady=5)

    edit_button = tk.Button(frame, text="Edit Contact", command=lambda: edit_contact(root))
    edit_button.grid(row=0, column=1, padx=10, pady=5)

    remove_button = tk.Button(frame, text="Remove Contact", command=lambda: remove_contact(root))
    remove_button.grid(row=0, column=2, padx=10, pady=5)

    view_button = tk.Button(frame, text="View Contact", command=lambda: view_contact(root))
    view_button.grid(row=0, column=3, padx=10, pady=5)

    exit_button = tk.Button(frame, text="Exit", command=root.quit)
    exit_button.grid(row=0, column=4, padx=10, pady=5)

    root.mainloop()

# Example usage
mainloop()