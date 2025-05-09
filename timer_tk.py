from tkinter import *
from tkinter.ttk import *
from time import strftime
import pyttsx3
import random as r

# Create window
root = Tk()
root.title('Timer')
root.config(background='purple')

# Style for the frames
style = Style()
style.configure("TFrame", background="purple")

# Frame for input fields
input_frame = Frame(root, style="TFrame")
input_frame.pack(pady=20)

# Minutes
min_in = Entry(input_frame, background='purple', foreground='black')
min_in.pack(side=LEFT, padx=10)
min_in.bind("<Return>", lambda event: setup_rets())
min_lab = Label(input_frame, font=('calibri', 10, 'bold'),
                background='purple',
                foreground='white',
                text="Minutes")
min_lab.pack(side=LEFT)

# Seconds
sec_in = Entry(input_frame, background='purple', foreground='black')
sec_in.pack(side=LEFT, padx=10)
sec_in.bind("<Return>", lambda event: setup_rets())
sec_lab = Label(input_frame, font=('calibri', 10, 'bold'),
                background='purple',
                foreground='white',
                text="Seconds")
sec_lab.pack(side=LEFT)

# Frame for timer display
timer_frame = Frame(root, style="TFrame")
timer_frame.pack()

# Minutes remaining display
m_rem = Label(timer_frame, font=('calibri', 40, 'bold'),
                background='purple',
                foreground='white',
                text="00")
m_rem.pack(side=LEFT, padx=20)

# Seconds remaining display
s_rem = Label(timer_frame, font=('calibri', 40, 'bold'),
                background='purple',
                foreground='white',
                text="00")
s_rem.pack(side=LEFT)

# Frame for buttons
button_frame = Frame(root, style="TFrame")
button_frame.pack(pady=20)

# Setup Button
def on_setup():
    seconds = 0
    try:
        u_min = int(min_in.get()) if min_in.get() else 0
        u_sec = int(sec_in.get()) if sec_in.get() else 0
    except ValueError:
        print("Please enter valid numbers for minutes and seconds.")
        return

    u_min *= 60
    seconds += u_min
    seconds += u_sec
    return seconds

def setup_rets():
    global seconds, original_seconds  
    original_seconds = on_setup() 
    if original_seconds is not None:
        # Format minutes as two digits
        m_rem.config(text=f"{original_seconds // 60:02}")
        # Format seconds as two digits
        s_rem.config(text=f"{original_seconds % 60:02}") 

setup_go = Button(button_frame, text="Prepare Timer", command=setup_rets)
setup_go.pack(side=LEFT, padx=10)

# Start Button
def start_timer():
    global seconds, original_seconds
    if original_seconds is not None:
        seconds = original_seconds
        countdown()

def countdown():
    global seconds
    if seconds > 0:
        seconds -= 1
        # Format minutes as two digits
        m_rem.config(text=f"{seconds // 60:02}")
        # Format seconds as two digits
        s_rem.config(text=f"{seconds % 60:02}")
        root.after(1000, countdown)
    else:
        m_rem.config(text="00")
        s_rem.config(text="00")
        print("Timer finished!")
        speak_timer_ended()

start_go = Button(button_frame, text="Start Timer", command=start_timer)
start_go.pack(side=LEFT, padx=10)

# Reset Button
def reset_timer():
    global seconds, original_seconds
    seconds = None  
    original_seconds = None
    min_in.delete(0, END)  
    sec_in.delete(0, END)  
    m_rem.config(text="00")
    s_rem.config(text="00")

reset_go = Button(button_frame, text="Reset Timer", command=reset_timer)
reset_go.pack(side=LEFT, padx=10)

# Text-to-Speech Function
def speak_timer_ended():
    end_lines = ["Time's Up!", "Timer has ended!", "Wrap it up!", "And That's Time!", "Finish Up!"]
    engine = pyttsx3.init() 
    end_line = r.choice(end_lines)
    rate = engine.getProperty('rate') 
    engine.setProperty('rate', rate - 50) 
    engine.say(end_line)
    engine.runAndWait()

# Bind Shift+Enter key
def start_timer_shift_enter(event):
    if event.state == 1: 
        start_timer()

root.bind("<Shift-Return>", start_timer_shift_enter)

root.mainloop()