from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import requests
import datetime as dt_
from tkinter import Tk, Label, Entry, Button, Text, Checkbutton, IntVar, messagebox, filedialog, Listbox
from tkinter.ttk import Combobox
import json
from pathlib import Path

# Initialize geolocator with a higher timeout
geolocator = Nominatim(user_agent="true_way.py", timeout=10)
mids = []

# Define the path to the Documents folder and the Routes folder
documents_folder = Path.home() / "Documents"
routes_folder = documents_folder / "Routes"
routes_folder.mkdir(parents=True, exist_ok=True)

# Function to save route to a file
def save_route(route_data, filename):
    route_file = routes_folder / filename
    with open(route_file, 'w') as f:
        json.dump(route_data, f, indent=4)
    messagebox.showinfo("Success", f"Route saved to {route_file}")

# Function to load route from a file
def load_route(filename):
    route_file = routes_folder / filename
    if route_file.exists():
        with open(route_file, 'r') as f:
            return json.load(f)
    else:
        messagebox.showerror("Error", f"Route file {route_file} does not exist.")
        return None

# Function to display route steps
def display_route(steps, total_distance_miles, total_distance_feet, total_duration_seconds):
    route_text.delete(1.0, 'end')
    route_text.insert('end', f"Total Distance: {total_distance_miles:.2f} miles ({total_distance_feet:.2f} feet)\n")
    route_text.insert('end', f"Total Duration: {dt_.timedelta(seconds=total_duration_seconds)}\n\n")
    
    for i, step in enumerate(steps, 1):
        if not isinstance(step, dict):
            route_text.insert('end', f"Step {i} is not a dictionary. Skipping...\n")
            continue
        
        distance_meters = step.get('distance', 0)
        distance_feet = distance_meters * 3.281
        distance_miles = distance_feet / 5280
        duration_seconds = step.get('duration', 0)
        instruction = step.get('instruction', {}).get('text', 'Continue')
        maneuver_type = step.get('maneuver', {}).get('type', 'unknown')
        instruction_before = step.get('instruction', {}).get('text_before', '')
        instruction_after = step.get('instruction', {}).get('text_after', '')
        road_class = step.get('road_class', 'unknown')
        road_name = step.get('name', 'unknown')
        surface = step.get('surface', 'unknown')
        speed_limit = step.get('speed_limit', 'unknown')
        
        detailed_instruction = f"{instruction}"
        if maneuver_type != "unknown":
            detailed_instruction += f" (Maneuver Type: {maneuver_type})"
        if instruction_before:
            detailed_instruction += f" (Before: {instruction_before})"
        if instruction_after:
            detailed_instruction += f" (After: {instruction_after})"
        
        route_text.insert('end', f"Step {i}:\n")
        route_text.insert('end', f"  Instructions: {detailed_instruction}\n")
        route_text.insert('end', f"  Distance: {distance_miles:.2f} miles ({distance_feet:.2f} feet)\n")
        route_text.insert('end', f"  Duration: {dt_.timedelta(seconds=duration_seconds)}\n")
        if road_class != "unknown":
            route_text.insert('end', f"  Road Class: {road_class}\n")
        if road_name != "unknown":
            route_text.insert('end', f"  Road Name: {road_name}\n")
        if surface != "unknown":
            route_text.insert('end', f"  Surface: {surface}\n")
        if speed_limit != "unknown":
            route_text.insert('end', f"  Speed Limit: {speed_limit/1.609:.0f} mph ({speed_limit} km/h)\n")
        route_text.insert('end', "-" * 40 + "\n")

# Function to handle route calculation
def calculate_route():
    global mids
    start_address = start_entry.get()
    end_address = end_entry.get()
    
    try:
        start_location = geolocator.geocode(start_address)
        if not start_location:
            messagebox.showerror("Error", "Could not find start location.")
            return

        end_location = geolocator.geocode(end_address)
        if not end_location:
            messagebox.showerror("Error", "Could not find end location.")
            return

        coordinates = f"{start_location.latitude},{start_location.longitude}"
        for mid in mids:
            mid_location = geolocator.geocode(mid)
            if mid_location:
                coordinates += f"|{mid_location.latitude},{mid_location.longitude}"
            else:
                messagebox.showerror("Error", f"Could not find midway location: {mid}")
                return
        coordinates += f"|{end_location.latitude},{end_location.longitude}"

        mode = mode_combobox.get().lower()
        if mode == "truck":
            truck_type = truck_type_combobox.get().lower().replace(" ", "_")
            if truck_type == "go_back":
                truck_back()
            elif truck_type == "truck_with_dangerous_goods":
                mode = "truck_dangerous_goods"
            else:
                mode = truck_type.lower()
        else:
            if mode == "car driving":
                mode = "drive"
            elif mode == "motorcycle":
                mode = "motorcycle"
            elif mode == "city bicycle":
                mode = "bicycle"
            elif mode == "regular bike":
                mode = "road_bike"
            elif mode == "walk":
                mode = "walk"
            elif mode == "hike":
                mode = "hike"
            elif mode == "scooter":
                mode = "scooter"
        avoid = []
        if avoid_highways_var.get():
            avoid.append("highways")
        if avoid_tolls_var.get():
            avoid.append("tolls")
        if avoid_ferries_var.get():
            avoid.append("ferries")

        url = "https://api.geoapify.com/v1/routing"
        querystring = {
            "waypoints": coordinates,
            "mode": mode,
            "apiKey": "1b386166e02e413589f3230fe67a6f7b",  # Replace with your actual Geoapify API key
            "details": "instruction_details,route_details"
        }
        if avoid:
            querystring["avoid"] = ",".join(avoid)
        print(f"""
              Start: {start_address}
              End: {end_address}
              Midways: {mids}
              Avoid: {avoid}
              URL: https://api.geoapify.com/v1/routing?mode={mode}&apiKey=1b386166e02e413589f3230fe67a6f7b&details=instruction_details,route_details&waypoints={coordinates}
              ----
              """)
        response = requests.get(url, params=querystring)
        response_json = response.json()

        if response.status_code == 200:
            features = response_json.get('features', [])
            if features:
                feature = features[0]
                properties = feature.get('properties', {})
                legs = properties.get('legs', [])
                if legs:
                    steps = legs[0].get('steps', [])
                    
                    total_distance_meters = properties.get('distance', 0)
                    total_distance_feet = total_distance_meters * 3.281
                    total_distance_miles = total_distance_feet / 5280
                    total_duration_seconds = properties.get('time', 0)
                    
                    display_route(steps, total_distance_miles, total_distance_feet, total_duration_seconds)
                    
                    # Save the route
                    route_name = route_name_entry.get().strip()
                    if route_name:
                        route_data = {
                            "steps": steps,
                            "total_distance_miles": total_distance_miles,
                            "total_distance_feet": total_distance_feet,
                            "total_duration_seconds": total_duration_seconds
                        }
                        save_route(route_data, f"{route_name}.json")
                    else:
                        messagebox.showinfo("Info", "Route not saved as no name was provided.")
                else:
                    messagebox.showerror("Error", "No legs found in the route.")
            else:
                messagebox.showerror("Error", "No features found.")
        else:
            messagebox.showerror("Error", f"Error: {response.status_code} - {response_json.get('message', 'Unknown error')} (Input: {mode})")
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        messagebox.showerror("Error", f"Geocoding service error: {str(e)}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Request error: {str(e)}")

def truck_back():
    mode_combobox.grid()
    truck_type_combobox.grid_remove()

# Function to add midway point
def add_midway():
    midway = midway_entry.get()
    if midway:
        mids.append(midway)
        midway_entry.delete(0, 'end')
        midway_listbox.insert('end', midway)

# Function to load route
def load_route_from_file():
    file_path = filedialog.askopenfilename(initialdir=str(routes_folder), filetypes=[("JSON files", "*.json")])
    if file_path:
        route_data = load_route(Path(file_path).name)
        if route_data:
            display_route(route_data['steps'], route_data['total_distance_miles'], route_data['total_distance_feet'], route_data['total_duration_seconds'])

# Create the main window
root = Tk()
root.title("True Way Route Planner")

# Create and place widgets
Label(root, text="Start Location:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
start_entry = Entry(root, width=50)
start_entry.grid(row=0, column=1, padx=10, pady=5)

Label(root, text="End Location:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
end_entry = Entry(root, width=50)
end_entry.grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Midway Locations:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
midway_entry = Entry(root, width=30)
midway_entry.grid(row=2, column=1, padx=10, pady=5)
Button(root, text="Add Midway", command=add_midway).grid(row=2, column=2, padx=10, pady=5)

midway_listbox = Listbox(root, width=50, height=5)
midway_listbox.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

Label(root, text="Mode of Transport:").grid(row=4, column=0, padx=10, pady=5, sticky='w')
mode_combobox = Combobox(root, values=["Car Driving", "Motorcycle", "City Bicycle", "Regular Bike", "Walk", "Hike", "Truck", "Scooter"], width=48)
mode_combobox.grid(row=4, column=1, padx=10, pady=5)
mode_combobox.current(0)

truck_type_combobox = Combobox(root, values=["Regular truck", "Medium truck", "Truck", "Heavy truck", "Truck with dangerous goods", "Long truck", "Go Back"], width=48)
truck_type_combobox.grid(row=4, column=1, padx=10, pady=5)
truck_type_combobox.grid_remove()

def on_mode_change():
    if mode_combobox.get().lower() == "truck":
        truck_type_combobox.grid()
    else:
        truck_type_combobox.grid_remove()

mode_combobox.bind("<<ComboboxSelected>>", on_mode_change)

avoid_highways_var = IntVar()
avoid_tolls_var = IntVar()
avoid_ferries_var = IntVar()

Checkbutton(root, text="Avoid Highways", variable=avoid_highways_var).grid(row=5, column=0, padx=10, pady=5, sticky='w')
Checkbutton(root, text="Avoid Tolls", variable=avoid_tolls_var).grid(row=5, column=1, padx=10, pady=5, sticky='w')
Checkbutton(root, text="Avoid Ferries", variable=avoid_ferries_var).grid(row=5, column=2, padx=10, pady=5, sticky='w')

Button(root, text="Calculate Route", command=calculate_route).grid(row=6, column=0, columnspan=3, pady=10)

Label(root, text="Route Name:").grid(row=7, column=0, padx=10, pady=5, sticky='w')
route_name_entry = Entry(root, width=50)
route_name_entry.grid(row=7, column=1, padx=10, pady=5)

Button(root, text="Load Route", command=load_route_from_file).grid(row=8, column=0, columnspan=3, pady=10)

route_text = Text(root, width=80, height=20)
route_text.grid(row=9, column=0, columnspan=3, padx=10, pady=5)

# Run the application
root.mainloop()