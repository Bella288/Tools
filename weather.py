import requests
import sys
from bs4 import BeautifulSoup
import pyttsx3 as tts
import tkinter as tk
from tkinter import messagebox

idents = ['ABQ', 'ABR', 'AFC', 'AFG', 'AJK', 'AKQ', 'ALY', 'AMA', 'APX', 'ARX', 'BGM', 'BIS', 'BMX', 'BOI', 'BOU', 'BOX', 'BRO', 'BTV', 'BUF', 'BYZ', 'CAE', 'CAR', 'CHS', 'CLE', 'CRP', 'CTP', 'CYS', 'DDC', 'DLH', 'DMX', 'DTX', 'DVN', 'EAX', 'EKA', 'EPZ', 'EYW', 'EWX', 'FFC', 'FGF', 'FGZ', 'FSD', 'FWD', 'GGW', 'GID', 'GJT', 'GLD', 'GRB', 'GRR', 'GSP', 'GUA', 'GYX', 'HFO', 'HGX', 'HNX', 'ICT', 'ILM', 'ILN', 'ILX', 'IND', 'IWX', 'JAN', 'JAX', 'JKL', 'LBF', 'LCH', 'LIX', 'LKN', 'LMK', 'LOT', 'LOX', 'LSX', 'LUB', 'LWX', 'LZK', 'MAF', 'MEG', 'MFL', 'MFR', 'MHX', 'MKX', 'MLB', 'MOB', 'MPX', 'MQT', 'MRX', 'MSO', 'MTR', 'OAX', 'OHX', 'OKX', 'OTX', 'OUN', 'PAH', 'PBZ', 'PDT', 'PHI', 'PIH', 'PQR', 'PSR', 'PUB', 'RAH', 'REV', 'RIW', 'RLX', 'RNK', 'SEW', 'SGF', 'SGX', 'SHV', 'SJT', 'SJU', 'SLC', 'STO', 'TAE', 'TBW', 'TFX', 'TOP', 'TSA', 'TWC', 'UNR', 'VEF', 'ACR', 'ALR', 'FWR', 'KRF', 'MSR', 'ORN', 'PTR', 'RHA', 'RSA', 'STR', 'TAR', 'TIR', 'TUA', 'ZAB', 'ZAN', 'ZAU', 'ZBW', 'ZDC', 'ZDV', 'ZFW', 'ZHU', 'ZID', 'ZJX', 'ZKC', 'ZLA', 'ZLC', 'ZMA', 'ZME', 'ZMP', 'ZOA', 'ZOB', 'ZSE', 'ZTL', 'ZYN']

def get_hazardous_weather_outlook(location_code):
    url = f'https://forecast.weather.gov/wwamap/wwatxtget.php?cwa={location_code}&wwa=hazardous%20weather%20outlook'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        outlook_div = soup.find('div', {'id': 'content'})
        if outlook_div:
            return outlook_div.get_text()
        else:
            messagebox.showerror("Error", "Unable to find the Hazardous Weather Outlook section.")
            sys.exit(1)
    else:
        messagebox.showerror("Error", f"Error {response.status_code}: Unable to fetch the Hazardous Weather Outlook for {location_code}.")
        sys.exit(1)

def fetch_outlook():
    location_code = entry.get().upper()
    if location_code not in idents:
        messagebox.showerror("Error", "Invalid location code. Please refer to the provided link for valid codes.")
        return
    
    outlook = get_hazardous_weather_outlook(location_code)
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, f"TOP\n{outlook}\nEND OF OUTLOOK")
    
    bot = tts.init()
    bot.say(outlook)
    bot.runAndWait()

# Create the main window
root = tk.Tk()
root.title("Hazardous Weather Outlook")

# Create and place the label
label = tk.Label(root, text="Enter the 3-Character Identifier for your city\n(Refer to https://training.weather.gov/nwstc/sysinfo/sites.html, and use the city closest to you.)")
label.pack(pady=10)

# Create and place the entry widget
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

# Create and place the fetch button
fetch_button = tk.Button(root, text="Fetch Outlook", command=fetch_outlook)
fetch_button.pack(pady=10)

# Create and place the text area
text_area = tk.Text(root, height=20, width=80)
text_area.pack(pady=10)

# Run the main loop
root.mainloop()