import os
import json
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from tkinter.scrolledtext import ScrolledText

PATH = os.path.join(os.path.expanduser("~"), "Documents", "movies.json")

# Global variables
items = []
current_sort_type = None  # To track the current sorting type

def load_movies():
    global items
    try:
        with open(PATH, "r") as file:
            items = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        items = []
        save_movies()
    update_movie_list()

def save_movies():
    with open(PATH, "w") as file:
        json.dump(items, file, indent=4)

def update_movie_list():
    movie_list.delete(0, tk.END)
    for item in items:
        # Display the title and watched status
        status = "✅ Watched" if item["watched"] else "❌ Unwatched"
        
        # Include additional details based on the current sort type
        if current_sort_type == "running_time":
            display_text = f"{item['title']} ({status}) - Running Time: {item['running_time']} min"
        elif current_sort_type == "director":
            display_text = f"{item['title']} ({status}) - Director: {item['director']}"
        else:
            # Handle "The" prefix for display
            title = item["title"]
            if title.startswith("The "):
                # Rearrange "The" to the end for display
                title_parts = title.split(" ", 1)
                display_title = f"{title_parts[1]}, The"
            else:
                display_title = title
            display_text = f"{display_title} ({status})"
        
        movie_list.insert(tk.END, display_text)

def search_movie():
    search_term = simpledialog.askstring("Search", "Enter movie title to search:")
    if not search_term:
        return

    search_term_lower = search_term.lower()
    found_movies = [item for item in items if search_term_lower in item["title"].lower()]

    if found_movies:
        for movie in found_movies:
            response = messagebox.askyesno("Movie Found", f"Title: {movie['title']}\nDirector: {movie['director']}\nWatched: {movie['watched']}\n\nMark as watched?")
            if response:
                movie["watched"] = True
                save_movies()
                update_movie_list()  # Refresh the list
    else:
        response = messagebox.askyesno("Movie Not Found", f"Movie '{search_term}' not found. Add it?")
        if response:
            add_movie(search_term)

def add_movie(title=""):
    print("Adding a new movie...")
    dialog = MovieDialog(root, "Add Movie", title)
    root.wait_window(dialog.top)

    if dialog.result:
        new_movie = {
            "title": dialog.result["title"],
            "director": dialog.result["director"],
            "part_of_series": dialog.result["part_of_series"],
            "in_series": dialog.result["in_series"],
            "series_index": dialog.result["series_index"],
            "running_time": dialog.result["running_time"],
            "notes": dialog.result["notes"],
            "format": dialog.result["format"],
            "redeemed_on": dialog.result["redeemed_on"],
            "rating": dialog.result["rating"],
            "watched": dialog.result["watched"]
        }
        items.append(new_movie)
        save_movies()
        update_movie_list()

def delete_movie():
    selected_index = movie_list.curselection()
    if not selected_index:
        messagebox.showwarning("Delete Movie", "No movie selected!")
        return

    movie_title = movie_list.get(selected_index)
    response = messagebox.askyesno("Delete Movie", f"Are you sure you want to delete '{movie_title}'?")
    if response:
        global items
        items = [item for item in items if item["title"] != movie_title]
        save_movies()
        update_movie_list()

def show_movie_details():
    selected_index = movie_list.curselection()
    if not selected_index:
        messagebox.showwarning("Show Details", "No movie selected!")
        return

    print("Showing movie details...")
    # Get the selected movie from the list, which includes the watched status
    selected_movie_with_status = movie_list.get(selected_index)
    print(f"Selected movie with status: {selected_movie_with_status}")

    # Extract the actual movie title by splitting the string
    # Assuming the format is: "Title (✅ Watched)" or "Title (❌ Unwatched)"
    movie_title = selected_movie_with_status.split(" (")[0]  # Removes the status part
    print(f"Extracted movie title: {movie_title}")

    # Find the movie in the items list using the extracted title
    movie = next((item for item in items if item["title"] == movie_title), None)
    if movie:
        details = f"Title: {movie['title']}\nDirector: {movie['director']}\nPart of Series: {'Yes' if movie['part_of_series'] else 'No'}\nSeries: {movie['in_series']}\nSeries Index: {movie['series_index']}\nRunning Time: {movie['running_time']} minutes\nNotes: {movie['notes']}\nFormat: {movie['format']}\nRedeemed On: {movie['redeemed_on']}\nRating: {movie['rating']}\nWatched: {'Yes' if movie['watched'] else 'No'}"
        messagebox.showinfo("Movie Details", details)
    else:
        print("Movie not found in items!")
        messagebox.showerror("Show Details", "The selected movie could not be found in the database.")

def edit_movie():
    selected_index = movie_list.curselection()
    if not selected_index:
        messagebox.showwarning("Edit Movie", "No movie selected!")
        return

    print("Editing a movie...")
    # Get the selected movie from the list, which includes the watched status
    selected_movie_with_status = movie_list.get(selected_index)
    print(f"Selected movie with status: {selected_movie_with_status}")

    # Extract the actual movie title by splitting the string
    # Assuming the format is: "Title (✅ Watched)" or "Title (❌ Unwatched)"
    movie_title = selected_movie_with_status.split(" (")[0]  # Removes the status part
    print(f"Extracted movie title: {movie_title}")

    # Find the movie in the items list using the extracted title
    movie = next((item for item in items if item["title"] == movie_title), None)
    if movie:
        print("Found movie in items:", movie)
        dialog = MovieDialog(root, "Edit Movie", movie=movie)
        root.wait_window(dialog.top)

        if dialog.result:
            movie.update(dialog.result)
            save_movies()
            update_movie_list()
    else:
        print("Movie not found in items!")
        messagebox.showerror("Edit Movie", "The selected movie could not be found in the database.")

# Sorting Functions
def sort_by_name():
    global items, current_sort_type
    current_sort_type = "name"
    
    # Sort by name, handling "The" prefix
    items.sort(key=lambda x: x["title"][4:].strip() if x["title"].startswith("The ") else x["title"])
    update_movie_list()

def sort_by_running_time():
    global items, current_sort_type
    current_sort_type = "running_time"
    items.sort(key=lambda x: x["running_time"])
    update_movie_list()

def sort_by_director():
    global items, current_sort_type
    current_sort_type = "director"
    items.sort(key=lambda x: x["director"])
    update_movie_list()

# Custom Dialog Class for Adding/Editing Movies
class MovieDialog:
    def __init__(self, parent, title, movie=None, title_value=""):
        self.parent = parent
        self.movie = movie
        self.result = None

        print("Initializing MovieDialog...")
        print(f"Title: {title}")
        print(f"Movie: {movie}")

        # Create the dialog window
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.transient(parent)
        self.top.grab_set()

        # Define options for dropdowns
        formats = ["DVD", "DVD + Digital", "Blu-Ray", "Blu-Ray + Digital", "HD-DVD", "HD-DVD + Digital", "Digital"]
        platforms = ["Movies Anywhere", "Fandango at Home (Vudu)", "Amazon", "iTunes", "Universal", "Lionsgate", "None"]

        # Initialize variables
        self.title_var = tk.StringVar(value=title_value)
        self.director_var = tk.StringVar()
        self.part_of_series_var = tk.BooleanVar()
        self.in_series_var = tk.StringVar()
        self.series_index_var = tk.IntVar()
        self.running_time_var = tk.IntVar()
        self.notes_var = tk.StringVar()
        self.format_var = tk.StringVar(value=formats[0])
        self.redeemed_on_var = tk.StringVar(value=platforms[0])
        self.rating_var = tk.IntVar()
        self.watched_var = tk.BooleanVar()

        # Populate fields with existing movie data if editing
        if movie:
            self.title_var.set(movie["title"])
            self.director_var.set(movie["director"])
            self.part_of_series_var.set(movie["part_of_series"])
            self.in_series_var.set(movie["in_series"])
            self.series_index_var.set(movie["series_index"])
            self.running_time_var.set(movie["running_time"])
            self.notes_var.set(movie["notes"])
            self.format_var.set(movie["format"])
            self.redeemed_on_var.set(movie["redeemed_on"])
            self.rating_var.set(movie["rating"])
            self.watched_var.set(movie["watched"])

        # Create and layout widgets
        self.create_widgets(formats, platforms)

    def create_widgets(self, formats, platforms):
        # Title
        tk.Label(self.top, text="Title:").grid(row=0, column=0, sticky="w")
        tk.Entry(self.top, textvariable=self.title_var).grid(row=0, column=1, sticky="ew")

        # Director
        tk.Label(self.top, text="Director:").grid(row=1, column=0, sticky="w")
        tk.Entry(self.top, textvariable=self.director_var).grid(row=1, column=1, sticky="ew")

        # Part of Series
        tk.Label(self.top, text="Part of Series:").grid(row=2, column=0, sticky="w")
        tk.Checkbutton(self.top, variable=self.part_of_series_var).grid(row=2, column=1, sticky="w")

        # Series Name
        tk.Label(self.top, text="Series Name:").grid(row=3, column=0, sticky="w")
        tk.Entry(self.top, textvariable=self.in_series_var).grid(row=3, column=1, sticky="ew")

        # Series Index
        tk.Label(self.top, text="Series Index:").grid(row=4, column=0, sticky="w")
        tk.Spinbox(self.top, textvariable=self.series_index_var, from_=1, to=100).grid(row=4, column=1, sticky="ew")

        # Running Time
        tk.Label(self.top, text="Running Time (minutes):").grid(row=5, column=0, sticky="w")
        tk.Spinbox(self.top, textvariable=self.running_time_var, from_=1, to=1000).grid(row=5, column=1, sticky="ew")

        # Notes
        tk.Label(self.top, text="Notes:").grid(row=6, column=0, sticky="w")
        tk.Entry(self.top, textvariable=self.notes_var).grid(row=6, column=1, sticky="ew")

        # Format
        tk.Label(self.top, text="Format:").grid(row=7, column=0, sticky="w")
        ttk.Combobox(self.top, textvariable=self.format_var, values=formats).grid(row=7, column=1, sticky="ew")

        # Redeemed On
        tk.Label(self.top, text="Redeemed On:").grid(row=8, column=0, sticky="w")
        ttk.Combobox(self.top, textvariable=self.redeemed_on_var, values=platforms).grid(row=8, column=1, sticky="ew")

        # Rating
        tk.Label(self.top, text="Rating:").grid(row=9, column=0, sticky="w")
        tk.Spinbox(self.top, textvariable=self.rating_var, from_=1, to=5).grid(row=9, column=1, sticky="ew")

        # Watched
        tk.Label(self.top, text="Watched:").grid(row=10, column=0, sticky="w")
        tk.Checkbutton(self.top, variable=self.watched_var).grid(row=10, column=1, sticky="w")

        # Buttons
        tk.Button(self.top, text="OK", command=self.ok).grid(row=11, column=0, sticky="ew")
        tk.Button(self.top, text="Cancel", command=self.cancel).grid(row=11, column=1, sticky="ew")

    def ok(self):
        # Validate and store the result
        self.result = {
            "title": self.title_var.get(),
            "director": self.director_var.get(),
            "part_of_series": self.part_of_series_var.get(),
            "in_series": self.in_series_var.get(),
            "series_index": self.series_index_var.get(),
            "running_time": self.running_time_var.get(),
            "notes": self.notes_var.get(),
            "format": self.format_var.get(),
            "redeemed_on": self.redeemed_on_var.get(),
            "rating": self.rating_var.get(),
            "watched": self.watched_var.get()
        }
        self.top.destroy()

    def cancel(self):
        self.top.destroy()

# Create the main window
root = tk.Tk()
root.title("Movie Cataloger")
root.geometry("600x400")

# Create a frame for the movie list
frame = ttk.Frame(root)
frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Create a scrollbar and listbox
scrollbar = ttk.Scrollbar(frame, orient="vertical")
movie_list = tk.Listbox(frame, yscrollcommand=scrollbar.set, width=50, height=15)
scrollbar.config(command=movie_list.yview)

scrollbar.pack(side="right", fill="y")
movie_list.pack(side="left", fill="both", expand=True)

# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=root.quit)

# Movie Menu
movie_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Movie", menu=movie_menu)
movie_menu.add_command(label="Search", command=search_movie)
movie_menu.add_command(label="Add", command=add_movie)
movie_menu.add_command(label="Delete", command=delete_movie)
movie_menu.add_command(label="Show Details", command=show_movie_details)
movie_menu.add_command(label="Edit", command=edit_movie)

# View Menu
view_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Sort by Name", command=sort_by_name)
view_menu.add_command(label="Sort by Running Time", command=sort_by_running_time)
view_menu.add_command(label="Sort by Director", command=sort_by_director)

# Load movies on startup
load_movies()

# Run the main loop
root.mainloop()