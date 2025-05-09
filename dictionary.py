import requests as req
import json as js
from tkinter import messagebox as mb, Tk, Label, Entry, Button, Text, Scrollbar, END, Toplevel
import time
import threading
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
DEBUG = False
# Flask application setup
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a model for storing data
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), nullable=False)
    value = db.Column(db.JSON, nullable=False)

    def to_dict(self):
        return {"id": self.id, "key": self.key, "value": self.value}

# Create the database and the database table
with app.app_context():
    db.create_all()

@app.route('/data', methods=['GET'])
def get_data():
    """Endpoint to retrieve all data."""
    data = Data.query.all()
    return jsonify([item.to_dict() for item in data])

@app.route('/data', methods=['POST'])
def post_data():
    """Endpoint to add data."""
    if request.is_json:
        data = request.get_json()
        # Clear existing data
        Data.query.delete()
        db.session.commit()
        # Add new data
        for entry in data:
            new_data = Data(key=entry.get('key'), value=entry.get('value'))
            db.session.add(new_data)
        db.session.commit()
        return jsonify({"message": "Data updated successfully!"}), 201
    else:
        return jsonify({"error": "Request must be JSON"}), 400

@app.route('/data/<string:key>', methods=['DELETE'])
def delete_data(key):
    """Endpoint to delete an entry by key."""
    entry = Data.query.filter_by(key=key).first()
    if entry:
        db.session.delete(entry)
        db.session.commit()
        return jsonify({"message": f"Entry '{key}' deleted successfully!"}), 200
    else:
        return jsonify({"error": f"Entry '{key}' not found!"}), 404

# Function to run the Flask app in a separate thread
def run_flask_app():
    app.run(debug=True, use_reloader=False)

# Function to append a new entry to the API
def append_entry(post_to, new_entry):
    try:
        # Fetch existing data
        response = req.get(post_to)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()

        # Debugging: Print the existing data
        print("Existing Data:")
        print(js.dumps(data, indent=2))

        # Append the new entry
        data.append(new_entry)

        # Print the data being sent for debugging
        print("Data being sent:")
        print(js.dumps(data, indent=2))

        # Set headers
        headers = {
            'Content-Type': 'application/json'
        }

        # Send the updated list back to the API using a POST request
        response = req.post(post_to, json=data, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        print("Entry added successfully!")
    except req.exceptions.ConnectionError as e:
        print(f"The connection was reset. Please try again later.\n{e}")
        if DEBUG:
            print(response.text)
        time.sleep(100)
    except req.exceptions.HTTPError as e:
        print(f"HTTP Error: {e} - Response: {response.text}")
        if DEBUG:
            print(response.text)
        time.sleep(100)
    except req.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        if DEBUG:
            print(response.text)
        time.sleep(100)
    except ValueError as e:
        print(f"Invalid JSON response: {e}")
        time.sleep(100)

# Function to create a new entry
def create_new_entry():
    def submit():
        if DEBUG:
            # Create a test entry
            new_entry = {
                "key": "Test",
                "value": {
                    "pronunciation": "Test",
                    "definitions": [
                        {
                            "form": "Test",
                            "definition": "Test",
                            "example": "Test",
                            "flag": "Test"
                        }
                    ]
                }
            }
            append_entry(endpoint, new_entry)
            add_window.destroy()
            return

        word_to_add = word_entry.get().strip()
        pronounce = pronounce_entry.get().strip()
        forms = []
        form = form_entry.get().strip()
        defin = defin_entry.get().strip()
        example = example_entry.get().strip()
        flag = flag_entry.get().strip()
        
        while form.lower() != "q":
            if form and defin and example and flag:
                forms.append({
                    "form": form,
                    "definition": defin,
                    "example": example,
                    "flag": flag
                })
            form = form_entry.get().strip()
            defin = defin_entry.get().strip()
            example = example_entry.get().strip()
            flag = flag_entry.get().strip()

        if forms:
            new_entry = {
                "key": word_to_add,
                "value": {
                    "pronunciation": pronounce,
                    "definitions": forms,
                }
            }
            append_entry(endpoint, new_entry)
            add_window.destroy()

    add_window = Toplevel(root)
    add_window.title("Add New Entry")

    Label(add_window, text="Enter the new word:").grid(row=0, column=0, padx=10, pady=5)
    word_entry = Entry(add_window)
    word_entry.grid(row=0, column=1, padx=10, pady=5)

    Label(add_window, text="Enter the IPA pronunciation:").grid(row=1, column=0, padx=10, pady=5)
    pronounce_entry = Entry(add_window)
    pronounce_entry.grid(row=1, column=1, padx=10, pady=5)

    Label(add_window, text="Enter the form of the word:").grid(row=2, column=0, padx=10, pady=5)
    form_entry = Entry(add_window)
    form_entry.grid(row=2, column=1, padx=10, pady=5)

    Label(add_window, text="Enter the definition for this form:").grid(row=3, column=0, padx=10, pady=5)
    defin_entry = Entry(add_window)
    defin_entry.grid(row=3, column=1, padx=10, pady=5)

    Label(add_window, text="Enter an example of this form:").grid(row=4, column=0, padx=10, pady=5)
    example_entry = Entry(add_window)
    example_entry.grid(row=4, column=1, padx=10, pady=5)

    Label(add_window, text="Enter the flag for this form:").grid(row=5, column=0, padx=10, pady=5)
    flag_entry = Entry(add_window)
    flag_entry.grid(row=5, column=1, padx=10, pady=5)

    Button(add_window, text="Submit", command=submit).grid(row=6, column=0, columnspan=2, pady=10)

# Function to search entries
def search_entries():
    def search():
        to_find = search_entry.get().strip().lower()
        try:
            response = req.get(endpoint)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()

            found = False
            for entry in data:
                if entry.get('key', '').strip().lower() == to_find:
                    result_text.delete(1.0, END)
                    result_text.insert(END, f"Word: {entry['key']}\n")
                    result_text.insert(END, f"Pronunciation: {entry['value']['pronunciation']}\n")
                    result_text.insert(END, "Definitions:\n")
                    for definition in entry['value']['definitions']:
                        result_text.insert(END, f"  Form: {definition['form']}\n")
                        result_text.insert(END, f"  Definition: {definition['definition']}\n")
                        result_text.insert(END, f"  Example: {definition['example']}\n")
                        result_text.insert(END, f"  Flag: {definition['flag']}\n")
                    
                    found = True
                    break
            if not found:
                result_text.delete(1.0, END)
                result_text.insert(END, f"No entry found for the word: {to_find}\n")
                add_it_new = mb.askyesno("Entry Not Found", "Add it?")
                if add_it_new:
                    create_new_entry()
        except req.exceptions.HTTPError as e:
            mb.showerror("HTTP Error", f"HTTP Error: {e} - Response: {response.text}")
            if DEBUG:
                print(response.text)
            time.sleep(100)
        except req.exceptions.RequestException as e:
            mb.showerror("Request Error", f"An error occurred: {e}")
            if DEBUG:
                print(response.text)
            time.sleep(100)
        except ValueError as e:
            mb.showerror("JSON Error", f"Invalid JSON response: {e}")
            if DEBUG:
                print(response.text)
            time.sleep(100)

    search_window = Toplevel(root)
    search_window.title("Search Entries")

    Label(search_window, text="Enter the word to find:").grid(row=0, column=0, padx=10, pady=5)
    search_entry = Entry(search_window)
    search_entry.grid(row=0, column=1, padx=10, pady=5)

    Button(search_window, text="Search", command=search).grid(row=1, column=0, columnspan=2, pady=10)

    result_text = Text(search_window, height=10, width=50)
    result_text.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    scrollbar = Scrollbar(search_window, command=result_text.yview)
    scrollbar.grid(row=2, column=2, sticky="ns")
    result_text.config(yscrollcommand=scrollbar.set)

# Function to delete an entry
def delete_entry():
    def delete():
        to_delete = delete_entry.get().strip()
        try:
            # Send a DELETE request to the specific entry
            url = f"{endpoint}/{to_delete}"
            print(f"Sending DELETE request to: {url}")  # Debugging: Print the URL
            response = req.delete(url)
            response.raise_for_status()  # Raise an error for bad responses
            mb.showinfo("Delete Success", response.json().get("message"))
            delete_window.destroy()
        except req.exceptions.HTTPError as e:
            mb.showerror("HTTP Error", f"HTTP Error: {e} - Response: {response.text}")
            if DEBUG:
                print(response.text)
        except req.exceptions.RequestException as e:
            mb.showerror("Request Error", f"An error occurred: {e}")
            if DEBUG:
                print(response.text)
        except ValueError as e:
            mb.showerror("JSON Error", f"Invalid JSON response: {e}")
            if DEBUG:
                print(response.text)

    delete_window = Toplevel(root)
    delete_window.title("Delete Entry")

    Label(delete_window, text="Enter the word to delete:").grid(row=0, column=0, padx=10, pady=5)
    delete_entry = Entry(delete_window)
    delete_entry.grid(row=0, column=1, padx=10, pady=5)

    Button(delete_window, text="Delete", command=delete).grid(row=1, column=0, columnspan=2, pady=10)

# Main function to start the Flask app and run the client logic
def main():
    mb.showinfo("Welcome!", """Welcome to Lawrence Dictionary, a crowdsourced, free-to-use dictionary. 
                Be assured, entries are screened for quality assurance!""")

    # Define the endpoint
    global endpoint
    endpoint = "http://127.0.0.1:5000/data"

    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask_app, daemon=True)
    flask_thread.start()

    # Allow some time for the Flask app to start
    time.sleep(2)

    # Main Tkinter window
    global root
    root = Tk()
    root.title("Lawrence Dictionary")

    Button(root, text="Search Entries", command=search_entries).grid(row=0, column=0, padx=10, pady=10)
    Button(root, text="Add New Entry", command=create_new_entry).grid(row=1, column=0, padx=10, pady=10)
    Button(root, text="Delete Entry", command=delete_entry).grid(row=2, column=0, padx=10, pady=10)
    Button(root, text="Exit", command=root.quit).grid(row=3, column=0, padx=10, pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()