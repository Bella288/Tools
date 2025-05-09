import tkinter as tk
from tkinter import ttk


# Define conversion factors for each category
CONVERSIONS = {
    "Length": {
        "meters": {"meters": 1, "feet": 3.28084, "inches": 39.3701, "yards": 1.09361, "kilometers": 0.001, "miles": 0.000621371, "centimeters": 100, "millimeters": 1000},
        "feet": {"meters": 0.3048, "feet": 1, "inches": 12, "yards": 0.333333, "kilometers": 0.0003048, "miles": 0.000189394, "centimeters": 30.48, "millimeters": 304.8},
        "inches": {"meters": 0.0254, "feet": 0.0833333, "inches": 1, "yards": 0.0277778, "kilometers": 2.54e-5, "miles": 1.57828e-5, "centimeters": 2.54, "millimeters": 25.4},
        "yards": {"meters": 0.9144, "feet": 3, "inches": 36, "yards": 1, "kilometers": 0.0009144, "miles": 0.000568182, "centimeters": 91.44, "millimeters": 914.4},
        "kilometers": {"meters": 1000, "feet": 3280.84, "inches": 39370.1, "yards": 1093.61, "kilometers": 1, "miles": 0.621371, "centimeters": 100000, "millimeters": 1000000},
        "miles": {"meters": 1609.34, "feet": 5280, "inches": 63360, "yards": 1760, "kilometers": 1.60934, "miles": 1, "centimeters": 160934, "millimeters": 1609340},
        "centimeters": {"meters": 0.01, "feet": 0.0328084, "inches": 0.393701, "yards": 0.0109361, "kilometers": 0.00001, "miles": 0.00000621371, "centimeters": 1, "millimeters": 10},
        "millimeters": {"meters": 0.001, "feet": 0.00328084, "inches": 0.0393701, "yards": 0.00109361, "kilometers": 0.000001, "miles": 0.000000621371, "centimeters": 0.1, "millimeters": 1}
    },
    "Weight": {
        "kilograms": {"kilograms": 1, "grams": 1000, "pounds": 2.20462, "ounces": 35.274, "tons": 0.001, "stones": 0.157473},
        "grams": {"kilograms": 0.001, "grams": 1, "pounds": 0.00220462, "ounces": 0.035274, "tons": 0.000001, "stones": 0.000157473},
        "pounds": {"kilograms": 0.453592, "grams": 453.592, "pounds": 1, "ounces": 16, "tons": 0.0005, "stones": 0.0714286},
        "ounces": {"kilograms": 0.0283495, "grams": 28.3495, "pounds": 0.0625, "ounces": 1, "tons": 0.00003125, "stones": 0.00446429},
        "tons": {"kilograms": 1000, "grams": 1000000, "pounds": 2204.62, "ounces": 35274, "tons": 1, "stones": 157.143},
        "stones": {"kilograms": 6.35029, "grams": 6350.29, "pounds": 14, "ounces": 224, "tons": 0.00635029, "stones": 1}
    },
    "Energy": {
        "joules": {"joules": 1, "calories": 0.239006, "kilowatt-hours": 2.77778e-7, "kilojoules": 0.001, "megajoules": 1e-6, "watt-hours": 0.000277778},
        "calories": {"joules": 4.184, "calories": 1, "kilowatt-hours": 1.16222e-6, "kilojoules": 0.004184, "megajoules": 4.184e-6, "watt-hours": 0.00116222},
        "kilowatt-hours": {"joules": 3600000, "calories": 860421, "kilowatt-hours": 1, "kilojoules": 3600, "megajoules": 3.6, "watt-hours": 1000},
        "kilojoules": {"joules": 1000, "calories": 239.006, "kilowatt-hours": 0.000277778, "kilojoules": 1, "megajoules": 0.001, "watt-hours": 0.277778},
        "megajoules": {"joules": 1000000, "calories": 239006, "kilowatt-hours": 0.277778, "kilojoules": 1000, "megajoules": 1, "watt-hours": 277.778},
        "watt-hours": {"joules": 3600, "calories": 860.421, "kilowatt-hours": 0.001, "kilojoules": 3.6, "megajoules": 0.0036, "watt-hours": 1}
    },
    "Speed": {
        "meters_per_second": {"meters_per_second": 1, "kilometers_per_hour": 3.6, "miles_per_hour": 2.23694, "feet_per_second": 3.28084},
        "kilometers_per_hour": {"meters_per_second": 0.277778, "kilometers_per_hour": 1, "miles_per_hour": 0.621371, "feet_per_second": 0.911344},
        "miles_per_hour": {"meters_per_second": 0.44704, "kilometers_per_hour": 1.60934, "miles_per_hour": 1, "feet_per_second": 1.46667},
        "feet_per_second": {"meters_per_second": 0.3048, "kilometers_per_hour": 1.09728, "miles_per_hour": 0.681818, "feet_per_second": 1}
    },
    "Volume": {
        "liters": {"liters": 1, "gallons": 0.264172, "quarts": 1.05669, "cubic_meters": 0.001, "cubic_feet": 0.0353147},
        "gallons": {"liters": 3.78541, "gallons": 1, "quarts": 4, "cubic_meters": 0.00378541, "cubic_feet": 0.133681},
        "quarts": {"liters": 0.946353, "gallons": 0.25, "quarts": 1, "cubic_meters": 0.000946353, "cubic_feet": 0.0334201},
        "cubic_meters": {"liters": 1000, "gallons": 264.172, "quarts": 1056.69, "cubic_meters": 1, "cubic_feet": 35.3147},
        "cubic_feet": {"liters": 28.3168, "gallons": 7.48052, "quarts": 29.9221, "cubic_meters": 0.0283168, "cubic_feet": 1}
    },
    "Pressure": {
        "pascals": {"pascals": 1, "bars": 0.00001, "atmospheres": 0.00000986923, "psi": 0.000145038},
        "bars": {"pascals": 100000, "bars": 1, "atmospheres": 0.986923, "psi": 14.5038},
        "atmospheres": {"pascals": 101325, "bars": 1.01325, "atmospheres": 1, "psi": 14.6959},
        "psi": {"pascals": 6894.76, "bars": 0.0689476, "atmospheres": 0.068046, "psi": 1}
    },
    "Time": {
        "seconds": {"seconds": 1, "minutes": 0.0166667, "hours": 0.000277778, "days": 0.0000115741},
        "minutes": {"seconds": 60, "minutes": 1, "hours": 0.0166667, "days": 0.000694444},
        "hours": {"seconds": 3600, "minutes": 60, "hours": 1, "days": 0.0416667},
        "days": {"seconds": 86400, "minutes": 1440, "hours": 24, "days": 1}
    },
    "Temperature": {
        "celsius": {"celsius": 1, "fahrenheit": lambda x: x * 9/5 + 32, "kelvin": lambda x: x + 273.15},
        "fahrenheit": {"celsius": lambda x: (x - 32) * 5/9, "fahrenheit": 1, "kelvin": lambda x: (x - 32) * 5/9 + 273.15},
        "kelvin": {"celsius": lambda x: x - 273.15, "fahrenheit": lambda x: (x - 273.15) * 9/5 + 32, "kelvin": 1}
    }
}

class UnitConverterApp:
    
    def __init__(self, root):
        self.curr = 0
        self.curr += 1
        print(f"{self.curr} - Running '__init__()'")
        self.root = root
        self.root.title("Unit Converter")
        self.root.geometry("400x300")

        # Variables to store user inputs
        self.selected_category = tk.StringVar(value="Length")  # Default category
        
        self.input_value = tk.StringVar()
        self.origin_unit = tk.StringVar()
        self.target_unit = tk.StringVar()
        self.result = tk.StringVar()

        # Create the main menu
        self.create_menu()

        # Create the conversion frame
        self.create_conversion_frame()

    def create_menu(self):
        self.curr += 1
        print(f"{self.curr} - Running 'create_menu()'")
        """Create a menu to select the conversion category."""
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        category_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Select Category", menu=category_menu)

        for category in CONVERSIONS.keys():
            category_menu.add_command(
                label=category,
                command=lambda cat=category: self.update_conversion_options(cat)
            )

    def create_conversion_frame(self):
        self.curr += 1
        print(f"{self.curr} - Running 'create_conversion_frame()'")
        """Create the frame for input, selection, and result display."""
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Input value
        ttk.Label(frame, text="Value:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.input_value).grid(row=0, column=1, padx=5, pady=5)

        # Origin unit dropdown
        ttk.Label(frame, text="From:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.origin_unit_menu = ttk.Combobox(frame, textvariable=self.origin_unit, state="readonly")
        self.origin_unit_menu.grid(row=1, column=1, padx=5, pady=5)

        # Target unit dropdown
        ttk.Label(frame, text="To:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.target_unit_menu = ttk.Combobox(frame, textvariable=self.target_unit, state="readonly")
        self.target_unit_menu.grid(row=2, column=1, padx=5, pady=5)

        # Convert button
        ttk.Button(frame, text="Convert", command=self.perform_conversion).grid(row=3, column=0, columnspan=2, pady=10)

        # Result label
        ttk.Label(frame, text="Result:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(frame, textvariable=self.result).grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

    def update_conversion_options(self, category):
        self.curr += 1
        print(f"{self.curr} - Running 'update_conversion_options({category})'")
        """Update the dropdowns based on the selected category."""
        self.selected_category.set(category)
        units = list(CONVERSIONS[category].keys())
        self.origin_unit_menu["values"] = units
        self.target_unit_menu["values"] = units
        self.origin_unit.set(units[0])
        self.target_unit.set(units[1])

    def perform_conversion(self):
        self.curr += 1
        print(f"{self.curr} - Running 'perform_conversion()'")
        """Perform the conversion based on user inputs."""
        try:
            value = float(self.input_value.get())
            from_unit = self.origin_unit.get()
            to_unit = self.target_unit.get()
            category = self.selected_category.get()

            # Handle temperature conversions separately due to lambda functions
            if category == "Temperature":
                conversion_function = CONVERSIONS[category][from_unit][to_unit]
                result = conversion_function(value)
            else:
                # Get the conversion factor
                conversion_factor = CONVERSIONS[category][from_unit][to_unit]
                result = value * conversion_factor
            self.result.set(f"{result:.4f} {to_unit.replace('_', ' ').replace('-', ' ').title()}")
        except ValueError:
            self.result.set("Invalid input. Please enter a numeric value.")
        except KeyError:
            self.result.set("Unsupported conversion. Please check your units.")

if __name__ == "__main__":
    root = tk.Tk()
    app = UnitConverterApp(root)
    app.update_conversion_options("Length")
    root.mainloop()