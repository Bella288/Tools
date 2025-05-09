import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import random
import time
import winsound

# For tooltips
import threading

# Define the folder path
folder_path = os.path.join(os.path.expanduser("~"), "Documents", "Name Lists")

# Check if the folder exists and create it if it doesn't
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    
class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in a tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, _cx, _cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 20
        y = y + self.widget.winfo_rooty() + 20
        # Creates a toplevel window 
        self.tipwindow = tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the window frame
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify="left",
                           background="#ffffe0", relief="solid", borderwidth=1,
                           font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def create_tooltip(widget, text):
    tooltip = ToolTip(widget)

    def enter(event):
        tooltip.showtip(text)

    def leave(event):
        tooltip.hidetip()

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)

class NameChooserApp:
    def __init__(self, master):
        self.master = master
        master.title("Name Chooser")

        self.names = []
        self.removed_names = []
        self.history = []

        self.create_widgets()

    def create_widgets(self):
        # Create the main frame
        main_frame = ttk.Frame(self.master)
        main_frame.pack(padx=10, pady=10)

        # Name listbox
        self.name_listbox = tk.Listbox(main_frame, selectmode=tk.SINGLE, width=30, height=10)
        self.name_listbox.pack(side=tk.LEFT, padx=10)

        # Scrollbar for listbox
        scrollbar = tk.Scrollbar(main_frame, command=self.name_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.name_listbox.config(yscrollcommand=scrollbar.set)

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.TOP)

        # Add button
        self.add_button = ttk.Button(button_frame, text="Add Name", command=self.add_name)
        self.add_button.pack(side=tk.LEFT, padx=5)
        create_tooltip(self.add_button, "Add a name to the list.")

        # Remove button
        self.remove_button = ttk.Button(button_frame, text="Remove Name", command=self.remove_name)
        self.remove_button.pack(side=tk.LEFT, padx=5)
        create_tooltip(self.remove_button, "Remove the selected name from the list.")

        # Choose button
        self.choose_button = ttk.Button(button_frame, text="Choose Name", command=self.choose_name)
        self.choose_button.pack(side=tk.LEFT, padx=5)
        create_tooltip(self.choose_button, "Randomly select a name from the list.")

        # Import button
        self.import_button = ttk.Button(button_frame, text="Import from File", command=self.import_names)
        self.import_button.pack(side=tk.LEFT, padx=5)
        create_tooltip(self.import_button, "Load names from a text file.")
        #Export Button
        self.export_button = ttk.Button(button_frame, text="Export Names to File", command=self.export_names)
        self.export_button.pack(side=tk.LEFT, padx=5)
        create_tooltip(self.export_button, "Save names to a text file.")
        # History listbox
        self.history_listbox = tk.Listbox(main_frame, selectmode=tk.SINGLE, width=30, height=10)
        self.history_listbox.pack(side=tk.RIGHT, padx=10)

        # Scrollbar for history listbox
        history_scrollbar = tk.Scrollbar(main_frame, command=self.history_listbox.yview)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_listbox.config(yscrollcommand=history_scrollbar.set)

        # Appearance options frame
        self.appearance_frame = ttk.Frame(self.master)
        self.appearance_frame.pack(padx=10, pady=10)

        # Background color option
        self.background_label = ttk.Label(self.appearance_frame, text="Background Color:")
        self.background_label.pack(side=tk.LEFT)

        self.background_var = tk.StringVar(self.appearance_frame)
        self.background_var.set("white")  # Default background

        self.background_options = ["white", "lightblue", "lightgray", "lightgreen", "lightpink"]
        self.background_dropdown = ttk.Combobox(self.appearance_frame, textvariable=self.background_var, values=self.background_options)
        self.background_dropdown.pack(side=tk.LEFT, padx=5)
        self.background_dropdown.bind("<<ComboboxSelected>>", self.update_appearance)

        # Font option
        self.font_label = ttk.Label(self.appearance_frame, text="Font:")
        self.font_label.pack(side=tk.LEFT)

        self.font_var = tk.StringVar(self.appearance_frame)
        self.font_var.set("Arial")  # Default font

        self.font_options = ["Arial", "Times New Roman", "Courier New", "Verdana"]
        self.font_dropdown = ttk.Combobox(self.appearance_frame, textvariable=self.font_var, values=self.font_options)
        self.font_dropdown.pack(side=tk.LEFT, padx=5)
        self.font_dropdown.bind("<<ComboboxSelected>>", self.update_appearance)

    def add_name(self):
        new_name = tk.simpledialog.askstring("Add Name", "Enter a new name:")
        if new_name:
            self.names.append(new_name)
            self.update_listbox()

    def remove_name(self):
        try:
            selected_index = self.name_listbox.curselection()[0]
            name_to_remove = self.name_listbox.get(selected_index)
            self.names.remove(name_to_remove)
            self.update_listbox()
        except IndexError:
            
            messagebox.showwarning("No Selection", "Please select a name to remove.")
            

    def choose_name(self):
        if self.names:
            # Choose a random name from the list
            choice = random.choice(self.names)

            # Check if the name has been chosen recently
            attempts = 0
            while attempts < 5:
                choice = random.choice(self.names)
                if choice not in self.removed_names[-3:]:
                    break
                attempts += 1

            if attempts == 5:
                choice = random.choice(self.names)

            self.removed_names.append(choice)  # Add to removed names
            self.names.remove(choice)  # Remove from the main list
            self.update_listbox()

            self.history.append(choice)
            self.update_history()

            # Play sound effect
            winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)

            # Display chosen name
            messagebox.showinfo("Chosen Name", f"The chosen name is: {choice}")
        else:
            messagebox.showerror("Error", "There are no names in the list. Please add names to the list.")
    def import_names(self):
        file_path = filedialog.askopenfilename(
            initialdir=os.path.join(os.path.expanduser("~"), "Documents", "Name Lists"),
            defaultextension=".txt",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )
        if file_path:
            with open(file_path, "r") as file:
                self.names = [line.strip() for line in file]
            self.update_listbox()
    def export_names(self):
        if self.names:
            file_path = filedialog.asksaveasfilename(
                initialfile="Untitled.txt",
                initialdir=os.path.join(os.path.expanduser("~"), "Documents", "Name Lists"),
                defaultextension=".txt",
                filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
            )
            if file_path:
                with open(file_path, "w") as file:
                    for l in self.names:
                        file.write(f"{l}\n")
                self.update_listbox()
        else:
            messagebox.showerror("Error", "There are no names to save. Please add names before trying to save.")
    def update_listbox(self):
        self.name_listbox.delete(0, tk.END)
        for name in self.names:
            self.name_listbox.insert(tk.END, name)

    def update_history(self):
        self.history_listbox.delete(0, tk.END)
        for name in self.history:
            self.history_listbox.insert(tk.END, name)

    def update_appearance(self, event=None):
        background_color = self.background_var.get()
        font_name = self.font_var.get()
        self.master.config(bg=background_color)
        self.name_listbox.config(bg=background_color, font=(font_name, 12))
        self.history_listbox.config(bg=background_color, font=(font_name, 12))

if __name__ == "__main__":
    root = tk.Tk()
    app = NameChooserApp(root)
    root.mainloop()