import tkinter as tk
from tkinter import ttk
import pyautogui
import threading
import time
from pynput import keyboard

class AutoclickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Autoclicker")
        self.running = False
        self.cps = 10  # Default CPS
        self.thread = None
        self.countdown = 5  # Countdown time in seconds
        self.listener = None

        # Create and place widgets
        self.create_widgets()

        # Start listening for global keyboard events
        self.start_listening()

    def create_widgets(self):
        # CPS Label and Entry
        self.cps_label = ttk.Label(self.root, text="Clicks Per Second (CPS):")
        self.cps_label.grid(column=0, row=0, padx=10, pady=10, sticky=tk.W)

        self.cps_entry = ttk.Entry(self.root)
        self.cps_entry.insert(0, str(self.cps))
        self.cps_entry.grid(column=1, row=0, padx=10, pady=10)

        # Start/Stop Button
        self.start_stop_button = ttk.Button(self.root, text="Start", command=self.toggle_clicking)
        self.start_stop_button.grid(column=0, row=1, columnspan=2, pady=10)

    def start_listening(self):
        # Set up the listener for global keyboard events
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def on_press(self, key):
        # Check if the Esc key is pressed
        if key == keyboard.Key.esc:
            self.toggle_clicking()

    def toggle_clicking(self):
        if not self.running:
            try:
                self.cps = float(self.cps_entry.get())
                if self.cps <= 0:
                    raise ValueError("CPS must be greater than 0.")
            except ValueError:
                self.cps_entry.delete(0, tk.END)
                self.cps_entry.insert(0, str(self.cps))
                return

            self.running = True
            self.start_stop_button.config(state=tk.DISABLED)  # Disable the button during countdown
            self.countdown_thread = threading.Thread(target=self.countdown_before_start)
            self.countdown_thread.start()
        else:
            self.running = False
            self.start_stop_button.config(text="Start", state=tk.NORMAL)

    def countdown_before_start(self):
        for i in range(self.countdown, 0, -1):
            self.start_stop_button.config(text=f"Start ({i})")
            time.sleep(1)
            if not self.running:  # Check if the user stopped the countdown
                break
        if self.running:
            self.start_stop_button.config(text="Stop", state=tk.NORMAL)
            self.thread = threading.Thread(target=self.click)
            self.thread.start()
        else:
            self.start_stop_button.config(text="Start")

    def click(self):
        interval = 0.0000001 / self.cps
        next_click_time = time.perf_counter()
        while self.running:
            pyautogui.click()
            next_click_time += interval
            sleep_duration = next_click_time - time.perf_counter()
            if sleep_duration > 0:
                time.sleep(sleep_duration)

    def __del__(self):
        # Ensure the listener is stopped when the application is closed
        if self.listener:
            self.listener.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoclickerApp(root)
    root.mainloop()